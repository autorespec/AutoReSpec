export const refinementExamples = [
  {
    tag: 'divide_by_zero',
    errorInfo:
      'Div.java:5: verify: verify: The prover cannot establish an assertion (PossiblyDivideByZero) in method calculate\n\t\treturn x / y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\treturn x / y;\n\t}\n}',
    refined:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\t//@ assume y != 0;\n\t\treturn x / y;\n\t}\n}',
  },
  {
    tag: 'negative_index',
    errorInfo:
      'MyArray.java:8: verify: The prover cannot establish an assertion (PossiblyNegativeIndex) in method MyArray\n\t\t\tarr[i] = 0;\n\n1 error',
    original:
      'public class MyArray {\n\tprivate /*@ spec_public @*/ int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
    refined:
      'public class MyArray {\n\tprivate /*@ spec_public @*/ int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\t//@ assume 0 <= i && i < arr.length;\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
  },
  {
    tag: 'overflow_div',
    errorInfo:
      'Div.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Div: overflow in int divide\n\t\treturn x / y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\treturn x / y;\n\t}\n}',
    refined:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\t//@ assume x / y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x / y;\n\t\treturn x / y;\n\t}\n}',
  },
  {
    tag: 'overflow_mul',
    errorInfo:
      'Mul.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Mul: int multiply overflow\n\t\treturn x * y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Mul {\n\t//@ ensures \\result == x * y;\n\tpublic int Mul(int x, int y) {\n\t\treturn x * y;\n\t}\n}',
    refined:
      'public class Mul {\n\t//@ ensures \\result == x * y;\n\tpublic int Mul(int x, int y) {\n\t\t//@ assume x * y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x * y;\n\t\treturn x + y;\n\t}\n}',
  },
  {
    tag: 'overflow_negation',
    errorInfo:
      'Neg.java:4: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Absolute: int negation\n\t\treturn -num;\n\t\t       ^\n1 verification failure',
    original:
      'public class Neg {\n\t//@ ensures \\result == -num;\n\tpublic int Negation(int num) {\n\t\treturn -num;\n\t}\n}',
    refined:
      'public class Neg {\n\t//@ ensures \\result == -num;\n\tpublic int Negation(int num) {\n\t\t//@ assume num > Integer.MIN_VALUE;\n\t\treturn -num;\n\t}\n}',
  },
  {
    tag: 'overflow_sub',
    errorInfo:
      'Sub.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Sub: overflow in int difference\n\t\treturn x - y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Sub {\n\t//@ ensures \\result == x - y;\n\tpublic int Sub(int x, int y) {\n\t\treturn x - y;\n\t}\n}',
    refined:
      'public class Sub {\n\t//@ ensures \\result == x - y;\n\tpublic int Sub(int x, int y) {\n\t\t//@ assume x - y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x - y;\n\t\treturn x - y;\n\t}\n}',
  },
  {
    tag: 'overflow_sum',
    errorInfo:
      'Add.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Add: overflow in int sum\n\t\treturn x + y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Add {\n\t//@ ensures \\result == x + y;\n\tpublic int Add(int x, int y) {\n\t\treturn x + y;\n\t}\n}',
    refined:
      'public class Add {\n\t//@ ensures \\result == x + y;\n\tpublic int Add(int x, int y) {\n\t\t//@ assume x + y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x + y;\n\t\treturn x + y;\n\t}\n}',
  },
  {
    tag: 'private_visibility',
    errorInfo:
      'MyArray.java:4: error: An identifier with private visibility may not be used in a ensures clause with package visibility\n\t//@ ensures (\\forall int i; 0 <= i && i < 10; arr[i] == 0);\n\t                                              ^\n1 error',
    original:
      'public class MyArray {\n\tprivate int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\t//@ assume i >= 0;\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
    refined:
      'public class MyArray {\n\tprivate /*@ spec_public @*/ int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\t//@ assume i >= 0;\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
  },
  {
    tag: 'too_large_index',
    errorInfo:
      'MyArray.java:8: verify: The prover cannot establish an assertion (PossiblyTooLargeIndex) in method MyArray\n\t\t\tarr[i] = 0;\n\n1 error',
    original:
      'public class MyArray {\n\tprivate /*@ spec_public @*/ int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
    refined:
      'public class MyArray {\n\tprivate /*@ spec_public @*/ int arr[];\n\t\n\t//@ ensures (\\forall int i; 0 <= i && i < 5; arr[i] == 0);\n\tMyArray(){\n\t\tarr = new int[5];\n\t\tint i;\n\t\t//@ maintaining (\\forall int j; 0 <= j && j < i; arr[j] == 0);\n\t\tfor(i = 0; i < 5; i++) {\n\t\t\t//@ assume 0 <= i && i < arr.length;\n\t\t\tarr[i] = 0;\n\t\t}\n\t}\n}',
  },
  {
    tag: 'underflow_div',
    errorInfo:
      'Div.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Div: overflow in int divide\n\t\treturn x / y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\treturn x / y;\n\t}\n}',
    refined:
      'public class Div {\n\t//@ ensures \\result == x / y;\n\tpublic int Div(int x, int y) {\n\t\t//@ assume x / y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x / y;\n\t\treturn x / y;\n\t}\n}',
  },
  {
    tag: 'underflow_mul',
    errorInfo:
      'Mul.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Mul: int multiply underflow\n\t\treturn x * y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Mul {\n\t//@ ensures \\result == x * y;\n\tpublic int Mul(int x, int y) {\n\t\treturn x * y;\n\t}\n}',
    refined:
      'public class Mul {\n\t//@ ensures \\result == x * y;\n\tpublic int Mul(int x, int y) {\n\t\t//@ assume x * y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x * y;\n\t\treturn x + y;\n\t}\n}',
  },
  {
    tag: 'underflow_sub',
    errorInfo:
      'Sub.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Sub: underflow in int difference\n\t\treturn x - y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Sub {\n\t//@ ensures \\result == x - y;\n\tpublic int Sub(int x, int y) {\n\t\treturn x - y;\n\t}\n}',
    refined:
      'public class Sub {\n\t//@ ensures \\result == x - y;\n\tpublic int Sub(int x, int y) {\n\t\t//@ assume x - y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x - y;\n\t\treturn x - y;\n\t}\n}',
  },
  {
    tag: 'underflow_sum',
    errorInfo:
      'Add.java:5: verify: The prover cannot establish an assertion (ArithmeticOperationRange) in method Add: underflow in int sum\n\t\treturn x + y;\n\t\t         ^\n1 verification failure',
    original:
      'public class Add {\n\t//@ ensures \\result == x + y;\n\tpublic int Add(int x, int y) {\n\t\treturn x + y;\n\t}\n}',
    refined:
      'public class Add {\n\t//@ ensures \\result == x + y;\n\tpublic int Add(int x, int y) {\n\t\t//@ assume x + y <= Integer.MAX_VALUE && Integer.MIN_VALUE <= x + y;\n\t\treturn x + y;\n\t}\n}',
  },
];
