from memory import Heap


def check(heap):        # function for checking current heap structure's state

    heap.print_line()
    heap.print_table()

    heap.print_line()
    heap.print_data()


def main():             # testing memory.py
    print("hi memory.py!")
    heap = Heap()
    heap.print_line()
    heap.print_line()

    a = heap.malloc(8)
    heap.save_datas(a, 'aaaaaaaa')
    check(heap)

    b = heap.malloc(8)
    heap.save_datas(b, 'bbbbbbbb')
    check(heap)

    c = heap.malloc(8)
    heap.save_datas(c, 'cccccccc')
    check(heap)

    d = heap.malloc(8)
    heap.save_datas(d, 'dddddddd')
    check(heap)

    e = heap.malloc(8)
    heap.save_datas(e, 'eeeeeeee')
    check(heap)

    heap.free(b)
    heap.free(d)
    check(heap)

    f = heap.malloc(15)     # dynamic memory management occur..! (lack of space for 15 bytes)
    heap.save_datas(f, 'f'*15)
    check(heap)


if __name__ == '__main__':
    main()