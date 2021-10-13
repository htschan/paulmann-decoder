from mysocket import MySocket

remote_ip = "192.168.0.169"
port = 5024
count = 0


def main():
    global remote_ip
    global port
    global count

    # Body: send the SCPI commands *IDN? and print the return message
    s = MySocket()
    s.connect(remote_ip, port)

    qStr = s.query(b'*IDN?')
    print(str(count) + ":: " + str(qStr))

    s.send(b'chdr off')
    vdiv = float(s.query(b'c1:vdiv?').decode("utf-8")[2 :].strip())  # vertical volt / div
    ofst = float(s.query(b'c1:ofst?').decode("utf-8")[2 :].strip())  # vertical offset
    tdiv = float(s.query(b'tdiv?').decode("utf-8")[1 :].strip())  # time / div
    sara = float(s.query(b'sara?').decode("utf-8")[2 :].strip())  # sampling rate
    s.send(b'WFSU SP,0,NP,10,FP,1000')

    qStr = s.query(b'C1:WF? DAT2')
    print(str(count) + ":: " + str(qStr))

    s.close()
    input("Press 'Enter' to exit")


if __name__ == '__main__':
    proc = main()
