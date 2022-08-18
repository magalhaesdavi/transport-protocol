import random


class Buffer:
    def __init__(self, buffer_size):
        self.buffer = []
        self.buffer_size = buffer_size

    def free_slot(self, n=1):
        # idx = random.randrange(self.buffer_size)
        for i in range(n):
            self.buffer.pop(0)

    def insert(self, data):
        used_space = len(self.buffer) / self.buffer_size
        if used_space > 0.9:
            if random.uniform(0, 1) < used_space / 1.5:
                if used_space > 0.95:
                    self.free_slot(n=250)
                else:
                    self.free_slot(n=125)
        if len(self.buffer) < self.buffer_size:
            self.buffer.append(data)
            return self.get_status()
        else:
            # msg = 'buffer full!'
            # c.send(msg.encode())
            self.free_slot(n=250)
            self.buffer.append(data)
            return 1

    def get_status(self):
        return (len(self.buffer) / self.buffer_size) > 0.9
