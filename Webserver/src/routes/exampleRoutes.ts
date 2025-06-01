import express from 'express';
import * as exampleController from '../controllers/exampleController';

const router = express.Router();

router.get('/', exampleController.getAllExamples);
router.post('/', exampleController.createExample);
router.get('/random', exampleController.getRandomExamples);
router.post('/bulk', exampleController.createExamples);

export default router;
