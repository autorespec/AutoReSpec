export const recommendLLM = [
  {
    programType: 'Branched',
    primaryLLM: { model: 'gemma3:27b', shot_count: 2 },
    collaborativeLLM: { model: 'claude-3-7-sonnet-20250219', shot_count: 4 },
  },
  {
    programType: 'Sequential',
    primaryLLM: { model: 'gemma3:27b', shot_count: 2 },
    collaborativeLLM: { model: 'gpt-4o', shot_count: 2 },
  },
  {
    programType: 'Single-path Loop',
    primaryLLM: { model: 'llama3:8b', shot_count: 2 },
    collaborativeLLM: { model: 'gpt-4o', shot_count: 4 },
  },
  {
    programType: 'Multi-path Loop',
    primaryLLM: { model: 'llama3:8b', shot_count: 2 },
    collaborativeLLM: { model: 'gpt-4o', shot_count: 4 },
  },
  {
    programType: 'Nested Loop',
    primaryLLM: { model: 'llama3:8b', shot_count: 2 },
    collaborativeLLM: { model: 'claude-3-7-sonnet-20250219', shot_count: 4 },
  },
  {
    programType: 'default',
    primaryLLM: { model: 'llama3:8b', shot_count: 2 },
    collaborativeLLM: { model: 'gpt-4o', shot_count: 4 },
  },
];
