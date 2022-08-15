import socket
import random
import re
import utils

PKT_LOSS_PROBABILITY = 0

if __name__ == "__main__":
    buffer = utils.Buffer(100)
    s = socket.socket()
    host = socket.gethostname()
    port = 3031
    s.bind((host, port))
    s.listen(5)
    c = None
    last_acked = 9

    while True:
        if c is None:
            print('[Waiting connection...]')
            c, addr = s.accept()
            print(addr)
            print('Client connected', addr)
        else:
            # try:
            #     pkt = c.recv(1024)
            # except SocketError as e:
            #     if e.errno != errno.ECONNRESET:
            #         raise  # Not error we are looking for
            #     time.sleep(0)
            #     # pass  # Handle error here.

            pkt = c.recv(517)
            msg = pkt.decode()
            # print(msg)
            seq_num = int(re.findall(r"\[(\d+)\]", msg)[0])
            loss_roll = random.uniform(0, 1)
            if loss_roll > PKT_LOSS_PROBABILITY:
                if last_acked < 29:
                    if seq_num != last_acked + 1:
                        msg = "ACK" + str(last_acked)
                        # print(msg)
                        c.send(msg.encode())
                    elif seq_num == last_acked + 1:
                        last_acked = seq_num
                        res = buffer.insert(pkt)
                        msg = "ACK" + str(seq_num)
                        # print(msg)
                        c.send(msg.encode())
                else:
                    if seq_num != 10:
                        msg = "ACK" + str(last_acked)
                        # print(msg)
                        c.send(msg.encode())
                    elif seq_num == 10:
                        last_acked = seq_num
                        res = buffer.insert(pkt)
                        msg = "ACK" + str(seq_num)
                        # print(msg)
                        c.send(msg.encode())

                    # if res == 2:
                    #     msg = "buffer full!"
                    #     s.send(msg.encode())

            else:
                pass
                # msg = "ACK" + str(last_acked)
                # s.send(msg.encode())
