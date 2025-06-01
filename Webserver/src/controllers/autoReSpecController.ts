import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import { GenerateSpecInput } from '../schemas/autoReSpecRequestSchema';
import * as autoReSpecService from '../services/autoReSpecService';
import * as completenessService from '../services/completenessService';

export const generateSpec = async (
  req: Request<{}, {}, GenerateSpecInput>,
  res: Response,
) => {
  const {
    model,
    testcase,
    shotCount,
    iteration,
    collaboratorIteration,
    collaboratorModel,
    collaborativeShotCount,
  } = req.body;
  const apiResponse = await autoReSpecService.generateSpec({
    model,
    testcase,
    shotCount,
    iteration,
    collaboratorModel,
    collaborativeShotCount,
    collaboratorIteration,
  });
  res.status(StatusCodes.OK).json(apiResponse);
};

export const measureCompleteness = async (req: Request, res: Response) => {
  const { testcase } = req.body;
  const apiResponse = await completenessService.measureCompleteness(testcase);
  res.status(StatusCodes.OK).json(apiResponse);
};
