import createHttpError from 'http-errors';
import { GenerateSpecInput } from '../schemas/autoReSpecRequestSchema';
import { getOllamaResponse, validateOpenJML } from '../services';
import { logger, parseClassName, parseCodeBlock } from '../utils';
import * as llmService from './../services';
import { Message } from '../types';
import * as refinementPromptService from './refinementPromptService';
import { FEEDBACK_MESSAGE } from '../constants';
import { generateGuidanceFromError } from '../utils/guidance';

export const generateSpec = async ({
  model,
  testcase,
  shotCount,
  iteration,
  collaboratorModel,
  collaboratorIteration,
  collaborativeShotCount,
}: GenerateSpecInput) => {
  const fewShotPrompt = await llmService.generateFewShotMessages(
    shotCount,
    testcase,
  );

  let prompt = [...fewShotPrompt];

  logger.info('iter-1 few-shot prompt', { prompt });
  let LLMResponse: any;
  let LLMResponseMessage: any;

  if (model.startsWith('gpt')) {
    LLMResponseMessage = await llmService.getGptResponse(model, prompt);
  } else if (model.startsWith('claude')) {
    LLMResponseMessage = await llmService.getAnthropicResponse(model, prompt);
  } else {
    LLMResponseMessage = await getOllamaResponse(model, prompt);
  }

  if (!LLMResponseMessage) {
    throw new createHttpError.BadGateway(`Invalid response from ${model}`);
  }

  let codeWithSpec = parseCodeBlock(LLMResponseMessage);
  logger.info('iter-1 current code', { codeWithSpec });

  const className = parseClassName(testcase);
  let validatorOutput = validateOpenJML(codeWithSpec, className);
  logger.info('iter-1 validator output', { validatorOutput });

  let iterUsed = 1;

  prompt = appendFeedbackMessage(prompt, codeWithSpec, validatorOutput);
  if (validatorOutput && iteration > 1) {
    ({ codeWithSpec, validatorOutput, iterUsed, prompt } =
      await conversationalSpecGeneration(
        model,
        codeWithSpec,
        validatorOutput,
        prompt,
        iteration,
      ));
  }

  let collaboratorIterUsed: number = 0;
  if (validatorOutput && collaboratorModel) {
    logger.info(
      `Conversation was not successful. collaborating with ${collaboratorModel}`,
    );
    collaboratorIterUsed++;
    ({
      codeWithSpec,
      validatorOutput,
      iterUsed: collaboratorIterUsed,
      prompt,
    } = await collaborativeSpecGeneration(
      collaboratorModel,
      codeWithSpec,
      validatorOutput,
      prompt,
      collaboratorIteration ?? 10,
      collaborativeShotCount,
    ));
  }

  return {
    verificationStatus: validatorOutput ? false : true,
    annotatedCode: codeWithSpec,
    validatorResponse: validatorOutput
      ? validatorOutput
      : 'No error found by validator!',
    iteration: iterUsed,
    collaboratorModel: collaboratorModel ?? null,
    collaboratorIteration: collaboratorIterUsed,
    prompt,
  };
};

export const collaborativeSpecGeneration = async (
  collaboratorModel: string,
  codeWithSpec: string,
  validatorOutput: string,
  prompt: Message[],
  collaboratorIteration: number,
  shotCount: number = 2,
) => {
  const initPrompt = await llmService.generateCollaboratorInitPrompt(
    codeWithSpec,
    validatorOutput,
    shotCount,
  );
  logger.info('collaboration iter-1 init prompt', { initPrompt });
  let currentCode = codeWithSpec;
  let currentValidatorOutput = validatorOutput;
  const className = parseClassName(currentCode);
  currentCode = await getAnnotatedCode(collaboratorModel, initPrompt);
  logger.info('collaboration iter-1 current code', { currentCode });
  currentValidatorOutput = validateOpenJML(currentCode, className);
  logger.info('collaboration iter-1 current validator output', {
    currentValidatorOutput,
  });

  let iterUsed = 1;

  prompt = appendFeedbackMessage(prompt, currentCode, currentValidatorOutput);
  if (currentValidatorOutput && collaboratorIteration > 1) {
    return await conversationalSpecGeneration(
      collaboratorModel,
      currentCode,
      currentValidatorOutput,
      prompt,
      collaboratorIteration ?? 10,
      true,
    );
  }
  return {
    codeWithSpec: currentCode,
    validatorOutput: currentValidatorOutput.trim(),
    iterUsed,
    prompt,
  };
};

export const conversationalSpecGeneration = async (
  model: string,
  codeWithSpec: string,
  validatorOutput: string,
  prevPrompt: Message[],
  iteration: number,
  collaboration: boolean = false,
) => {
  let currentCode = codeWithSpec;
  let currentValidatorOutput = validatorOutput;

  let currentPrompt: Message[] = [...prevPrompt];

  let iterUsed = 1;

  for (let iter = 2; iter <= iteration; iter++) {
    logger.info(
      `${collaboration ? 'Collaboration' : 'conversational'} Iteration ${iter} — Sending prompt to ${model}`,
    );

    let nextPrompt: Message[];

    const errorTags = refinementPromptService.extractErrorTags(
      currentValidatorOutput,
    );
    if (errorTags.length > 0) {
      logger.info(`error tag detected: ${errorTags}`);
      const refinementPrompt =
        await refinementPromptService.generateRefinementPrompt(
          errorTags,
          currentCode,
          currentValidatorOutput,
        );
      nextPrompt = [...refinementPrompt];
    } else {
      const guidance = generateGuidanceFromError(validatorOutput);

      nextPrompt = replaceLastUserWithGuidance(currentPrompt, guidance);
    }

    logger.info(
      `${collaboration ? 'Collaboration' : 'conversational'} iter-${iter} next prompt`,
      { nextPrompt },
    );

    const refinedCode = await getAnnotatedCode(model, nextPrompt);
    logger.info(`iter-${iter} annotated code`, { refinedCode });

    const className = parseClassName(refinedCode);
    const validatorResult = validateOpenJML(refinedCode, className);
    logger.info(
      `${collaboration ? 'Collaboration' : 'conversational'} iter-${iter} validator result`,
      { validatorResult },
    );

    currentCode = refinedCode;
    currentValidatorOutput = validatorResult;

    if (!validatorResult || validatorResult.trim() === '') {
      logger.info(
        `${collaboration ? 'Collaboration' : 'conversational'} successful on iteration ${iter}`,
      );
      const finalPrompt = appendFeedbackMessage(
        nextPrompt,
        currentCode,
        validatorResult,
      );
      logger.info('final prompt', { finalPrompt });
      return {
        codeWithSpec: currentCode,
        validatorOutput: '',
        iterUsed: iter,
        prompt: finalPrompt,
      };
    }

    currentPrompt = appendFeedbackMessage(
      nextPrompt,
      refinedCode,
      validatorResult,
    );
    iterUsed = iter;
  }

  return {
    codeWithSpec: currentCode,
    validatorOutput: currentValidatorOutput.trim(),
    iterUsed,
    prompt: currentPrompt,
    verified: validatorOutput.length > 0,
  };
};

const getAnnotatedCode = async (model: string, prompt: Message[]) => {
  let LLMResponse: any;
  let message: any;

  if (model.startsWith('gpt')) {
    message = await llmService.getGptResponse(model, prompt);
  } else if (model.startsWith('claude')) {
    message = await llmService.getAnthropicResponse(model, prompt);
  } else {
    message = await getOllamaResponse(model, prompt);
  }

  console.log({ message });

  if (!message) {
    throw new createHttpError.BadGateway(`Invalid response from ${model}`);
  }

  const codeWithSpec = parseCodeBlock(message);
  return codeWithSpec;
};

const appendFeedbackMessage = (
  messages: Message[],
  codeWithSpec: string,
  validatorOutput: string,
): Message[] => {
  const updatedPrompt: Message[] = [
    ...messages,
    {
      role: 'assistant',
      content: `\`\`\`java\n${codeWithSpec}\n\`\`\``,
    },
  ];
  if (validatorOutput && validatorOutput.trim() !== '') {
    updatedPrompt.push({
      role: 'user',
      content: FEEDBACK_MESSAGE.replace(
        '{specified_code}',
        codeWithSpec,
      ).replace('{err_info}', validatorOutput),
    });
  }
  return updatedPrompt;
};

export const replaceLastUserWithGuidance = (
  messages: Message[],
  guidanceSuffix: string,
): Message[] => {
  console.log('adding guidance prompt');
  // find the last user content index
  const lastUserIndex = [...messages]
    .reverse()
    .findIndex((m) => m.role === 'user');

  // if user message not found
  if (lastUserIndex === -1) return messages;

  const indexToReplace = messages.length - 1 - lastUserIndex;
  const oldMsg = messages[indexToReplace];

  const updated = {
    role: 'user',
    content: oldMsg.content + '\n\n' + guidanceSuffix,
  };

  const next = [...messages];
  next.splice(indexToReplace, 1, updated);
  return next;
};
