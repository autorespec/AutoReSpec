import express from 'express';
import { generateSpec, measureCompleteness } from '../controllers';
import { validateRequest } from '../middlewares/validate';
import { generateSpecSchema } from '../schemas/autoReSpecRequestSchema';
import { getRecommendedLLM } from '../controllers/recommenderController';

const router = express.Router();

router.post(
  '/generate-spec',
  validateRequest(generateSpecSchema),
  generateSpec,
);
router.post('/measure-completeness', measureCompleteness);
router.post('/recommend', getRecommendedLLM);

export default router;
