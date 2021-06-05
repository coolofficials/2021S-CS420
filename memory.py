MAX_SPACE = 1000
print_size = 50


class Heap:
    def __init__(self):
        self.data = ' ' * MAX_SPACE
        self.table = [0 for i in range(MAX_SPACE)]
        self.size = 0
        self.count = 0
        self.dic = {}      # var - > (off, size)

    def is_valid(self, off):
        if off < 0 or off >= MAX_SPACE:
            print("not valid offset : {}\n".format(off))
            return -1
        else:
            return 1

    def get_off(self, var):
        if var not in self.dic:
            print("no such variable in memory space... var : {}\n".format(var))
            return -1
        return self.dic[var][0]

    def get_size(self, var):
        if var not in self.dic:
            print("no such var in memory space... var : {}\n".format(var))
            return -1
        return self.dic[var][1]

    def get_var(self, off):
        for key, value in self.dic:
            if value[0] == off:
                return key
        print("not allocated in offset {}\n".format(off))
        return -1

    def get_data(self, off):
        if self.is_valid(off):
            return self.data[off]
        else:
            return -1

    def get_datas(self, off, size):
        if self.is_valid(off) and self.is_valid(off + size - 1):
            return self.data[off:off + size]
        else:
            return -1

    def save_data(self, off, byte):
        if self.is_valid(off):
            self.data[off] = byte
            return 1
        else:
            return -1

    def save_datas(self, off, size, bytes):
        if self.is_valid(off) and self.is_valid(off + size - 1):
            if len(bytes) != size:
                print("allocating size and data size are different..!\n")
                return -1
            for i in range(size):
                self.data[off + i] = bytes[i]
            return 1
        else:
            return -1

    def dynamic_allocation(self, size):
        pass

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
        #return dynamic_allocation(size)
        return -1

    def malloc(self, var, size):
        if size < 0 or size > MAX_SPACE:
            print("size error\n")
            return -1
        off = self.find_off(size)
        if off == -1:
            print("no more sufficient memory is available..!\n")
            self.mem()
            return -1

        self.dic[var] = [off, size]
        self.size += size
        self.count += 1
        return 1

    def free(self, var):
        if var not in self.dic:
            print("no such var error\n")
            return -1

        off, size = self.dic[var]
        for i in range(size):
            self.table[off + i] = 0

        self.size -= size
        self.count -= 1
        return 1

    def mem(self):
        print("Dynamic allocation : {}, {}\n".format(self.count, self.size))

    def print_table(self):
        count = 0
        for i in self.table:
            count += 1
            print(i, end=' ')
            if count % print_size == 0:
                print('')

    def print_data(self):
        count = 0
        for i in self.data:
            count += 1
            print(i, end=' ')
            if count % print_size == 0:
                print('')
