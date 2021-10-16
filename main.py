from mysocket import MySocket
from dataprocessor import DataProcessor

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
    vdiv = float(s.query(b'c1:vdiv?').decode("utf-8")
                 [2:].strip())  # vertical volt / div
    ofst = float(s.query(b'c1:ofst?').decode(
        "utf-8")[2:].strip())  # vertical offset
    tdiv = float(s.query(b'tdiv?').decode("utf-8")[1:].strip())  # time / div
    sara = float(s.query(b'sara?').decode("utf-8")
                 [1:].strip())  # sampling rate
    s.send(b'WFSU SP,0')

    data = s.query(b'C1:WF? DAT2')
    dp = DataProcessor(data, vdiv=vdiv, voffset=ofst, tdiv = tdiv, sara = sara)
    bits = dp.process()

    for i in range(len(bits)):
        print("i[" + str(i) + "]: rawvalue: " + str(bits[i]) + " volt: " + str(bits[i]) + " time: " + str(bits[i]))
        # if i % 10 == 0:
        #     input("Press 'Enter' to continue")

    s.close()
    input("Press 'Enter' to exit")


if __name__ == '__main__':
    proc = main()
