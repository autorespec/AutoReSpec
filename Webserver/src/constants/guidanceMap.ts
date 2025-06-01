import {
  ARRAY_ASSIGNMENT_GUIDANCE,
  ASSERT_GUIDANCE,
  BAD_CAST_GUIDANCE,
  DIVIDE_BY_ZERO_GUIDANCE,
  INDEX_GUIDANCE,
  LARGE_SHIFT_GUIDANCE,
  LOOP_INVARIANT,
  MIN_MAX_QUANTIFIER,
  NULL_POINTER_GUIDANCE,
  OVERFLOW_GUIDANCE,
  POSTCONDITION_GUIDANCE,
  PRECONDITION_GUIDANCE,
  QUANTIFIER_GUIDANCE,
} from './guidanceSnippets';

type MatchRule = {
  match: string[] | ((err: string) => boolean);
  guidance: string;
};
export const guidanceMap: MatchRule[] = [
  {
    match: ['visibility'],
    guidance: `To avoid errors related to visibility, you can add "spec_public" specifications to the member variables within the class.`,
  },
  {
    match: ['non-pure'],
    guidance: `To avoid errors related to non-pure methods, add "pure" specifications to methods that do not modify class state.`,
  },
  {
    match: ['ArithmeticOperationRange', 'negation'],
    guidance: `To avoid integer overflow in integer negation operation, you can add an "assume" specification BEFORE the related code, ensuring that the operand is greater than the minimal expressible value.`,
  },
  {
    match: ['overflow'],
    guidance: `To avoid integer overflow in arithmetic operations, you can add an "assume" specification to guarantee that the operation result is within the expressible range (smaller than the maximum value and greater than the minimum value).`,
  },
  {
    match: ['underflow'],
    guidance: `To avoid integer underflow in arithmetic operations, you can add an "assume" specification to guarantee that the operation result is within the expressible range (smaller than the maximum value and greater than the minimum value).`,
  },
  {
    match: ['DivisionByZero'],
    guidance: `To prevent division by zero errors, add an "assume" or "requires" specification ensuring that the denominator is non-zero before performing the division.`,
  },
  {
    match: ['ArrayStoreException'],
    guidance: `This error occurs when storing an incompatible value in an array. Ensure the stored values match the declared array type.`,
  },
  {
    match: [
      'Expected a declaration or a JML construct inside the JML annotation',
    ],
    guidance:
      'This error suggests a **syntax issue** in a JML annotation. Ensure that ```maintaining```, ```ensures```, or ```requires``` statements not correctly structured.',
  },
  {
    match: ['not a statement'],
    guidance:
      'This error means that the JML annotation is incorrectly written in a place where Java expects a **valid statement**. Make sure annotations are properly placed inside a method or loop block.',
  },
  {
    match: ['cannot be resolved'],
    guidance:
      'The error "cannot be resolved" suggests a variable or function is being referenced without being properly declared or imported. Ensure that all referenced variables exist in the current scope.',
  },
  {
    match: ['Illegal start of expression'],
    guidance:
      'This error often indicates an incorrectly formatted JML annotation. Check for misplaced or missing `//@` or `/*@ ... @*/` markers.',
  },
  {
    match: ['Type mismatch'],
    guidance:
      'This error suggests that an operation involves incompatible types. Ensure that variables and expressions match the expected types.',
  },
  {
    match: ['Syntax error'],
    guidance:
      'This error suggests that a necessary **Java or JML keyword** is missing. Check for missing semicolons, brackets, or keywords like `requires` or `ensures`.',
  },
  {
    match: [`expected ';'`],
    guidance:
      'JML specifications **do not** require semicolons (`;`) at the end of annotations. Remove the semicolon if it appears after `//@` or `/*@ ... @*/`.',
  },
  {
    match: [`catastrophic JML internal error`],
    guidance:
      'The specification creates catastrophic JML internal error. Avoid double rewriting of ident',
  },
  {
    match: (err) =>
      ['\\sum', '\\num_of', '\\product'].some((kw) => err.includes(kw)),
    guidance: QUANTIFIER_GUIDANCE,
  },
  {
    match: (err) => ['\\min,', '\\max'].some((kw) => err.includes(kw)),
    guidance: MIN_MAX_QUANTIFIER,
  },
  {
    match: [`LoopInvariant`],
    guidance: LOOP_INVARIANT,
  },
  {
    match: [`overflow`],
    guidance: OVERFLOW_GUIDANCE,
  },
  {
    match: [`postcondition`],
    guidance: POSTCONDITION_GUIDANCE,
  },
  {
    match: [`NullPointer`],
    guidance: NULL_POINTER_GUIDANCE,
  },
  {
    match: [`Index`],
    guidance: INDEX_GUIDANCE,
  },
  {
    match: [`Assert`],
    guidance: ASSERT_GUIDANCE,
  },
  {
    match: [`divide by zero`],
    guidance: DIVIDE_BY_ZERO_GUIDANCE,
  },
  {
    match: [`large shift`],
    guidance: LARGE_SHIFT_GUIDANCE,
  },
  {
    match: [`precondition`],
    guidance: PRECONDITION_GUIDANCE,
  },
  {
    match: [`array assignment`],
    guidance: ARRAY_ASSIGNMENT_GUIDANCE,
  },
];
// catastrophic JML internal error occurred.
