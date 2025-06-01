import { Request, Response } from 'express';
import * as exampleService from '../services/exampleService';
import { StatusCodes } from 'http-status-codes';

export const createExample = async (req: Request, res: Response) => {
  const { className, testcase, groundTruth } = req.body;
  const saved = await exampleService.createExample(
    className,
    testcase,
    groundTruth,
  );
  res.status(StatusCodes.CREATED).json(saved);
};

export const getAllExamples = async (req: Request, res: Response) => {
  const allExamples = await exampleService.getAllExamples();
  res.status(StatusCodes.OK).json(allExamples);
};

export const createExamples = async (req: Request, res: Response) => {
  const { examples } = req.body;
  const saved = await exampleService.createManyExamples(examples);
  res.status(StatusCodes.CREATED).json(saved);
};

export const getRandomExamples = async (req: Request, res: Response) => {
  const { count } = req.body;
  const randomExamples = await exampleService.getRandomExamples(count);
  res.status(StatusCodes.OK).json(randomExamples);
};
