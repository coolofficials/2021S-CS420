MAX_SPACE = 1000

class Heap:
    def __init__(self):
        self.base = None    # base address of 1kb Memory Page
        self.table = [0 for i in range(MAX_SPACE)]
        self.size = 0
        self.count = 0
        self.dic = {}      # addr - > (off, size)
        #self.lastoff = -1

    def set_base(self, base):
        self.base = base

    def get_off(self, addr):
        if addr not in self.dic:
            print("no such addr in memory space... addr : {}\n".format(addr))
            return -1
        return self.dic[addr][0]

    def get_size(self, addr):
        if addr not in self.dic:
            print("no such addr in memory space... addr : {}\n".format(addr))
            return -1
        return self.dic[addr][1]

    def get_addr(self, off):
        for key, value in self.dic:
            if value[0] == off:
                return key
        print("not allocated in offset {}\n".format(off))
        return -1

    def get_contents(self):
        pass

    def save_contents(self):
        pass

    def dynamic_allocation(self, size):
        print("not implemented\n")
        return -1

    def find_off(self, size):
        count = 0

        #for i in range(self.lastoff + 1, MAX_SPACE + self.lastoff + 1 + size):
        #    if i == 0:
        #        count = 0
        #    elif i > MAX_SPACE:
        #        i -= MAX_SPACE
        for i in range(MAX_SPACE):
            if self.table[i] == 0:
                count += 1
            else:
                count = 0
            if count == size:
                for j in range(size):
                    self.table[i - j] = 1
                #self.lastoff = i
                return i - size + 1
        return dynamic_allocation(size)

    def malloc(self, addr, size):
        if size < 0 or size > MAX_SPACE:
            print("size error\n")
            return -1
        off = self.find_off(size)

        self.dic[addr] = [off, size]
        self.size += size
        self.count += 1
        return 1

    def free(self, addr):
        if addr not in self.dic:
            print("no such addr error\n")
            return -1

        off, size = self.dic[addr]
        for i in range(size):
            self.table[off + i] = 0

        self.size -= size
        self.count -= 1
        return 1

    def mem(self):
        print("Dynamic allocation : {}, {}\n".format(self.count, self.size))