import { Request, Response, NextFunction } from 'express';
import * as refinementExampleService from '../services/refinementExampleService';
import createHttpError from 'http-errors';
import { StatusCodes } from 'http-status-codes';

export const createExample = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const { tag, errorInfo, original, refined } = req.body;
    const saved = await refinementExampleService.createExample(
      tag,
      errorInfo,
      original,
      refined,
    );
    res.status(StatusCodes.CREATED).json(saved);
  } catch (err) {
    next(err);
  }
};

export const createManyExamples = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const examples = req.body;
    const saved = await refinementExampleService.createManyExamples(examples);
    res.status(StatusCodes.CREATED).json(saved);
  } catch (err) {
    next(err);
  }
};

export const getAllExamples = async (
  _req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const examples = await refinementExampleService.getAllExamples();
    res.status(StatusCodes.OK).json(examples);
  } catch (err) {
    next(err);
  }
};

export const getExamplesByTags = async (
  req: Request,
  res: Response,
  next: NextFunction,
) => {
  try {
    const { tags } = req.body;

    if (!Array.isArray(tags) || tags.length === 0) {
      throw createHttpError.BadRequest('tags must be a non-empty array');
    }

    const examples = await refinementExampleService.getRefinementExamples(tags);
    res.status(StatusCodes.OK).json(examples);
  } catch (err) {
    next(err);
  }
};
