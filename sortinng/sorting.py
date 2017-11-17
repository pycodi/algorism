import random
import threading
import copy
import itertools
import datetime
import time


INPUT = [random.randint(pow(2, 2), pow(2, 10)) for i in range(2000)]


def taimer(f):

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = f(*args, **kwargs)
        t2 = time.time()
        print('Result {} seconds'.format(t2 -t1))
        return result
    return wrapper


def output(lst):
    return "{}...".format(lst[:30])


@taimer
def bubble_sort(lst):
    """ Сортировка пузырьком """
    sorted_ = False
    while not sorted_:
        sorted_ = True
        for i in range(len(lst)-1):
            if lst[i] > lst[i+1]:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                sorted_ = False
    return lst


@taimer
def quick_sort(lst):
    """ Быстрая сортировка """
    point = random.randint(0, len(lst)-1)
    left_side = []
    right_side = []
    result = []
    for i, v in enumerate(lst):
        if v < lst[point]:
            left_side.append(v)
        if v > lst[point]:
            right_side.append(v)

    def _bubble(side_list):
        sorted_ = False
        while not sorted_:
            sorted_ = True
            for i in range(len(side_list) - 1):
                if side_list[i] > side_list[i + 1]:
                    side_list[i], side_list[i + 1] = side_list[i + 1], side_list[i]
                    sorted_ = False
        result.append(side_list)
        return result

    t1 = threading.Thread(target=_bubble, args=(left_side, ))
    t1.start()
    t2 = threading.Thread(target=_bubble, args=(right_side, ))
    t2.start()
    t1.join()
    t2.join()
    del left_side
    del right_side
    return list(itertools.chain(*result))

if __name__ == '__main__':
    print(output(bubble_sort(INPUT)))
    print(output(quick_sort(INPUT)))