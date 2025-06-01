import * as exampleRepository from '../repositories/exampleRepository';
import { config } from '../config/config';
export const getAllExamples = async () => {
  return await exampleRepository.findAllExamples();
};

export const getRandomExamples = async (count = 2) => {
  const shuffled = [...config.groundTruth].sort(() => 0.5 - Math.random());
  const selectedClassNames = shuffled.slice(0, count);

  const allExamples = await exampleRepository.findAllExamples();
  const selectedExamples = allExamples.filter((example) =>
    selectedClassNames.includes(example.className),
  );

  return selectedExamples;
};
