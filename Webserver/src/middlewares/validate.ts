import { Request, Response, NextFunction } from 'express';
import { ZodSchema } from 'zod';
import createHttpError from 'http-errors';

export const validateRequest =
  (schema: ZodSchema) => (req: Request, _res: Response, next: NextFunction) => {
    try {
      req.body = schema.parse(req.body);
      next();
    } catch (err: any) {
      const message =
        err.errors?.map((e: any) => e.message).join(', ') ||
        'Validation failed';
      next(createHttpError.BadRequest(message));
    }
  };
