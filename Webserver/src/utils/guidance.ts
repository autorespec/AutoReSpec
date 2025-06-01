import { guidanceMap } from '../constants/guidanceMap';

export const generateGuidanceFromError = (errInfo: string): string => {
  console.log('generate guidance error was called');
  errInfo = errInfo.toLowerCase();
  for (const rule of guidanceMap) {
    if (typeof rule.match === 'function') {
      if (rule.match(errInfo)) return rule.guidance;
    } else {
      const matches = rule.match.every((kw) =>
        errInfo.includes(kw.toLocaleLowerCase()),
      );
      if (matches) return rule.guidance;
    }
  }
  return '';
};
