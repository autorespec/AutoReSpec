export const parseCodeBlock = (content: string) => {
  const parts = content.split('```');
  if (parts.length < 2) {
    throw new Error('No code block found.');
  }

  let extracted = parts[1];

  if (extracted.trimStart().startsWith('java')) {
    extracted = extracted.trimStart().slice(4); // remove first 4 characters (java)
  }
  return extracted.trim();
};
