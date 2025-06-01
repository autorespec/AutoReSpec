import { recommendLLM } from '../data';
import { classifyProgramType } from './ASTService';

type LLMConfig = {
  model: string;
  shot_count: number;
};

type Recommendation = {
  programType: string;
  primaryLLM: LLMConfig;
  collaborativeLLM: LLMConfig;
};

const defaultRecommendation: Recommendation = {
  programType: 'Unknown',
  primaryLLM: { model: 'llama3:8b', shot_count: 2 },
  collaborativeLLM: { model: 'gpt-4o', shot_count: 4 },
};

export function recommendLLMsFromType(programType: string): Recommendation {
  const match = recommendLLM.find((entry) => entry.programType === programType);
  return (
    match || recommendLLM.find((entry) => entry.programType === 'default')!
  );
}

export function recommendLLMsFromCode(javaCode: string): Recommendation {
  const programType = classifyProgramType(javaCode);
  console.log({ programType });
  return recommendLLMsFromType(programType);
}
