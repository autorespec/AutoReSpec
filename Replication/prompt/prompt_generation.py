import os
import random

from config import config

from utils.llm_wrapper import (
    create_llm_config,
    request_llm_engine,
    create_collaborative_llm_config,
    create_chatgpt_config,
    create_collaborative_gpt_llm_config,
    request_chatgpt_engine,
    create_claude_config,
    request_claude_engine,
    create_collaborative_claude_llm_config,
)
from utils.utils import file2str, check_file_read_access


def randomly_select_prompt(oracle_list, num, class_name):
    selected_list = random.sample(oracle_list, num)
    while class_name in selected_list:
        selected_list.remove(class_name)
        selected_list.append(random.choice(oracle_list))
    return selected_list


def read_oracle_as_msg(classname):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    filename_oracle = os.path.join(
        project_root, "oracle", "oracle", classname, f"{classname}.java"
    )
    filename_clean = os.path.join(
        project_root, "oracle", "oracle_clean", classname, f"{classname}.java"
    )
    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_INIT_PROMPT").replace(
            "{src_code}", file2str(filename_clean)
        ),
    }
    msg_reply = {
        "role": "assistant",
        "content": "```java\n{code}\n```".format(code=file2str(filename_oracle)),
    }
    return [msg_request, msg_reply]


def select_few_shot_prompts(
    input_code_path,
    class_name,
    messages,
    few_shot=4,
):
    check_file_read_access(input_code_path)
    print("retrieving random examples...")
    oracle_list = [
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
    ]

    random_class_names = randomly_select_prompt(oracle_list, few_shot, class_name)
    for class_name in random_class_names:
        messages.extend(
            read_oracle_as_msg(classname=class_name.split(".")[0])
        )
    return messages


def create_generation_prompt_config(
    model_name,
    input_code_path,
    class_name,
):
    # initial system message
    msg_base = {"role": "system", "content": config.get("system_message")}
    base_messages = [msg_base]

    input_code = file2str(input_code_path)

    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("few_shot", 4),

    )
    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_GENERATION_PROMPT").replace(
            "{src_code}", input_code
        ),
    }
    few_shot_included_messages.append(msg_request)
    return create_llm_config(model_name, few_shot_included_messages)


def create_chatgpt_generation_prompt_config(
    input_code_path,
    class_name,

):
    msg_base = {"role": "system", "content": config.get("system_message")}
    base_messages = [msg_base]

    input_code = file2str(input_code_path)

    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("few_shot", 4),

    )
    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_GENERATION_PROMPT").replace(
            "{src_code}", input_code
        ),
    }
    few_shot_included_messages.append(msg_request)
    return create_chatgpt_config(few_shot_included_messages)


def create_claude_generation_prompt_config(
    input_code_path,
    class_name,
):
    base_messages = []

    input_code = file2str(input_code_path)

    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("few_shot", 4),
    )
    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_GENERATION_PROMPT").replace(
            "{src_code}", input_code
        ),
    }
    few_shot_included_messages.append(msg_request)
    return create_claude_config(few_shot_included_messages)


def collaborator_llm_initial_prompt_generation(
    input_code_path,
    class_name,
    specified_code,
    err_info,
):
    msg_base = {"role": "system", "content": config.get("collaborator_system_message")}
    base_messages = [msg_base]

    ## TODO: there might be some issues!
    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("collaborator_few_shot", 4),

    )
    msg_request = {
        "role": "user",
        "content": config.get("collaborator_feedback_message")
        .replace("{specified_code}", specified_code)
        .replace("{err_info}", err_info),
    }

    few_shot_included_messages.append(msg_request)
    return create_collaborative_llm_config(few_shot_included_messages)


def gpt_collaborator_llm_initial_prompt_generation(
    input_code_path,
    class_name,
    specified_code,
    err_info,
):
    msg_base = {"role": "system", "content": config.get("collaborator_system_message")}
    base_messages = [msg_base]

    ## TODO: there might be some issues!
    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("collaborator_few_shot", 4),

    )
    msg_request = {
        "role": "user",
        "content": config.get("collaborator_feedback_message")
        .replace("{specified_code}", specified_code)
        .replace("{err_info}", err_info),
    }

    few_shot_included_messages.append(msg_request)
    return create_collaborative_gpt_llm_config(few_shot_included_messages)


def claude_collaborator_llm_initial_prompt_generation(
    input_code_path,
    class_name,
    specified_code,
    err_info,

):
    base_messages = []

    ## TODO: there might be some issues!
    few_shot_included_messages = select_few_shot_prompts(
        input_code_path,
        class_name,
        base_messages,
        config.get("collaborator_few_shot", 4),

    )
    msg_request = {
        "role": "user",
        "content": config.get("collaborator_feedback_message")
        .replace("{specified_code}", specified_code)
        .replace("{err_info}", err_info),
    }

    few_shot_included_messages.append(msg_request)
    return create_collaborative_claude_llm_config(few_shot_included_messages)


def gen_extra_guidance(err_info):
    if "visibility" in err_info:
        return 'To avoid errors related to visibility, you can add "spec_public" specifications to the member variables within the class.'
    elif "non-pure" in err_info:
        return 'To avoid errors related to non-pure methods, you can add "pure" specifications to the methods that don\'t modify any class members.'
    # elif "NegativeIndex" in err_info:
    #     return 'In case of "PossiblyNegativeIndex", you can add an "assume" specification to ensure that the index is either equal to 0 or greater than 0.'
    # elif "TooLargeIndex" in err_info:
    #     return 'In case of "PossiblyTooLargeIndex", you can add an "assume" specification to ensure that the index is less than the length of the array.'
    elif "ArithmeticOperationRange" in err_info and "negation" in err_info:
        return 'To avoid integer overflow in integer negation operation, you can add an "assume" specification BEFORE the related code, ensuring that the operand is greater than the minimal expressible value.'
    elif "overflow" in err_info:
        return 'To avoid integer overflow in arithmetic operations, you can add an "assume" specification to guarantee that the operation result is within the expressible range (smaller than the maximum value and greater than the minimum value).'
    elif "underflow" in err_info:
        return 'To avoid integer underflow in arithmetic operations, you can add an "assume" specification to guarantee that the operation result is within the expressible range (smaller than the maximum value and greater than the minimum value).'
    # elif "LoopInvariantBeforeLoop" in err_info:
    #     return 'The "LoopInvariantBeforeLoop" error indicates that the loop invariant you stated may be violated before entering the loop. You should consider modifying the corresponding "loop_invariant" or "maintaining" specifications.'
    ## generated by chatgpt
    # elif "LoopInvariantNotMaintained" in err_info:
    #     return 'The "LoopInvariantNotMaintained" error suggests that your loop invariant is violated during the loop execution. Check if your maintaining clause correctly describes properties that hold true at every iteration.'
    # elif "LoopInvariantNotInitiallyTrue" in err_info:
    #     return 'The "LoopInvariantNotInitiallyTrue" error means that the stated invariant is **not satisfied before the loop starts**. Verify that the initial values satisfy the invariant.'
    # elif "LoopVariantNonDecreasing" in err_info:
    #     return 'The "LoopVariantNonDecreasing" error means that the `decreases` clause does not strictly decrease with each loop iteration. Ensure that the termination condition is well-defined and reduces the variant correctly.'
    # elif "LoopMayNotTerminate" in err_info:
    #     return 'The "LoopMayNotTerminate" warning suggests that the loop may run indefinitely. Ensure that your loop variant decreases at each iteration and a valid termination condition exists.'
    elif "DivisionByZero" in err_info:
        return 'To prevent division by zero errors, add an "assume" or "requires" specification ensuring that the denominator is non-zero before performing the division.'
    elif "ArrayStoreException" in err_info:
        return "This error occurs when storing an incompatible value in an array. Ensure the stored values match the declared array type."
    # elif "NullPointerException" in err_info:
    #     return "To prevent null pointer exceptions, add a `requires a != null;` specification before accessing an array or object reference."
    elif (
        "Expected a declaration or a JML construct inside the JML annotation"
        in err_info
    ):
        return "This error suggests a **syntax issue** in a JML annotation. Ensure that `maintaining`, `ensures`, or `requires` statements are correctly structured."
    elif "not a statement" in err_info:
        return "This error means that the JML annotation is incorrectly written in a place where Java expects a **valid statement**. Make sure annotations are properly placed inside a method or loop block."
    elif "cannot be resolved" in err_info:
        return 'The error "cannot be resolved" suggests a variable or function is being referenced without being properly declared or imported. Ensure that all referenced variables exist in the current scope.'
    elif "Illegal start of expression" in err_info:
        return "This error often indicates an incorrectly formatted JML annotation. Check for misplaced or missing `//@` or `/*@ ... @*/` markers."
    elif "Type mismatch" in err_info:
        return "This error suggests that an operation involves incompatible types. Ensure that variables and expressions match the expected types."
    elif "Syntax error, insert" in err_info:
        return "This error suggests that a necessary **Java or JML keyword** is missing. Check for missing semicolons, brackets, or keywords like `requires` or `ensures`."
    elif "expected ';' " in err_info:
        return "JML specifications **do not** require semicolons (`;`) at the end of annotations. Remove the semicolon if it appears after `//@` or `/*@ ... @*/`."
    elif any(q in err_info for q in [r"\\num_of", r"\\sum", r"\\product"]):
        return r""" 
        To avoid the use of \\sum, \\num_of, and \\product quantifiers in your JML specifications, you can express your specifications using induction steps to help OpenJML's verifiers to reason about your code. You can do this by define mathematical functions and lemmas through model methods. 
        For example, you can should not use \\product quantifier in the following specifications:
        
        ```
        //@ requires 0 <= n && n <= 20;
        //@ ensures \\result >= 1 && \\result <= Long.MAX_VALUE;
        //@ ensures \\result == (\\product int i; 1 <= i && i <= n; i);
        public /*@ pure @*/ long factorial(int n)
        {
          int c;
          long fact = 1;
        
        if (n == 0) {         
          return fact;
          }
        
          //@ maintaining c >= 1 && c <= n+1;
          //@ maintaining fact > 0;
          //@ maintaining fact <= Long.MAX_VALUE; 
          //@ maintaining fact == (\\product int i; 1 <= i && i <= c; i);
          //@ decreases n - c;
              for (c = 1; c <= n; c++) { 
                    fact = fact*c;
                  }	 
        
              return fact;
          }
        ```
        Instead, you can define a model method `spec_factorial` to help OpenJML's verifiers to reason about your code. Here is an example of how you can define a model method to replace the \product quantifier in the factorial method:
        
        ```   
        //@ requires 0 <= n && n <= 20;
        //@ ensures \\result >= 1 && \\result <= Long.MAX_VALUE;
        //@ ensures \\result == spec_factorial(n);
          public /*@ pure @*/ long factorial(int n)
          {
            int c;
            long fact = 1;
        
        //@ assert spec_factorial(0) == 1;
        if (n == 0) {         
                  return fact;
        }
        
        //@ maintaining c >= 1 && c <= n+1;
        //@ maintaining fact > 0;
        //@ maintaining fact <= Long.MAX_VALUE; 
        //@ maintaining spec_factorial(c - 1) == fact;
        //@ decreases n - c;
            for (c = 1; c <= n; c++) { 
                  fact = fact*c;
                }	 
        
            return fact;
        }
        
        /*@ 	
        requires n > 0 && n <= 20;
          ensures 0 <= \\result && \\result <= Long.MAX_VALUE;
          ensures n > 0 ==> \\result == n * spec_factorial(n-1);
        also
          requires n == 0;
          ensures \\result == 1;
        public model static pure long spec_factorial(int n) { 
        if (n == 0) {
          return 1; 
        }
        else {
          assert n * spec_factorial(n-1) <= Long.MAX_VALUE;
          return n * spec_factorial(n-1);
        }
            }
        @*/
        }
        ```
        """
    elif any(q in err_info for q in [r"\\min,", r"\\max"]):
        return r"""
        To avoid the use of \\min and \\max quantifiers in your JML specifications, you can use the \\forall quantifier to express your specifications. 
        For example, you should not use \\max quantifier in the following specifications:

        ```
        /*@
        @ public normal_behavior
        @ requires a != null;
        @ ensures \\result >= (\\max int j; j >= 0 && j < a.length; a[j]);
        @*/
        public static /*@ pure @*/ int max(int[] a) {
            if (a.length == 0) return 0;
            int max = a[0], i = 1;
            /*@
            @ loop_invariant i >= 1 && i <= a.length;
            @ loop_invariant max >= (\\max int j; j >= 0 && j < i; a[j]);
            @ decreases a.length - i;
            @*/
            while (i < a.length) {
                if (a[i] > max) max = a[i];
                ++i;
            }
            return max;
        }
        ```
        Instead, you can use the \\forall quantifier to express the same specification without using \\max quantifier:

        ```
        /*@
        @ public normal_behavior
        @ requires a != null;
        @ ensures (\\forall int j; j >= 0 && j < a.length; \\result >= a[j]);
        @*/
        public static /*@ pure @*/ int max(int[] a) {
        if (a.length == 0) return 0;
        int max = a[0], i = 1;
        /*@
        @ loop_invariant i >= 1 && i <= a.length;
        @ loop_invariant (\\forall int j; j >= 0 && j < i; max >= a[j]);
        @ decreases a.length - i;
        @*/
        while (i < a.length) {
            if (a[i] > max) max = a[i];
            ++i;
        }
        return max;
        }
        """
    elif "LoopInvariant" in err_info:
        return r"""
                This error occurs when the loop invariant—a condition that must hold true before the loop begins and remain true after each iteration—is not properly established or maintained. This semantic error typically arises when verifiers fail to confirm the correctness of the synthesized loop invariant. The causes of this error include: (1) an incorrect loop invariant, (2) wrong/weak preconditions that prevent the invariant from holding at the start of the loop, or (3) incomplete reasoning about the loop, leading to insufficient information for the verifier to verify the invariant.
                To resolve the error, please consider the following steps:
        1. Carefully review the loop invariant to ensure it correctly captures the necessary conditions that hold true before and after each iteration of the loop.
        2. Carefully examine preconditions to ensure they are strong enough to establish the loop invariant at the beginning of the loop.
        3. Add additional assertions or assumptions within the loop to help the verifier reason about the loop invariant.

        For example, consider the following code snippet with a loop invariant failure:
        ```
        /*@ public normal_behaviour
        @   requires a != null && b != null;
        @   requires a != b;
        @   requires a.length == b.length;
        @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
        @   assignable b[*];
        @
        @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
        @*/
        public static void invert(int[] a, int[] b) {
            
            /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
            @  decreases a.length - i;
            @*/
            for(int i = 0; i < a.length; i++) {
                b[a[i]] = i;
            }
        }
        ```

        In this example, the loop invariant is correctly defined to ensure that the mapping between arrays a and b is established correctly. However, it lacks a precondition to guarantee that the elements of array a are unique, which is essential for the invariant to hold. To fix this issue, you can add a precondition to ensure the uniqueness of elements in array a as follows:

        ```
        /*@ public normal_behaviour
        @   requires a != null && b != null;
        @   requires a != b;
        @   requires a.length == b.length;
        @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
        @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
        @   assignable b[*];
        @
        @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
        @*/
        public static void invert(int[] a, int[] b) {
            
            /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
            @  decreases a.length - i;
            @*/
            for(int i = 0; i < a.length; i++) {
                b[a[i]] = i;
            }
        }
        ```
        """
    elif "postcondition" in err_info:
        return r"""
            This error occurs when the postcondition—a condition that must hold true after the execution of a program or function—is not satisfied. This type of semantic error typically arises when verifiers are unable to confirm that the program’s logic guarantees the postcondition under all valid inputs and scenarios. The causes of this error include: (1) an incorrect or incomplete postcondition, (2) wrong/weak preconditions that prevent the program from reaching a state where the postcondition holds, or (3) incomplete reasoning about the programs, leading to insufficient information for the verifier to verify the postcondition.
            To resolve the error, please consider the following steps:
            1. Review the postcondition to ensure it correctly captures the expected behavior of the program or function.
            2. Check the preconditions to ensure they are strong enough to reach a state where the postcondition holds.
            3. Add additional assertions or assumptions within the program or function to help the verifier reason about the postcondition.

            For example, consider the following code snippet with a postcondition failure:
            ```
            /*@ public normal_behaviour
            @   requires a != null && b != null;
            @   requires a != b;
            @   requires a.length == b.length;
            @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
            @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
            @   assignable b[*];
            @
            @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
            @*/
            public static void invert(int[] a, int[] b) {
                
                //@ decreases a.length - i;
                for(int i = 0; i < a.length; i++) {
                    b[a[i]] = i;
                }
            }
            ```

            In this example, the postcondition specifies that the array b should be the inverse of array a. However, verifiers failed to confirm this postcondition due to the lack of a proper loop invariant for reasoning about behaviors of loop. To fix this issue, you can add a loop invariant to ensure that the mapping between arrays a and b is correctly established as follows:

            ```
            /*@ public normal_behaviour
            @   requires a != null && b != null;
            @   requires a != b;
            @   requires a.length == b.length;
            @   requires (\\forall int x; 0 <= x && x < a.length; 0 <= a[x] && a[x] < a.length);
            @   requires (\\forall int x, y; 0 <= x && x < y && y < a.length; a[x] != a[y]); // New precondition for uniqueness
            @   assignable b[*];
            @
            @   ensures (\\forall int x; 0 <= x && x < b.length; b[a[x]] == x);
            @*/
            public static void invert(int[] a, int[] b) {
                
                /*@ loop_invariant 0 <= i && i <= a.length && (\\forall int x; 0 <= x && x < i; b[a[x]] == x);
                @  decreases a.length - i; 
                @*/
                for(int i = 0; i < a.length; i++) {
                    b[a[i]] = i;
                }
            }
            ```
                        """
    elif "overflow" in err_info:
        return """
                            This error occurs when arithmetic overflows cause computations to exceed the allowable range of values. 
            To resolve the error, you should consider the following steps:
            1. Review the arithmetic operations in your code to identify potential overflow scenarios.
            2. Use appropriate data types that can accommodate the expected range of values.
            3. Add explicit preconditions or assumptions to ensure that the inputs to arithmetic operations are within the valid range.

            For example, consider the following code snippet with an arithmetic operation range error:

            ```
            //@ ensures \\result == a + b;
            public static int add(int a, int b) {
                return a + b;
            }
            ```

            In this example, the postcondition specifies that the result of the `add` method should be equal to the sum of `a` and `b`. However, if the sum of `a` and `b` exceeds the range of `int`, an arithmetic overflow will occur, leading to incorrect results. To fix this issue, you can add explicit preconditions to ensure that the inputs to the `add` method are within the valid range as follows:

            ```
            //@ requires Integer.MIN_VALUE <= a + b && a + b <= Integer.MAX_VALUE; // Precondition to avoid arithmetic overflow
            //@ ensures \\result == a + b;
            public static int add(int a, int b) {
                return a + b;
            }
            ```
                """
    elif "NullPointer" in err_info:
        return r"""
                This error occurs when a null pointer is dereferenced, leading to undefined behavior or runtime failures. These issues typically arise due to the absence of preconditions ensuring the non-nullness of objects, such as arrays.
            
                To resolve the error, you should consider the following steps:
            1. Review the code to identify potential dereference of null pointers.
            2. Add explicit preconditions to ensure that objects are not null before dereferencing them.

            For example, consider the following code snippet with a null dereference error:

            ```
            //@ ensures \\result == a.length;
            public static int getLength(int[] a) {
                return a.length;
            }
            ```

            In this example, the postcondition specifies that the result of the `getLength` method should be equal to the length of the input array `a`. However, if `a` is null, dereferencing it to access its length will result in a null pointer dereference error. To fix this issue, you can add an explicit precondition to ensure that `a` is not null before accessing its length as follows:

            ```
            //@ requires a != null; // Precondition to ensure a is not null
            //@ ensures \\result == a.length;
            public static int getLength(int[] a) {
                return a.length;
            }
            ```
                    """
    elif "Index" in err_info:
        return r"""
        This error occurs when an array index exceeds its valid bounds, leading to potential runtime failures. These issues typically arise due to missing conditions or specifications regarding the array's length or the bounds of the index.
        To resolve the error, you should consider the following steps:
            1. Review the code to identify potential array index operations that could exceed the valid bounds.
            2. Add explicit preconditions or assertions to ensure that array indices are within the valid range.

            For example, consider the following code snippet with a too large index error:

            ```
            //@ ensures \\result == a[index];
            public static int getElement(int[] a, int index) {
                return a[index];
            }
            ```

            In this example, the postcondition specifies that the result of the `getElement` method should be equal to the element at the given index in the input array `a`. However, if the `index` exceeds the bounds of the array `a`, an array index out of bounds error will occur. To fix this issue, you can add an explicit precondition to ensure that the `index` is within the valid range before accessing the array element as follows:

            ```
            //@ requires a != null; // Precondition to ensure a is not null
            //@ requires 0 <= index && index < a.length; // Precondition to ensure index is within bounds
            //@ ensures \\result == a[index];
            public static int getElement(int[] a, int index) {
                return a[index];
            }
            ```

        """
    elif "Assert" in err_info:
        return r"""
            This error occurs when an assertion—a condition that must hold true at a specific point in the program—evaluates to false during execution. This type of error typically arises due to (1) incorrect assertions, (2) incomplete reasoning about program behavior, leading to insufficient information for the verifier to verify the assertions, or (3) insufficient preconditions that fail to guarantee the assertion. To resolve this issue, ensure that the assertion is correctly formulated and that all necessary conditions are met before reaching the assertion.

            To resolve the error, you should consider the following steps:
            1. Review the assertion to ensure it correctly captures the expected behavior of the program at that point.
            2. Check the preconditions to ensure they are strong enough to reach the assertion point.
            3. Add additional assertions or assumptions within the program to help the verifier reason about the assertion.

            For example, consider the following code snippet with an assertion failure:

            ```
            public static int calculate(int n) {
                if (n == 1 || n == 2) {
                    return 1;
                } else {
                    //@ assert n > 2;
                    return n * 5;
                }
            }
            ```

            In this example, the assertion specifies that `n` should be greater than 2. However, this assertions only hold if the input `n` is positive. To fix this issue, you can add a precondition to ensure that `n` is positive before reaching the assertion as follows:

            ```
            //@ requires n > 0; // Precondition to ensure n is positive
            public static int calculate(int n) {
                if (n == 1 || n == 2) {
                    return 1;
                } else {
                    //@ assert n > 2;
                    return n * 5;
                }
            }
            ```

                        """
    elif "divide by zero" in err_info.lower():
        return r"""
                    This error occurs when a division operation attempts to divide by zero, leading to undefined behavior. These issues typically arise due to missing or incomplete specifications on the values of variables. The root causes can vary and include insufficient preconditions, missing loop invariants, or the absence of assertions to enforce non-zero denominators.


                    To resolve the error, you should consider the following steps:
            1. Review the code to identify potential division operations that could result in division by zero.
            2. Add explicit preconditions or assertions to ensure that denominators are non-zero before performing division operations.

            For example, consider the following code snippet with a division by zero error:

            ```
            //@ ensures \\result == a / b;
            public static int divide(int a, int b) {
                return a / b;
            }
            ```

            In this example, the postcondition specifies that the result of the `divide` method should be equal to the division of `a` by `b`. However, if `b` is zero, a division by zero error will occur, leading to undefined behavior. To fix this issue, you can add an explicit precondition to ensure that `b` is non-zero before performing the division operation as follows:

            ```
            //@ requires b != 0; // Precondition to avoid division by zero
            //@ ensures \\result == a / b;
            public static int divide(int a, int b) {
                return a / b;
            }
            ```
                        """
    elif "large shift" in err_info.lower():
        return r"""
            To avoid large shift values, you should consider the following steps:
1. Review the code to identify potential shift expressions with large shift values.
2. Ensure that the shift values are within the valid range of 0 to 31 for 32-bit operations.
3. Use explicit preconditions, assertions or loop invariants to enforce the valid range of shift values.

For example, consider the following code snippet with a large shift value warning:

```
public static int calculate(int n) {
    int count = 0;
    for (int i = 0; i < 32; i++) {
        if (((n >> i) & 1) == 1) {
            count++;
        }
    }
    return count;
}
```

In this example, the code iterates over the bits of the input `n` using a shift operation. However, if the shift value `i` exceeds the valid range of 0 to 31, the behavior of the shift operation may not be as expected. To fix this issue, you can add an explicit loop invariant to help verify to reason that the shift values are within the valid range as follows:


```
public static int calculate(int n) {
    int count = 0;
    //@ loop_invariant 0 <= i && i < 32;
    for (int i = 0; i < 32; i++) {
        if (((n >> i) & 1) == 1) {
            count++;
        }
    }
    return count;
}
```
                            """
    elif "precondition" in err_info.lower():
        return r"""
        This error occurs when the precondition—a condition that must hold true before the execution of a program or function—is not satisfied. This type of semantic error typically arises when verifiers are unable to confirm that the program's logic guarantees the precondition under all valid inputs and scenarios. The causes of this error include: (1) an incorrect or incomplete precondition, (2) incomplete reasoning about the programs, leading to insufficient information for the verifier to verify the precondition, especially in recursive or mutually recursive methods.

                To resolve the error, you should consider the following steps:
1. Review the precondition to ensure it correctly captures the necessary conditions that must hold true before the program or function executes.
2. Check the program's logic to ensure it guarantees the precondition under all valid inputs and scenarios.
3. Add additional assertions or assumptions within the program or function to help the verifier reason about the precondition.

For example, consider the following code snippet with a precondition failure:

```
class Gcd {
    /*@ requires x > 0 || y > 0; 
      @*/
    public static int gcd(int x, int y) {
        if (y == 0) {
            return x;
        } else {
            return gcd(y, x % y);
        }
    }
}
```

In this example, the precondition specifies that either `x` or `y` should be greater than 0. However, the recursive call to the `gcd` method does not guarantee that the precondition holds for all valid inputs. To fix this issue, you need (1) add a precondition to ensure that both `x` and `y` are non-negative, and (2) add a assertion to ensure the recursive call satisfies the precondition as follows:

```
class Gcd {
    
    /*@ requires x >= 0 && y >= 0;
      @ requires x > 0 || y > 0; 
      @*/
    public static int gcd(int x, int y) {
        if (y == 0) {
            return x;
        } else {
            //@ assert y > 0;
            return gcd(y, x % y);
        }
    }
}
```
                                """
    elif "bad cast" in err_info.lower():
        return r"""
            This error occurs when an invalid cast operation is performed, leading to runtime failures or incorrect behavior. These issues typically arise from incorrect assumptions about the types of objects or variables being cast. 
To resolve the error, you should consider the following steps:
1. Review the code to identify potential cast operations that could result in invalid type conversions.
2. Ensure that the types being cast are compatible and that the cast operation is valid.
3. Add explicit preconditions or assertions to ensure that the cast operation is safe and correct.
                                    """
    elif "array assignment" in err_info.lower():
        return r"""
To resolve the error, you should consider the following steps:
1. Review the code to identify potential array assignments with mismatched types.
2. Add explicit preconditions or assertions to ensure that the assigned values match the expected data types.

For example, consider the following code snippet with a bad array assignment error:

```
class MyObjectArray {
    class Address {
        public int address;
        
        //@ ensures this.address == address;
        //@ pure
        public Address(int address) {
                this.address = address;
        }
    }
    
    //@ requires addresses != null;
    //@ requires addresses.length == 100;
    //@ ensures (\\forall int i; i >= 0 && i < 100; addresses[i] != null);
    public MyObjectArray(Address[] addresses) {
        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j] != null);
        for (int i = 0; i < 100; ++i) {
            addresses[i] = new Address(88);
        }

        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j].address == 99);
        for (int i = 0; i < 100; ++i) {
            addresses[i].address = 99;
        }
    }
}
```

In this example, each element of the addresses array is assigned an instance of the Address class. As a result, OpenJML must verify that the dynamic type of the right-hand side is a subclass of the element type of the dynamic type on the left-hand side. To address this issue, you can include a precondition to ensure that the Address class is a subclass of the element type of the addresses array, as shown below:

```
class MyObjectArray {
    class Address {
        public int address;
        
        //@ ensures this.address == address;
        //@ pure
        public Address(int address) {
                this.address = address;
        }
    }
    
    //@ requires addresses != null;
    //@ requires addresses.length == 100;
    //@ requires \\type(Address) <: \\elemtype(\\typeof(addresses)); // Precondition to ensure Address is a subclass of the element type
    //@ ensures (\\forall int i; i >= 0 && i < 100; addresses[i] != null);
    public MyObjectArray(Address[] addresses) {
        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j] != null);
        for (int i = 0; i < 100; ++i) {
            addresses[i] = new Address(88);
        }

        //@ maintaining i >= 0 && i <= 100;
        //@ decreasing 100 - i;
        //@ maintaining (\\forall int j; j >=0 && j < i; addresses[j].address == 99);
        for (int i = 0; i < 100; ++i) {
            addresses[i].address = 99;
        }
    }
}
```
    """
    else:
        return ""


def read_refine_as_msg(dirname):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    dirpath = os.path.join(project_root, "oracle", "refine", dirname)
    original_code = file2str(os.path.join(dirpath, "original"))
    err_info = file2str(os.path.join(dirpath, "err_info"))
    refined_code = file2str(os.path.join(dirpath, "refined"))
    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_REFINEMENT_PROMPT")
        .replace("{specified_code}", original_code)
        .replace("{err_info}", err_info),
    }
    msg_reply = {
        "role": "assistant",
        "content": "```java\n{code}\n```".format(code=refined_code),
    }
    msg_request["content"] += gen_extra_guidance(err_info)
    return [msg_request, msg_reply]


def extract_err_type(err_info):
    prompt_list = []
    keyword_dict = {
        "DivideByZero": "divide_by_zero",
        "visibility": "private_visibility",
        "NegativeIndex": "negative_index",
        "TooLargeIndex": "too_large_index",
        "ArithmeticOperationRange negation": "overflow_negation",
        "overflow sum": "overflow_sum",
        "overflow difference": "overflow_sub",
        "overflow multiply": "overflow_mul",
        "overflow divide": "overflow_div",
        "underflow sum": "underflow_sum",
        "underflow difference": "underflow_sub",
        "underflow multiply": "underflow_mul",
        "underflow divide": "underflow_div",
    }
    for key in keyword_dict:
        keyword_list = key.split(" ")
        flag_all_in = True
        for keyword in keyword_list:
            if err_info.find(keyword) == -1:
                flag_all_in = False
                break
        if flag_all_in:
            prompt_list.append(keyword_dict[key])
    return prompt_list


def create_specialized_patcher_prompt_config(
    model_name, original_code, err_info, collaborate=False, gpt=False, claude=False
):
    """return the config file with refinement prompts"""
    print("retrieving refined prompts ...")

    msg_base = {"role": "system", "content": config.get("system_message")}
    messages = [msg_base]

    prompt_list = extract_err_type(err_info)

    for dirname in prompt_list:
        messages.extend(read_refine_as_msg(dirname))

    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_REFINEMENT_PROMPT")
        .replace("{specified_code}", original_code)
        .replace("{err_info}", err_info),
    }
    msg_request["content"] += gen_extra_guidance(err_info)
    messages.append(msg_request)

    # TODO: collaborative and gpt or claude issue, here!
    if collaborate:
        llm_config = create_collaborative_llm_config(messages)
    elif gpt:
        llm_config = create_chatgpt_config(messages)
    elif claude:
        llm_config = create_claude_config(messages)
    else:
        llm_config = create_llm_config(model_name, messages)
    return llm_config


def create_specialized_claude_patcher_prompt_config(
    original_code, err_info,
):
    """return the config file with refinement prompts"""
    print("retrieving refined prompts ...")

    messages = []

    prompt_list = extract_err_type(err_info)

    for dirname in prompt_list:
        messages.extend(read_refine_as_msg(dirname))

    msg_request = {
        "role": "user",
        "content": config.get("FORMAT_REFINEMENT_PROMPT")
        .replace("{specified_code}", original_code)
        .replace("{err_info}", err_info),
    }
    msg_request["content"] += gen_extra_guidance(err_info)
    messages.append(msg_request)

    return create_claude_config(messages)


def provide_good_feedback(llm_config, f_log):
    print("providing good feedback ...")
    good_feedback = {"role": "user", "content": config.get("good_feedback_prompt")}
    llm_config["messages"] = [good_feedback]
    ret = request_llm_engine(llm_config)
    content = ret.message.content
    print(content)
    f_log.write(f"{'*' * 8} positive feedback {'*' * 8}\n")
    f_log.write(f"\n{content}")
    return content


def provide_good_feedback_gpt(llm_config, f_log):
    print("providing good feedback ...")
    good_feedback = {"role": "user", "content": config.get("good_feedback_prompt")}
    llm_config["messages"] = [good_feedback]
    ret = request_chatgpt_engine(llm_config)
    content = ret.choices[0].message.content
    print(content)
    f_log.write(f"{'*' * 8} positive feedback {'*' * 8}\n")
    f_log.write(f"\n{content}")
    return content


def provide_good_feedback_claude(llm_config, f_log):
    print("providing good feedback ...")
    good_feedback = {"role": "user", "content": config.get("good_feedback_prompt")}
    llm_config["messages"] = [good_feedback]
    ret = request_claude_engine(llm_config)
    content = ret.content[0].text
    print(content)
    f_log.write(f"{'*' * 8} positive feedback {'*' * 8}\n")
    f_log.write(f"\n{content}")
    return content
