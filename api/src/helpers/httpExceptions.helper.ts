/**
 * Error.Exception
 */
export default class HttpException extends Error {
  statusCode: number;
  statusMessage: string;
  error: string | null;

  constructor(statusCode: number, statusMessage: string, error?: string) {
    super(statusMessage);
    this.statusCode = statusCode;
    this.statusMessage = statusMessage;
    this.error = error || null;
  }
}
