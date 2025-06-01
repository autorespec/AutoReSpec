import * as refinementExampleRepository from '../repositories/refinementExampleRepository';
// import { IRefinementExample } from '../models';
// export const createExample = async (
//   tag: string,
//   errorInfo: string,
//   original: string,
//   refined: string,
// ) => {
//   return await refinementExampleRepository.createRefinementExample(
//     tag,
//     errorInfo,
//     original,
//     refined,
//   );
// };

export const getAllExamples = async () => {
  return await refinementExampleRepository.findAllRefinementExamples();
};

// export const createManyExamples = async (
//   refinementExamples: IRefinementExample[],
// ) => {
//   if (!Array.isArray(refinementExamples) || refinementExamples.length === 0) {
//     throw new Error('Input must be a non-empty array of examples');
//   }
//   return await refinementExampleRepository.insertManyRefinementExamples(
//     refinementExamples,
//   );
// };

export const getRefinementExamples = async (errorTag: string[]) => {
  return await refinementExampleRepository.findAllRefinementExamples({
    tag: { $in: errorTag },
  });
};
