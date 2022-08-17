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

# from signal import signal, SIGPIPE, SIG_DFL

# signal(SIGPIPE, SIG_DFL)


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
    global last_acked, done, rtt, upper_bound, lower_bound, first_run, pkt_timer, timeouts, pending_acks, ack_counter
    start_time = time.time()
    sent_pkts = 0
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

        # Max RTT: 0.5072517395019531
        # Average RTT: 0.0038837311207316817
        if time.time() - pkt_timer > 0.52:
            i = lower_bound
            pkt_timer = time.time()
            timeouts += 1
            # print("timeout!")
        
        if ack_counter >= 3:
            i = lower_bound
            pkt_timer = time.time()
            # timeouts += 1
            # print("timeout!")

        if i < upper_bound and i < len(lines):
            # print('i: ' + str(i))
            idx = (i % 20) + 10
            # pkt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=PKT_SIZE))
            pkt = lines[i]
            pkt = '[' + str(idx) + ']' + pkt
            # print(pkt)
            pkt = pkt.encode()
            s.send(pkt)
            sent_pkts += 1
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
        
    run_time = time.time() - start_time

    print("Runtime: " + str(run_time))
    print("Packets sent: " + str(sent_pkts))
    done_lock.acquire()
    done = True
    done_lock.release()
    print("Done!")
    pkt = "FIN"
    s.send(pkt.encode())
    exit()
    receiver_thread.join()
    # print("Average RTT: " + str(rtt / 20480))


def receiver():
    global last_acked, rtt, upper_bound, lower_bound, pkt_timer, buffer_full, pending_acks, ack_counter, executions, max_rtt
    while not done:
        pkt = s.recv(8)
        msg = pkt.decode()
        # print(msg)
        lock.acquire()
        msg_seq_num = int(re.findall(r'\d+', msg)[0])
        buffer_full = int(re.findall(r'\d+', msg)[1])
        if msg_seq_num != last_acked:
            # print(rtt)
            # rtt += time.time() - pkt_timer
            # rtt = time.time() - pkt_timer
            # if rtt > max_rtt:
            #     max_rtt = rtt
            # print(max_rtt)
            last_acked = msg_seq_num
            # print('la: ' + str(last_acked))
            lower_bound += 1
            upper_bound += 1
            if lower_bound % 500 == 0:
                print('Window lower bound: ' + str(lower_bound) + '/20480')
            # print('upper bound: ' + str(upper_bound))
            pkt_timer = time.time()
            pending_acks -= 1
            # print(pending_acks)
            # if pending_acks <= 9:
            #     pause = False
        else:
            ack_counter += 1
        lock.release()


if __name__ == "__main__":
    WINDOW_SIZE = 10
    PKT_SIZE = 512

    parser = argparse.ArgumentParser(description='Client application that will send data from file to a given port.')
    parser.add_argument("-p", "--port", help="Connection port.", default=3031)
    parser.add_argument("-f", "--file_path", help="File path.", default="text.txt")
    # parser.add_argument("-e", "--executions", help="Number of executions.", default=10)
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
    ack_counter = 0
    # executions = int(args.executions)
    max_rtt = 0

    lock = threading.Lock()
    done_lock = threading.Lock()

    path = args.file_path
    sender(path)
    exit()
