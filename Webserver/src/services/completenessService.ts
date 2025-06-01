import { existsSync } from 'fs';
import fs, { readFile } from 'fs/promises';
import createHttpError from 'http-errors';
import path from 'path';
import { parseClassName } from '../utils';
import { promisify } from 'util';
import { exec } from 'child_process';
import { validateOpenJML } from './validatorService';
const execAsync = promisify(exec);

const MAJOR_BIN = path.resolve('major/bin/major');
const MAJOR_MML = path.resolve('src/config/major.mml.bin');
const COMPLETENESS_DIR = path.resolve('completenessAnalysis');

export const generateMutations = async (testcase: string) => {
  const className = parseClassName(testcase);
  const timestamp = Date.now();

  await fs.mkdir(COMPLETENESS_DIR, { recursive: true });
  const targetDir = path.join(COMPLETENESS_DIR, `${className}-${timestamp}`);
  await fs.mkdir(targetDir, { recursive: true });
  const targetPath = path.join(targetDir, `${className}.java`);
  await fs.writeFile(targetPath, testcase);

  console.log('Running mutation in:', targetDir);
  console.log('Classpath:', path.resolve('major/build'));

  if (!existsSync(MAJOR_BIN)) {
    throw createHttpError(500, `Major not found at: ${MAJOR_BIN}`);
  }
  if (!existsSync(MAJOR_MML)) {
    throw createHttpError(500, `MML config not found at: ${MAJOR_MML}`);
  }

  const command = `"${MAJOR_BIN}" --mml "${MAJOR_MML}" "${targetPath}" --export export.mutants`;

  try {
    const { stdout, stderr } = await execAsync(command, { cwd: targetDir });
    if (stderr) console.warn(`Mutation stderr: ${stderr}`);
    console.log(`Mutation stdout:\n${stdout}`);
    return targetDir;
  } catch (err) {
    console.error('Mutation generation failed:', err);
    throw new createHttpError.InternalServerError('Mutation analysis failed');
  }
};

export const measureCompleteness = async (testcase: string) => {
  const targetDir = await generateMutations(testcase);
  const mutantDir = path.join(targetDir, 'mutants');

  let mutantCount = 0;
  let errorCount = 0;

  const subdirs = await fs.readdir(mutantDir);

  for (const sub of subdirs) {
    const subPath = path.join(mutantDir, sub);
    const files = await fs.readdir(subPath);

    for (const file of files) {
      if (!file.endsWith('.java')) continue;

      const filePath = path.join(subPath, file);
      console.log('evaluating... ', filePath);
      const code = await readFile(filePath, 'utf-8');
      const className = parseClassName(code);
      try {
        mutantCount++;
        const validatorOutput = validateOpenJML(code, className);
        console.log(validatorOutput);

        if (validatorOutput.trim()) {
          errorCount++;
          console.warn(`OpenJML error in ${file}:\n${validatorOutput}`);
        }
      } catch (err) {
        errorCount++;
        console.error(`Validation failed for ${file}:`, err.message || err);
      }
    }
  }
  const completeness =
    mutantCount === 0 ? 0 : (errorCount / mutantCount).toFixed(2);
  console.log(
    `n_mutants: ${mutantCount}, n_errors: ${errorCount}, completeness: ${completeness}`,
  );
  return {
    mutantCount,
    errorCount,
    completeness,
    mutantDir,
  };
};
