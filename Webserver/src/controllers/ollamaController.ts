import { Request, Response } from 'express';
import * as ollamaService from './../services/ollamaService';
import { StatusCodes } from 'http-status-codes';
export const handleOllamaPrompt = async (req: Request, res: Response) => {
  const { prompt, model } = req.body;
  const ollamaResponse = await ollamaService.generateOllamaResponse(
    prompt,
    model,
  );
  res.status(StatusCodes.OK).json({ response: ollamaResponse });
};

export const getOllamaModelsDetails = async (req: Request, res: Response) => {
  const ollamaResponse = await ollamaService.getOllamaModelsDetails();
  res.status(StatusCodes.OK).json(ollamaResponse);
};

export const getOllamaModels = async (req: Request, res: Response) => {
  const ollamaResponse = await ollamaService.getOllamaModels();
  res.status(StatusCodes.OK).json(ollamaResponse);
};
