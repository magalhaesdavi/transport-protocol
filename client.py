from ast import If
from http.cookiejar import LWPCookieJar
import socket
import time
import threading
import random
import string
import re
from socket import error as SocketError, timeout
import errno
import argparse

from more_itertools import first
import utils
from signal import signal, SIGPIPE, SIG_DFL

signal(SIGPIPE, SIG_DFL)


def check_timeout(timers):
    global timedout, timedout_id
    for key in list(timers):
        if time.time() - timers[key] > 1:
            return int(key)
    return -1


def sender(path):
    test_file = open(path, 'r')
    lines = test_file.readlines()
    receiver_thread = threading.Thread(name='daemon', target=receiver)
    receiver_thread.daemon = True
    receiver_thread.start()

    global last_acked, done, rtt, upper_bound, lower_bound, first_run, pkt_timer, timeouts, pending_acks, pause
    i = 0
    while lower_bound < len(lines):  # 20480
        # print(lower_bound)
        if buffer_full:
            time.sleep(0.5)
        if first_run:
            pkt_timer = time.time()
            first_run = False
        
        if not (i % 500):
            timeouts = 0

        if time.time() - pkt_timer > 0.27:
            i = lower_bound
            pkt_timer = time.time()
            timeouts += 1
            # print("timeout!")

        if i < upper_bound and i < len(lines) and not pause:
            # print('i: ' + str(i))
            idx = (i % 20) + 10
            # pkt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=PKT_SIZE))
            pkt = lines[i]
            pkt = '[' + str(idx) + ']' + pkt
            # print(pkt)
            pkt = pkt.encode()
            s.send(pkt)
            # pending_acks += 1
            i += 1

        if timeouts > 20:
            time.sleep(1)
            timeouts = 0
            print("Too many timeouts!")
        # if pending_acks > 9:
        #     pause = True
        # else:
        #     pause = False
    
    done_lock.acquire()
    done = True
    done_lock.release()
    receiver_thread.join()
    print("Done!")
    # print("Average RTT: " + str(rtt / 20480))


def receiver():
    global last_acked, timedout, timedout_id, rtt, upper_bound, lower_bound, pkt_timer, buffer_full, pending_acks, pause
    while not done:
        pkt = s.recv(8)
        msg = pkt.decode()
        print(msg)
        lock.acquire()
        msg_seq_num = int(re.findall(r'\d+', msg)[0])
        buffer_full = int(re.findall(r'\d+', msg)[1])
        if msg_seq_num != last_acked:
            # print(rtt)
            # rtt += time.time() - pkt_timer
            last_acked = msg_seq_num
            # print('la: ' + str(last_acked))
            lower_bound += 1
            upper_bound += 1
            print('Lower bound: ' + str(lower_bound))
            # print('upper bound: ' + str(upper_bound))
            pkt_timer = time.time()
            pending_acks -= 1
            # print(pending_acks)
            # if pending_acks <= 9:
            #     pause = False
        lock.release()


if __name__ == "__main__":
    WINDOW_SIZE = 10
    PKT_SIZE = 512

    parser = argparse.ArgumentParser(description='Client application that will send data from file to a given port.')
    parser.add_argument("-p", "--port", help="Connection port.", default=3031)
    parser.add_argument("-f", "--file_path", help="File path.", default="text.txt")
    parser.add_argument("-i", "--iterations", help="Number of iterations.", default=10)
    args = parser.parse_args()

    s = socket.socket()
    host = socket.gethostname()
    port = int(args.port)
    s.connect((host, port))
    print('Connected to', host)

    done = False
    last_acked = 9
    upper_bound = 10
    lower_bound = 0
    rtt = 0
    pkt_timer = -1
    first_run = True
    buffer_full = False
    pending_acks = 0
    timeouts = 0
    pause = False

    lock = threading.Lock()
    done_lock = threading.Lock()

    path = args.file_path
    sender(path)

# lock = threading.Lock()
# lock2 = threading.Lock()

# receiver_thread = threading.Thread(name='daemon', target=receiver)
# receiver_thread.daemon = True

# path = 'test.txt'
# sender_thread = threading.Thread(name='non-daemon', target=sender, args=(path,))

# receiver_thread.start()
# sender_thread.start()

# receiver_thread.join()
# sender_thread.join()

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
