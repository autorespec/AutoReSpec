import { config } from '../config/config';
import { FORMAT_REFINEMENT_PROMPT, SYSTEM_MESSAGE } from '../constants';
import { Message } from '../types';
import * as refinementExampleService from './refinementExampleService';
export const extractErrorTags = (validatorError: string): string[] => {
  const promptList: string[] = [];

  const keywordDict: Record<string, string> = {
    DivideByZero: 'divide_by_zero',
    visibility: 'private_visibility',
    NegativeIndex: 'negative_index',
    TooLargeIndex: 'too_large_index',
    'ArithmeticOperationRange negation': 'overflow_negation',
    'overflow sum': 'overflow_sum',
    'overflow difference': 'overflow_sub',
    'overflow multiply': 'overflow_mul',
    'overflow divide': 'overflow_div',
    'underflow sum': 'underflow_sum',
    'underflow difference': 'underflow_sub',
    'underflow multiply': 'underflow_mul',
    'underflow divide': 'underflow_div',
  };

  for (const key in keywordDict) {
    const keywordList = key.split(' ');
    const allFound = keywordList.every((keyword) =>
      validatorError.includes(keyword),
    );

    if (allFound) {
      promptList.push(keywordDict[key]);
    }
  }

  return promptList;
};

// export const getExamplesForErrorTags = async (errorTags: string[]) => {};
export const generateRefinementPrompt = async (
  errorTags: string[],
  codeWithSpec: string,
  validatorOutput: string,
) => {
  const refinementExamples =
    await refinementExampleService.getRefinementExamples(errorTags);

  const systemMessage = { role: 'system', content: SYSTEM_MESSAGE }; // should not include

  const refinementMessages = refinementExamples.flatMap((ex) => [
    {
      role: 'user',
      content: FORMAT_REFINEMENT_PROMPT.replace(
        '{specified_code}',
        ex.original,
      ).replace('{err_info}', ex.errorInfo),
    },
    {
      role: 'assistant',
      content: `\`\`\`java\n${ex.refined}\n\`\`\``,
    },
  ]);

  // this includes the feedback message!?
  const currentMessage = {
    role: 'user',
    content: FORMAT_REFINEMENT_PROMPT.replace(
      '{specified_code}',
      codeWithSpec,
    ).replace('{err_info}', validatorOutput),
  };
  return [systemMessage, ...refinementMessages, currentMessage];
  // return [...refinementMessages, currentMessage];
};

export const generateGuidancePrompt = (prevMessages: Message[]) => {
  // if guidance prompts were not found do what?
  return prevMessages;
  // const refineMsg = {
  //   role: 'user',
  //   content: config.get('FORMAT_REFINE_PROMPT').replace('{err_info}', err_info),
  // };
  // refine_msg['content'] += gen_extra_guidance(err_info);
  // llm_config['messages'].append(refine_msg);
};
