export const config = {
  openJML: {
    max_warning: 1,
    prover: "z3",
    validator_timeout: 180, // in seconds
  },
  ollamaOptions: {
    options: {
      temperature: 0.4,
    },
    stream: false,
  },
  groundTruth: [
    "AddLoop",
    "BinarySearch",
    "BubbleSort",
    "CopyArray",
    "Factorial",
    "FIND_FIRST_IN_SORTED",
    "FindFirstZero",
    "Inverse",
    "LinearSearch",
    "OddEven",
    "Perimeter",
    "SetZero",
    "Smallest",
    "StrPalindrome",
    "TransposeMatrix",
  ],
};
