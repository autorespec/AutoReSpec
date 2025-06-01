import path from 'path';
import { writeFileSync, readFileSync, unlinkSync } from 'fs';
import { execSync } from 'child_process';
import { createFolderIfNotExist, logger } from '../utils';
import { config } from '../config/config';

export function validateOpenJML(
  codeWithSpec: string,
  className: string,
): string {
  const tmpDir = path.resolve('./validators/tmp');
  createFolderIfNotExist(tmpDir);

  const javaFilePath = path.join(tmpDir, `${className}.java`);
  writeFileSync(javaFilePath, codeWithSpec);

  const validatorBinary = path.resolve('./openjml/openjml');

  const cmd = `${validatorBinary} --esc --esc-max-warnings=${config.openJML.max_warning} --arithmetic-failure=quiet --nonnull-by-default --timeout=${config.openJML.validator_timeout} --quiet -nowarn --prover=${config.openJML.prover} ${javaFilePath}`;

  let output = '';
  try {
    output = execSync(cmd, {
      encoding: 'utf-8',
      timeout: config.openJML.validator_timeout * 1000,
    });
    if (!output.trim()) {
      logger.info('No error found by validator!');
    }
  } catch (err: any) {
    output = err.stdout || err.message;
  } finally {
    unlinkSync(javaFilePath); // deletes the temp file
  }
  return output;
}
