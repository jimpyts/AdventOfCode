from functools import wraps
import time
import re


def time_it(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_elapsed = end_time - start_time
        print(f"fn {func.__name__} took: {time_elapsed:.2f} sec")
        return result

    return wrap


def get_input(filename, *separators, data_type=str):
    """
    :type filename: str
    :type data_type: type
    :type separators: str
    """
    assert type(data_type) is type
    with open(filename) as f:
        data = f.read()
        for separator in separators:
            if type(data) is str:
                if len(separators) == 1:
                    data = [data_type(i) for i in data.split(separator) if i]
                else:
                    data = [i for i in data.split(separator) if i]
            else:
                data = [[data_type(i) for i in sub_data.split(separator) if i] for sub_data in data if sub_data]
        return data
