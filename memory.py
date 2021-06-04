MAX_SPACE = 1000

class Heap:
    def __init__(self):
        self.table = [0 in range(MAX_SPACE)]
        self.size = 0
        self.count = 0
        self.dic = {}      # addr - > (off, size)

    def find_off(self, size):
        count = 0
        for i in range(MAX_SPACE):
            if self.table[i] == 0:
                count += 1
            else:
                count = 0
            if count == size:
                for j in range(size):
                    self.table[i - j] = 1
                return i - size + 1
        return -1   # need arrangement

    def malloc(self, addr, size):
        if size < 0 or size > MAX_SPACE:
            print("size error\n")
            return None
        off = self.find_off(size)

        self.dic[addr] = [off, size]
        self.size += size
        self.count += 1

    def free(self, addr):
        if addr not in self.dic:
            print("no such addr error\n")
            return -1

        off, size = self.dic[addr]
        for i in range(size):
            self.table[off + i] = 0

        self.size -= size
        self.count -= 1

    def mem(self):
        print("Dynamic allocation : {}, {}\n".format(self.count, self.size))