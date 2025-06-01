import { existsSync, mkdirSync } from 'fs';

export function createFolderIfNotExist(path: string): void {
  if (!existsSync(path)) {
    mkdirSync(path, { recursive: true });
  }
}
