import time


def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)  # Run function (which calls external LLM or Validator)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    return result, execution_time
