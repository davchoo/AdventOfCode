def process_data(data):
    return list(map(int, data))


base_pattern = [0, 1, 0, -1]


def pattern(i, repeat):
    return base_pattern[((i + 1) // repeat) % 4]


def fft(signals, offset=0):
    def general_fft(src, dst, end):
        for i in range(end):
            dst[i] = abs(sum(signal * pattern(j + offset, i + 1) for j, signal in enumerate(src))) % 10

    def fast_fft(src, dst, start):
        running_sum = 0
        for i in range(len(src) - 1, start - 1, -1):
            running_sum = abs((running_sum + src[i]) % 10)
            dst[i] = running_sum

    for phase in range(100):
        new_signals = [0] * len(signals)
        mid = (len(signals) + offset) // 2 - offset
        if mid < 0:
            mid = 0
        general_fft(signals, new_signals, mid)
        fast_fft(signals, new_signals, mid)
        signals = new_signals

    return signals


def solve_a(data):
    data = process_data(data)
    signals = fft(data)
    return "".join(map(str, signals[0:8]))


def solve_b(data):
    message_offset = int(data[0:7])
    data = process_data(data) * 10000
    data = data[message_offset:]
    signals = fft(data, message_offset)
    return "".join(map(str, signals[0:8]))
