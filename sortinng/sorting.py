import multiprocessing.pool as mpp
import random
import threading
import itertools
import time
from gevent.monkey import patch_all
import gevent

patch_all(thread=False)


INPUT = list(random.randint(pow(2, 2), pow(2, 10)) for i in range(3000))


def taimer(f):

    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = f(*args, **kwargs)
        t2 = time.time()
        print('Result for {}: {} seconds'.format(f.__name__, t2 -t1))
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

    t1 = threading.Thread(target=_bubble, args=(left_side, ))
    t1.start()
    t2 = threading.Thread(target=_bubble, args=(right_side, ))
    t2.start()
    t1.join()
    t2.join()
    del left_side
    del right_side
    return list(itertools.chain(*result))


@taimer
def quick_sort_gevent(lst):
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

    g1 = gevent.spawn(_bubble, left_side)
    g2 = gevent.spawn(_bubble, right_side)
    gevent.joinall([g1, g2])
    del left_side
    del right_side
    return list(itertools.chain(*result))

@taimer
def insert_sort(lst):
    """ Сортировка вставкой """
    for i in range(1, len(lst)):
        key = lst[i]
        point = i-1
        while point >= 0 and key < lst[point]:
            lst[point+1] = lst[point]
            point -= 1
        lst[point+1] = key
    return lst

@taimer
def merge_sort(lst):
    """ Сортировка слиянием """
    if len(lst) <= 1:
        return lst
    #if len(lst) > 2:
    #    return merge_sort(lst)

    def _merge(l_):
        print(l_)

    with mpp.ThreadPool(10) as pool:
        result = [pool.apply_async(_merge, args=(lst, )) ]


@taimer
def heap_sort(lst):
    """
    Последовательность: 4, 10, 3, 5, 1
        4(0)
       /   \
        10(1)   3(2)
           /   \
     (3)    1(4)
    """
    n = len(lst)

    def heapify(lst, n, i):
        largest = i
        l = 2*i+1  # left = 2*i + 1
        r = 2*i+2  # right = 2*i + 2
        if l < n and lst[i] < lst[l]:
            largest = l
        if r < n and lst[largest] < lst[r]:
            largest = r

        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]
            heapify(lst, n, largest)

    for i in range(n,-1,-1):
        heapify(lst, n, i)

    for i in range(n-1,0,-1):
        lst[i], lst[0] = lst[0], lst[i]
        heapify(lst, i, 0)

    return lst


if __name__ == '__main__':

    print(output(insert_sort(INPUT)))
    print(output(bubble_sort(INPUT)))
    print(output(quick_sort(INPUT)))
    print(output(quick_sort_gevent(INPUT)))
    print(output(heap_sort(INPUT)))

