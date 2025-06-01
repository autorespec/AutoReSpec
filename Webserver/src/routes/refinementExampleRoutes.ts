import express from 'express';
import * as refinementExampleController from '../controllers/refinementExampleController';

const router = express.Router();

router.get('/', refinementExampleController.getAllExamples);
router.post('/', refinementExampleController.createExample);
router.get('/tag', refinementExampleController.getExamplesByTags);
router.post('/bulk', refinementExampleController.createManyExamples);

export default router;
