import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils';

export const errorHandler = (
  err: Error & { status?: number; statusCode?: number },
  _req: Request,
  res: Response,
  _next: NextFunction,
) => {
  const status = err.status || err.statusCode || 500;

  logger.error({
    message: err.message,
    stack: err.stack,
  });

  res.status(status).json({
    error: err.name || 'Error',
    message: err.message,
  });
};
