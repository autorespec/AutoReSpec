import express from 'express';
import * as ollamaController from './../controllers/ollamaController';

const router = express.Router();

router.post('/chat', ollamaController.handleOllamaPrompt);
router.get('/models-details', ollamaController.getOllamaModelsDetails);
router.get('/models', ollamaController.getOllamaModels);

export default router;
