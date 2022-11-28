import { Request, Response } from "express";
import HttpException from "../helpers/httpExceptions.helper";

export const errorHandler = (
  error: HttpException,
  request: Request,
  response: Response
) => {
  const status = error.statusCode || 500;

  response
    .status(status)
    .send({ ResponseMessage: error.statusMessage, IsError: true });
};
