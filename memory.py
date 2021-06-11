MAX_SPACE = 40
print_size = 20
data_blank = '*'        # form of blank data (string currently) # TODO #1: change into appropriate data form
debugging = True        # print arguments for errors
debugging2 = True       # print arguments before some function returns
debugging3 = False      # memory tracking
base_address = 0x100000 # base address of virtual memory space
VM_size = MAX_SPACE * 100


class Heap:
    def __init__(self):
        self.data = data_blank * MAX_SPACE          # space to save data
        self.table = [0 for i in range(MAX_SPACE)]  # Projection of self.data: 0 if empty, 1 if occupied
        self.table2 = [0 for i in range(VM_size)]   # table for getting virtual address
        self.size = 0                               # total allocated memory size
        self.count = 0                              # the number of allocated variables
        self.dic = {}                               # address of variable - > (offset, allocated size)

    # noinspection PyMethodMayBeStatic
    def is_valid(self, off):    # check whether offset in 0 ~ (MAX_SPACE - 1)
        if off < 0 or off >= MAX_SPACE:
            if debugging:
                print("not valid offset : {}\n".format(off))
            return -1
        else:
            return 1

    def get_off(self, var):     # get offset of variable
        if var not in self.dic:
            if debugging:
                print("no such variable in memory space... var : {}\n".format(var))
            return -1
        return self.dic[var][0]

    def get_size(self, var):    # get allocated memory size of variable
        if var not in self.dic:
            if debugging:
                print("no such var in memory space... var : {}\n".format(var))
            return -1
        return self.dic[var][1]

    def get_var(self, off):     # get address of variable in offset 'off'
        for key in self.dic:
            if self.dic[key][0] == off:
                return key

        if debugging:
            print("not allocated in offset {}\n".format(off))

        return -1

    def get_data(self, off):       # get 1 byte data in offset 'off'
        if self.is_valid(off):
            return self.data[off]
        else:
            return -1

    def get_datas(self, off, size):     # get data of size 'size'
        if self.is_valid(off) and self.is_valid(off + size - 1):
            return self.data[off:off + size]
        else:
            return -1

    def reset_data(self, off, size):    # reset data in offset 'off' ~ 'off + size - 1' into 'data_blank'
        self.data = self.data[:off] + data_blank * size + self.data[off + size:]

    def save_data(self, var, byte):     # save data 'byte' into offset of variable 'var'
        if var not in self.dic:
            if debugging:
                print("no such addr : {} in dic..!\n".format(var))
            return -1
        off = self.get_off(var)

        if self.is_valid(off):
            self.data = self.data[:off] + byte + self.data[off + 1:]
            return 1
        else:
            return -1

    def save_datas(self, var, bytes):   # save continuous data 'bytes' into offset of variable 'var'
        if var not in self.dic:
            if debugging:
                print("no such addr : {} in dic..!\n".format(var))
            return -1
        off = self.get_off(var)

        if var == -1:
            return -1
        size = self.get_size(var)

        if size < len(bytes):
            if debugging:
                print("need more memory allocation..!\n")
            return -1

        if debugging2:
            print("saving addr : {:#x} offset : {}\n".format(var, off))

        self.reset_data(off, size)  # reset memory space before saving input data
        self.data = self.data[:off] + bytes + self.data[off + len(bytes):]
        return 1

    def dynamic_allocation(self, size):     # simply sort data forward to do defragmentation
        zero_point = -1     # offset of first appearing empty memory space

        # find zero_point
        for i in range(MAX_SPACE):
            if self.table[i] == 0:
                zero_point = i
                break

        off = zero_point + 1
        if debugging3:
            print("offset : {} right?\n".format(off))

        # Memory defragmentation    # TODO #2 : use heap maybe..?
        while zero_point != -1 and off < MAX_SPACE:
            if self.table[off] == 1:
                # find var information in offset 'off'
                var = self.get_var(off)
                _, size2 = self.dic[var]
                self.dic[var] = [zero_point, size2]

                buffer = self.get_datas(off, size2)  # save data into buffer to move forward
                for i in range(size2):   # change the table according to data movement
                    self.table[off + i] = 0
                    self.table[zero_point + i] = 1

                    if debugging3:
                        self.print_line()
                        self.print_table()
                        self.print_line()
                        self.print_data()
                        print("")

                # empty previous data space, copy the data in buffer into reallocated space
                self.reset_data(off, size2)
                self.save_datas(var, buffer)
                off += size2

                if debugging3:
                    self.print_line()
                    self.print_table()
                    self.print_line()
                    self.print_data()
                    print("")

                # find zero_point again
                zero_point = -1
                for i in range(MAX_SPACE):
                    if self.table[i] == 0:
                        zero_point = i
                        break

            else:
                off += 1    # check next offset

        return self.find_off(size)      # find memory space with size 'size' again to allocate

    def find_addr(self, size):       # find offset in self.data with continuously empty 'size' size memory
        count = 0

        for i in range(VM_size):
            if self.table2[i] == 0:
                count += 1
            else:
                count = 0
            if count == size:
                # add 1s in table before allocating memory to variable
                for j in range(size):
                    self.table2[i - j] = 1
                return base_address + i - size + 1

        return -1

    def find_off(self, size):       # find offset in self.data with continuously empty 'size' size memory
        count = 0

        for i in range(MAX_SPACE):
            if self.table[i] == 0:
                count += 1
            else:
                count = 0
            if count == size:
                # add 1s in table before allocating memory to variable
                for j in range(size):
                    self.table[i - j] = 1
                return i - size + 1

        if size == 1:
            return -1

        return self.dynamic_allocation(size)    # if there is no enough space, do dynamic_allocation()

    def malloc(self, size):    # allocate memory to var
        if size < 0 or size > MAX_SPACE:
            if debugging:
                print("size error\n")
            return 0

        # get offset of memory space to allocate to var
        off = self.find_off(size)
        if off == -1:
            if debugging:
                print("no more memory space is available..!\n")
                self.mem()
            return 0

        # register var to dic
        var = self.find_addr(size)
        if var == -1:
            if debugging:
                print("no more VM space is available..!\n")
                self.mem()
            return 0

        self.dic[var] = [off, size]
        self.size += size
        self.count += 1
        if debugging:
            print("malloc addr : {:#x} offset : {}\n".format(var, off))

        return var

    def free(self, var):    # free memory for var
        if var not in self.dic:
            if debugging:
                print("no such var error\n")
            return -1

        off, size = self.dic[var]
        if debugging2:
            print("free addr : {:#x} offset : {}\n".format(var, off))

        # remove var from table, data(memory), self.dic
        vm_off = var - base_address
        for i in range(size):
            self.table[off + i] = 0
            self.table2[vm_off + i] = 0
        self.reset_data(off, size)
        del(self.dic[var])

        self.size -= size
        self.count -= 1
        return 1

    def mem(self):      # print total allocated memory count and size
        print("Dynamic allocation : {}, {}\n".format(self.count, self.size))

    def print_table(self):  # print self.table just for debugging
        count = 0
        for i in self.table:
            count += 1
            print(i, end=' ')
            if count % print_size == 0:
                print('')

    def print_data(self):   # print self.data just for debugging
        count = 0
        for i in self.data:
            count += 1
            print(i, end=' ')
            if count % print_size == 0:
                print('')

    # noinspection PyMethodMayBeStatic
    def print_line(self):   # print line just for debugging
        print('-' * (print_size * 2 - 1))