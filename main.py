from memory import Heap

def main():
    print("hi memory.py!")
    heap = Heap()

    a = heap.malloc()
    heap.print_table()

if __name__ == '__main__':
    main()