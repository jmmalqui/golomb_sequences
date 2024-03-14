"""
Golomb Sequence
https://www.codewars.com/kata/5d06938fcac0a5001307ce57/train/python

"""

from functools import reduce
from itertools import count
from math import floor


class Iterable:
    def __init__(self, fn) -> None:
        self.fn = fn

    def __iter__(self):
        return self.fn()


iterable = lambda *fns: Iterable(
    lambda: (reduce(lambda z, fn: lambda v: fn(z(v)), fns)(i) for i in count(0))
)

identity = lambda x: x
plus = lambda v: lambda w: v + w
times = lambda v: lambda w: v * w
exp = lambda v: lambda w: v**w
triangle = lambda x: x * (x + 1) // 2
square = lambda x: x * x


def input_integer_holds_relation_with_output(output: list[int], idx: int):
    if len(output) == 0:
        return False
    return idx < len(output)


def golomb(given, n):
    input_list: list[int] = []
    output_list: list[int] = []
    queue: dict[int, int] = {}

    idx = 0
    wait = False

    for input_integer in given:
        input_list.append(input_integer)
        if not input_integer_holds_relation_with_output(output_list, idx):
            if input_integer == 0:
                output_list.append(1)
                queue[input_integer] = 1
                wait = True
            elif wait:
                output_list[idx - 1] = input_integer
                queue[input_list[idx - 1]] = output_list[idx - 1] - output_list.count(
                    input_list[idx - 1]
                )
                wait = False
                if input_list[idx - 1] in queue and input_list[idx - 1] != 0:
                    output_list.append(input_list[idx - 1])
                    queue[input_list[idx - 1]] -= 1
                else:
                    output_list.append(input_integer)
                    queue[input_integer] = output_list[idx] - output_list.count(
                        input_integer
                    )
                    if output_list.count(input_integer) > output_list[idx]:
                        wait = True
            elif len(queue) != 0 and not wait:
                smallest_integer_on_queue = min(queue.keys())
                for times in range(queue[smallest_integer_on_queue]):
                    output_list.append(smallest_integer_on_queue)
                queue[input_integer] = output_list[idx]
                del queue[smallest_integer_on_queue]
            else:
                for times in range(input_integer):
                    output_list.append(input_integer)
        else:
            if len(queue) == 0:
                for times in range(output_list[idx]):
                    output_list.append(input_integer)
            else:
                smallest_integer_on_queue = min(queue.keys())
                for times in range(queue[smallest_integer_on_queue]):
                    output_list.append(smallest_integer_on_queue)
                queue[input_integer] = output_list[idx]
                del queue[smallest_integer_on_queue]

        idx += 1
        to_delete = []
        for key in queue.keys():
            if queue[key] == 0:
                to_delete.append(key)

        for key in to_delete:
            del queue[key]

        if len(output_list) > n:
            break
    return output_list[:n]


def assert_equals(val1, val2):
    print("Passed" if val1 == val2 else "Failed")
    return val1 == val2


assert_equals(
    tuple(golomb(iterable(plus(1)), 20)),
    (1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8),
)


assert_equals(
    tuple(golomb(iterable(exp(2)), 20)),
    (1, 2, 2, 4, 4, 8, 8, 8, 8, 16, 16, 16, 16, 32, 32, 32, 32, 32, 32, 32),
)


assert_equals(
    tuple(golomb(iterable(plus(1), triangle), 20)),
    (1, 3, 3, 3, 6, 6, 6, 10, 10, 10, 15, 15, 15, 15, 15, 15, 21, 21, 21, 21),
)


assert_equals(
    tuple(golomb(iterable(plus(1), square), 20)),
    (1, 4, 4, 4, 4, 9, 9, 9, 9, 16, 16, 16, 16, 25, 25, 25, 25, 36, 36, 36),
)


assert_equals(
    tuple(golomb(iterable(plus(1), times(2)), 20)),
    (2, 2, 4, 4, 6, 6, 6, 6, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 12, 12),
)


assert_equals(
    tuple(golomb(iterable(plus(1), times(3)), 20)),
    (3, 3, 3, 6, 6, 6, 9, 9, 9, 12, 12, 12, 12, 12, 12, 15, 15, 15, 15, 15),
)


assert_equals(
    tuple(golomb(iterable(plus(1), times(4)), 20)),
    (4, 4, 4, 4, 8, 8, 8, 8, 12, 12, 12, 12, 16, 16, 16, 16, 20, 20, 20, 20),
)


assert_equals(
    tuple(golomb(iterable(identity), 20)),
    (1, 2, 1, 0, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7),
)


assert_equals(
    tuple(golomb(iterable(plus(-1), exp(2), floor), 20)),
    (1, 2, 1, 0, 8, 8, 8, 8, 8, 8, 8, 8, 16, 16, 16, 16, 16, 16, 16, 16),
)


assert_equals(
    tuple(golomb(iterable(triangle), 20)),
    (1, 3, 1, 0, 1, 10, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 21, 21, 21, 21),
)


assert_equals(
    tuple(golomb(iterable(square), 20)),
    (1, 4, 1, 0, 1, 1, 16, 25, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36),
)


assert_equals(
    tuple(golomb(iterable(times(2)), 20)),
    (2, 2, 0, 0, 8, 8, 8, 8, 8, 8, 8, 8, 10, 10, 10, 10, 10, 10, 10, 10),
)


assert_equals(
    tuple(golomb(iterable(times(3)), 20)),
    (3, 3, 0, 0, 0, 3, 15, 15, 15, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18),
)


assert_equals(
    tuple(golomb(iterable(times(4)), 20)),
    (4, 4, 0, 0, 0, 0, 4, 4, 24, 24, 24, 24, 28, 28, 28, 28, 32, 32, 32, 32),
)
