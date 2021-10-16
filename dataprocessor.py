

class DataProcessor:

    def __init__(self, data, vdiv, voffset, tdiv, sara):
        self.data = data
        self.vdiv = vdiv
        self.voffset = voffset
        self.tdiv = tdiv
        self.sara = sara
        self.grid = 14

    def process(self):
        print("process data, len: " + str(len(self.data)))
        bits = []
        tfirst = -(self.tdiv * self.grid / 2)
        tinterval = 1 / self.sara
        isample = 0
        d_zero_bit_min = 0.0000001 # 100 ns
        d_zero_bit_max = 0.0000003 # 300 ns
        d_one_bit_min = 0.0000003 # 300 ns
        d_one_bit_max = 0.0000010 # 1000 ns
        t_p_pause = 0.000010 # 10 usec
        t_rising_edge = 0.0
        t_falling_edge = -20.0
        v_rising_th = 3.0
        v_falling_th = 0.5
        p_high = False
        for i in range(len(self.data)):
            if i < 22:
                continue
            code = self.data[i]
            if code > 127:
                code = code - 255
            voltage = code * self.vdiv / 25 - self.voffset
            t = tfirst + isample * tinterval
            # if voltage > 0.1:
            #     print("voltag: " + str(voltage) + "   t: " + str(t * 1000000) + " us")
            if p_high: # pulse high
                if voltage < v_falling_th:
                    t_falling_edge = t
                    p_high = False
                    t_p_duration = t - t_rising_edge
                    print("------------ t_p_duration: " + str(t_p_duration * 1000000000) + " voltag: " + str(voltage))
                    if t_p_duration > d_zero_bit_min and t_p_duration < d_zero_bit_max:
                        bits.append(0)
                    if t_p_duration > d_one_bit_min and t_p_duration > d_one_bit_max:
                        bits.append(1)
            else: # pulse low
                if voltage > v_rising_th:
                    t_p_duration = t - t_falling_edge
                    print("------------ t_p_duration: " + str(t_p_duration * 1000000000) + " voltag: " + str(voltage))
                    if t_p_duration > t_p_pause:
                        t_rising_edge = t
                        p_high = True

            isample += 1
        return bits
