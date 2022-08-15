import random


class Buffer:
    def __init__(self, buffer_size):
        self.buffer = []
        self.buffer_size = buffer_size

    def free_slot(self):
        idx = random.randrange(self.buffer_size)
        self.buffer.pop(idx)

    def insert(self, data):
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(data)
            return 1
        else:
            # msg = 'buffer full!'
            # c.send(msg.encode())
            self.free_slot()
            self.buffer.append(data)
            return 2

    def status(self):
        return len(self.buffer)


class Pkt:
    def __init__(self, data, seq_num):
        self.data = data
        self.seq_num = seq_num
    
    def get_data(self):
        return self.data
    
    def set_data(self, data):
        self.data = data
        return 1
    
    def get_seq_num(self, seq_num):
        return self.seq_num
    
    def set_seq_num(self, seq_num):
        self.seq_num = seq_num
        return 1


class SequeceNumber:
    def __init__(self):
        self.list = list(range(10, 31))
        self.next = self.list[0]
        self.counter = 0

    def get_next(self):
        temp = self.next
        self.update()
        return temp

    def update(self):
        if self.counter + 1 < len(self.list):
            self.counter += 1
        else:
            self.counter = 0
        self.next = self.list[self.counter]
