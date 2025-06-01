import createHttpError from 'http-errors';

export function parseClassName(code: string): string {
  const classMatch = code.match(/\bclass\s+([A-Za-z_][A-Za-z0-9_]*)\b/);
  if (!classMatch) {
    throw new createHttpError.BadRequest(
      'No class name found in the source code.',
    );
  }
  return classMatch[1];
}
