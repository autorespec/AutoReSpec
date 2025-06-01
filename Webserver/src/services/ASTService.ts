// @ts-nocheck

const { parse } = require('java-parser');

function walkAST(node, path = [], loops = [], branches = []) {
  if (!node || typeof node !== 'object') return;

  const currentPath = [...path, node];

  if (node.forStatement || node.whileStatement || node.doStatement) {
    loops.push(currentPath);
  }

  if (node.ifStatement || node.switchStatement || node.ifThenElseStatement) {
    branches.push(currentPath);
  }

  if (hasTernaryOperator(node)) {
    branches.push(currentPath);
  }

  for (const key in node) {
    const value = node[key];
    if (Array.isArray(value)) {
      value.forEach((child) => walkAST(child, currentPath, loops, branches));
    } else if (typeof value === 'object') {
      walkAST(value, currentPath, loops, branches);
    }
  }
}

function isSubpath(parent, child) {
  return parent.every((val, idx) => child[idx] === val);
}

function classifyProgramType(javaCode) {
  let cst;
  try {
    cst = parse(javaCode);
    logNodeTypes(cst);
  } catch (err) {
    return `Parse Error: ${err.message}`;
  }

  const loops = [];
  const branches = [];

  walkAST(cst, [], loops, branches);

  if (loops.length === 0 && branches.length === 0) return 'Sequential';
  if (branches.length > 0 && loops.length === 0) return 'Branched';

  for (let i = 0; i < loops.length; i++) {
    for (let j = 0; j < loops.length; j++) {
      if (
        i !== j &&
        loops[j].length > loops[i].length &&
        isSubpath(loops[i], loops[j])
      ) {
        return 'Nested Loop';
      }
    }
  }

  for (const loopPath of loops) {
    for (const branchPath of branches) {
      if (isSubpath(loopPath, branchPath)) {
        return 'Multi-path Loop';
      }
    }
  }

  return 'Single-path Loop';
}

function logNodeTypes(cst) {
  const seen = new Set();

  function walk(node) {
    if (!node || typeof node !== 'object') return;

    if (node.name && !seen.has(node.name)) {
      seen.add(node.name);
    }

    for (const key in node) {
      const val = node[key];
      if (Array.isArray(val)) {
        val.forEach((child) => walk(child));
      } else if (typeof val === 'object') {
        walk(val);
      }
    }
  }

  walk(cst);
}

function hasTernaryOperator(node) {
  if (!node || typeof node !== 'object') return false;

  const stack = [node];

  while (stack.length > 0) {
    const current = stack.pop();

    if (current && typeof current === 'object') {
      if (current.image === '?') return true;
      if (current.image === ':') return true;

      for (const key in current) {
        const value = current[key];
        if (value && typeof value === 'object') {
          stack.push(value);
        }
      }
    }
  }

  return false;
}

export { classifyProgramType };
