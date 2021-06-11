from memory import Heap
debugging = False


def check(heap):        # function for checking current heap structure's state
    if debugging:
        heap.print_line()
        heap.print_table()

        heap.print_line()
        heap.print_data()


def main():             # testing memory.py
    heap = Heap()

    if debugging:
        print("hi memory.py!")
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

    h = heap.malloc(333)
    i = heap.malloc(333)
    j = heap.malloc(333)
    k = heap.malloc(-2)
    heap.free(a + 1)
    heap.mem()      # a c e f h i / 8 8 8 15 333 333 = 6, 705
    l = heap.malloc(295)

    """
    address1 = heap.malloc(111)
    address2 = heap.malloc(222)
    address3 = heap.malloc(333)
    heap.free(address2)
    address4 = heap.malloc(444)
    address5 = heap.malloc(555)
    """


if __name__ == '__main__':
    main()
