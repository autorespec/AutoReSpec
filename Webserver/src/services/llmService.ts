import {
  COLLABORATOR_FEEDBACK_MESSAGE,
  COLLABORATOR_SYSTEM_MESSAGE,
  FORMAT_GENERATION_PROMPT,
  FORMAT_INIT_PROMPT,
  SYSTEM_MESSAGE,
} from '../constants/prompts';
import * as exampleService from '../services';
import { Example } from '../types';
import { config } from './../config/config';
import type { Message } from './../types';
import axios from 'axios';
import OpenAI from 'openai';
import Anthropic from '@anthropic-ai/sdk';

const ollamaURL = process.env.OLLAMA_URL!;
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const anthropic = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

export const getAnthropicResponse = async (model: string, messages: any) => {
  const filteredMessages = messages.filter((msg: any) => msg.role !== 'system');

  const anthropicResponse = await anthropic.messages.create({
    model: model,
    system: COLLABORATOR_SYSTEM_MESSAGE,
    max_tokens: 1024,
    messages: filteredMessages,
  });

  const content = anthropicResponse.content[0];
  const { text: message } = content as any;

  return message;
};

export const getOllamaResponse = async (model: string, messages: Message[]) => {
  const LLMResponse = await axios.post(`${ollamaURL}/api/chat`, {
    model,
    messages,
    ...config.ollamaOptions,
  });
  console.log({
    ollamaResponse: LLMResponse.data,
  });
  return LLMResponse.data?.message.content;
};

export const getGptResponse = async (model: string, messages: any) => {
  console.log({ model, messages });
  const response = await openai.chat.completions.create({
    model,
    messages,
  });
  return response.choices[0].message.content;
};

export const generateFewShotMessages = async (
  shotCount = 2,
  testcase: string,
) => {
  const fewShotExamples = await exampleService.getRandomExamples(shotCount);

  const fewShotMessages = fewShotExamples.flatMap((ex: Example) => [
    {
      role: 'user',
      content: FORMAT_INIT_PROMPT.replace('{src_code}', ex.testcase),
    },
    { role: 'assistant', content: `\`\`\`java\n${ex.groundTruth}\n\`\`\`` },
  ]);

  const messages = [
    {
      role: 'system',
      content: SYSTEM_MESSAGE,
    },
    ...fewShotMessages,
    {
      role: 'user',
      content: FORMAT_GENERATION_PROMPT.replace('{src_code}', testcase),
    },
  ];

  return messages;
};

export const generateCollaboratorInitPrompt = async (
  codeWithSpec: string,
  validatorOutput: string,
  shotCount = 2,
) => {
  const fewShotExamples = await exampleService.getRandomExamples(shotCount);
  const fewShotMessages = fewShotExamples.flatMap((ex: Example) => [
    {
      role: 'user',
      content: FORMAT_INIT_PROMPT.replace('{src_code}', ex.testcase),
    },
    { role: 'assistant', content: `\`\`\`java\n${ex.groundTruth}\n\`\`\`` },
  ]);

  const messages = [
    {
      role: 'system',
      content: COLLABORATOR_SYSTEM_MESSAGE,
    },
    ...fewShotMessages,
    {
      role: 'user',
      content: COLLABORATOR_FEEDBACK_MESSAGE.replace(
        '{specified_code}',
        codeWithSpec,
      ).replace('{err_info}', validatorOutput),
    },
  ];
  return messages;
};
