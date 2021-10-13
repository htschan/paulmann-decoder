from mysocket import MySocket

remote_ip = "192.168.0.169"
port = 5024
count = 0





def main():
    global remote_ip
    global port
    global count

    # Body: send the SCPI commands *IDN? 10 times and print the return message
    s = MySocket()
    s.connect(remote_ip, port)

    qStr = s.query(b'*IDN?')
    print(str(count) + ":: " + str(qStr))

    s.send(b'chdr off')
    vdiv = s.query(b'c1:vdiv?')  # vertical volt / div
    ofst = s.query(b'c1:ofst?')  # vertical offset
    tdiv = s.query(b'tdiv?')  # time / div
    sara = s.query(b'sara?')  # sampling rate
    s.send(b'WFSU SP,0,NP,10,FP,1000')

    qStr = s.query(b'C1:WF? DAT2')
    print(str(count) + ":: " + str(qStr))

    s.close()
    input("Press 'Enter' to exit")


if __name__ == '__main__':
    proc = main()
