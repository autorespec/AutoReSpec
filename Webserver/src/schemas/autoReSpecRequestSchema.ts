import { z } from 'zod';

export const generateSpecSchema = z.object({
  model: z
    .string({ required_error: 'Model is required' })
    .min(1, 'Model is required'),
  testcase: z
    .string({ required_error: 'Testcase is required' })
    .min(1, 'Testcase is required'),
  shotCount: z
    .number({ required_error: 'shotCount is required' })
    .min(0)
    .max(4),
  iteration: z
    .number({ required_error: 'iteration is required' })
    .min(1)
    .max(10),
  collaboratorModel: z.string().optional(),
  collaboratorIteration: z.number().optional(),
  collaborativeShotCount: z.number().optional(),
});

export type GenerateSpecInput = z.infer<typeof generateSpecSchema>;
