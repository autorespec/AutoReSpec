import axios from 'axios';
import createHttpError from 'http-errors';
import { config } from '../config/config';

const ollamaURL = process.env.OLLAMA_URL!;

export const generateOllamaResponse = async (prompt: string, model: string) => {
  if (!prompt || typeof prompt !== 'string') {
    throw new createHttpError.BadRequest('Prompt must be a string');
  }

  const response = await axios.post(`${ollamaURL}/api/chat`, {
    model,
    messages: [{ role: 'user', content: prompt }],
    ...config.ollamaOptions,
  });
  const ollamaResponse = response.data;
  return ollamaResponse;
};

export const getOllamaModelsDetails = async () => {
  const response = await axios.get(`${ollamaURL}/api/tags`);
  const ollamaResponse = response.data;
  console.log(ollamaResponse);
  return ollamaResponse;
};

export const getOllamaModels = async () => {
  const allModelDetails = await getOllamaModelsDetails();
  const modelNames = allModelDetails.models.map((model: any) => {
    return model.name;
  });
  return modelNames;
};
