import socket
import time
import threading
import random
import string
import re
from socket import error as SocketError
import errno
import utils
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


def check_timeout(timers):
    global timedout, timedout_id
    # while not done:
    for key in list(timers):
        if time.time() - timers[key] > 1:
            return int(key)
            # timedout = True
            # timedout_id = int(key)
    return -1


def sender(path):
    # test_file = open(path, 'r')
    # lines = test_file.readlines()
    # print(lines[0])
    # lines = []
    # with open(r"test.txt", 'r') as fp:
    #     for count, line in enumerate(fp):
    #         lines.append(line)
    # print(lines[0])

    global last_acked, done, rtt, upper_bound
    seq_num = utils.SequeceNumber()
    i = 0
    while i < 20480:
        lock.acquire()
        if i < upper_bound:
            print('i: ' + str(i))
            # idx = seq_num.get_next()
            idx = (i % 20) + 10
            pkt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=PKT_SIZE))
            pkt = '[' + str(idx) + '] ' + pkt
            # print(pkt)
            pkt = pkt.encode()
            s.send(pkt)
            # try:
            #     s.send(pkt)
            # except SocketError as e:
            #     if e.errno != errno.ECONNRESET:
            #         raise  # Not error we are looking for
            #     pass  # Handle error here.
            timers[str(idx)] = time.time()
            # print(timers)
            i += 1
        else:
            # print(timers)
            temp = check_timeout(timers)
            lock.release()
            if temp != -1:
                i = temp
            # if lock.acquire(False):
            #     print(timers)
            #     # print('a')
            #     for key in list(timers):
            #         # print('b')
            #         # print(timers)
            #         if str(key) in timers:
            #             if time.time() - timers[key] > 10:
            #                 i = int(key)
            #     lock.release()
        #     time.sleep(0)
        # if timedout:
        #     i = timedout_id
        #     timedout = False
    done = True
    print("Done!")
    # print("Average RTT: " + str(rtt / 20480))


def receiver():
    global last_acked, timedout, timedout_id, rtt, upper_bound
    while not done:
        # pkt = []
        # while not pkt:
        #     try:
        #         pkt = s.recv(5)
        #     except SocketError as e:
        #         if e.errno != errno.ECONNRESET:
        #             raise  # Not error we are looking for
        #         time.sleep(0)
        #         # pass  # Handle error here.
        pkt = s.recv(5)
        msg = pkt.decode()
        print(msg)
        msg_seq_num = int(re.findall(r'\d+', msg)[0])
        lock2.acquire()
        if msg_seq_num != last_acked:
            # print(rtt)
            # print(timers)
            # rtt += time.time() - timers[str(msg_seq_num)]
            timers.pop(str(msg_seq_num))
            last_acked = msg_seq_num
            # print(last_acked)
            upper_bound += 1
        lock2.release()
        # time.sleep(0)


# BUFFER_SIZE = 1024
WINDOW_SIZE = 10
PKT_SIZE = 512

# if __name__ == "__main__":
done = False
# buffer = utils.Buffer(BUFFER_SIZE)
timers = {}
# timedout = False
# timedout_id = -1

s = socket.socket()
host = socket.gethostname()
port = 3031
s.connect((host, port))
print('Connected to', host)
last_acked = 9
upper_bound = 10
rtt = 0

lock = threading.Lock()
lock2 = threading.Lock()

receiver_thread = threading.Thread(name='daemon', target=receiver)
receiver_thread.daemon = True

path = 'test.txt'
sender_thread = threading.Thread(name='non-daemon', target=sender, args=(path,))

receiver_thread.start()
sender_thread.start()

receiver_thread.join()
sender_thread.join()

# def check_timeout(timers):
#     # print(timers)
#     for key in timers:
#         if time.time() - timers[key] > AVERAGE_RTT * 1.5:
#             return int(key)
#     return -1
#
#
# WINDOW_SIZE = 10
# PKT_SIZE = 512
# AVERAGE_RTT = 0.0018207671237178147
#
# # if __name__ == "__main__":
# done = False
# timers = {}
#
# s = socket.socket()
# host = socket.gethostname()
# port = 3031
# s.connect((host, port))
# print('Connected to', host)
# last_acked = 9
# rtt = 0
#
# # test_file = open(path, 'r')
# # lines = test_file.readlines()
# # print(lines[0])
# # lines = []
# # with open(r"test.txt", 'r') as fp:
# #     for count, line in enumerate(fp):
# #         lines.append(line)
# # print(lines[0])
#
#
# seq_num = utils.SequeceNumber()
# i = 0
# upper_bound = 10
# while i < 20480:
#     # print((i % 20) + 10)
#     if i < upper_bound:
#         print('i: ' + str(i))
#         # idx = seq_num.get_next()
#         idx = (i % 20) + 10
#         pkt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=PKT_SIZE))
#         pkt = '[' + str(idx) + '] ' + pkt
#         # print(pkt)
#         pkt = pkt.encode()
#         s.send(pkt)
#         # try:
#         #     s.send(pkt)
#         # except SocketError as e:
#         #     if e.errno != errno.ECONNRESET:
#         #         raise  # Not error we are looking for
#         #     pass  # Handle error here.
#         timers[str(idx)] = time.time()
#         # print(timers)
#         i += 1
#     else:
#         j = 0
#         while j < 10:
#             # pkt = []
#             # while not pkt:
#             #     try:
#             #         pkt = s.recv(5)
#             #     except SocketError as e:
#             #         if e.errno != errno.ECONNRESET:
#             #             raise  # Not error we are looking for
#             #         time.sleep(0)
#             #         # pass  # Handle error here.
#             pkt = s.recv(5)
#             msg = pkt.decode()
#             # print(msg)
#             msg_seq_num = int(re.findall(r'\d+', msg)[0])
#             if msg_seq_num != last_acked:
#                 # print(rtt)
#                 # print(timers)
#                 rtt += time.time() - timers[str(msg_seq_num)]
#                 timers.pop(str(msg_seq_num))
#                 last_acked = msg_seq_num
#                 # print(last_acked)
#                 upper_bound += 1
#             j += 1
#
#         # print(timers)
#         temp = check_timeout(timers)
#         if temp != -1:
#             i = temp
#         # print('ok')
#
# done = True
# print("Done!")
# print("Average RTT: " + str(rtt / 20480))
