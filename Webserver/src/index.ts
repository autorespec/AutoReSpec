import 'express-async-errors';
import express from 'express';
import morgan from 'morgan';
import cors from 'cors';
import dotenv from 'dotenv';
dotenv.config();

import { errorHandler, notFound } from './middlewares';

import ollamaRoutes from './routes/ollamaRoutes';
import autoReSpecService from './routes/autoReSpecRoutes';
import exampleRoutes from './routes/exampleRoutes';
import refinementRoutes from './routes/refinementExampleRoutes';

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json({ limit: '10mb' }));
app.use(morgan('dev'));

app.use('/api/ollama', ollamaRoutes);
app.use('/api/autorespec', autoReSpecService);
app.use('/api/examples', exampleRoutes);
app.use('/api/refinement', refinementRoutes);
app.use(notFound);
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
