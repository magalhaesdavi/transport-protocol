import socket
import random
import re
import utils
import argparse

# PKT_LOSS_PROBABILITY = 0.006
# BUFFER_SIZE = 1500

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Server application that will receive data from client and store in a buffer.')
    parser.add_argument("-p", "--port", help="Connection port.", default=3031)
    parser.add_argument("-l", "--loss_probability", help="Probability of losing a package.", default=0.01)
    parser.add_argument("-s", "--buffer_size", help="Size of the buffer.", default=1500)
    args = parser.parse_args()

    BUFFER_SIZE = int(args.buffer_size)
    PKT_LOSS_PROBABILITY = float(args.loss_probability)
    # print(PKT_LOSS_PROBABILITY)
    buffer = utils.Buffer(BUFFER_SIZE)
    s = socket.socket()
    host = socket.gethostname()
    port = int(args.port)
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
            if msg == 'FIN':
                exit()
            # print(msg)
            nums = re.findall(r"\[(\d+)\]", msg)
            if nums:
                seq_num = int(nums[0])
                loss_roll = random.uniform(0, 1)
                if loss_roll > PKT_LOSS_PROBABILITY:
                    if last_acked < 29:
                        if seq_num != last_acked + 1:
                            status = buffer.get_status()
                            msg = "ACK" + str(last_acked) + "BF" + str(int(status))
                            # print(msg)
                            c.send(msg.encode())
                        elif seq_num == last_acked + 1:
                            last_acked = seq_num
                            res = buffer.insert(pkt)
                            msg = "ACK" + str(seq_num) + "BF" + str(int(res))
                            # print(msg)
                            c.send(msg.encode())
                    else:
                        if seq_num != 10:
                            status = buffer.get_status()
                            msg = "ACK" + str(last_acked) + "BF" + str(int(status))
                            # print(msg)
                            c.send(msg.encode())
                        elif seq_num == 10:
                            last_acked = seq_num
                            res = buffer.insert(pkt)
                            msg = "ACK" + str(seq_num) + "BF" + str(int(res))
                            # print(msg)
                            c.send(msg.encode())
                else:
                    # print("loss")
                    pass

            else:
                pass
                # msg = "ACK" + str(last_acked)
                # s.send(msg.encode())
