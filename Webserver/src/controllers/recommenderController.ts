import { Request, Response } from 'express';
import { StatusCodes } from 'http-status-codes';
import * as recommenderService from './../services/recommenderService';

export const getRecommendedLLM = async (req: Request, res: Response) => {
  const { testcase } = req.body;
  const apiResponse = await recommenderService.recommendLLMsFromCode(testcase);
  res.status(StatusCodes.OK).json(apiResponse);
};
