import os

FILE_NAME = "data.txt"

def load_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        return [[v.strip().split(" ") for v in line.strip().split("|")] for line in lines]


def decode(signals):
    signals = [set(signal) for signal in signals]
    encoding = [None] * 10
    display = [None] * 7
    encoding[1] = set(next(signal for signal in signals if len(signal) == 2))
    encoding[4] = set(next(signal for signal in signals if len(signal) == 4))
    encoding[7] = set(next(signal for signal in signals if len(signal) == 3))
    encoding[8] = set(next(signal for signal in signals if len(signal) == 7))

    display[0] = encoding[7].difference(encoding[1])
    len_six = [signal for signal in signals if len(signal) == 6]
    cf = encoding[7].difference(display[0])
    encoding[6] = next(signal for signal in len_six if len(cf.difference(signal)) != 0)
    len_six.remove(encoding[6])
    display[2] = encoding[8].difference(encoding[6])
    display[5] = cf.difference(display[2])
    bd = encoding[4].difference(encoding[1])
    encoding[0] = next(signal for signal in len_six if len(bd.difference(signal)) != 0)
    display[3] = encoding[8].difference(encoding[0])
    display[1] = bd.difference(display[3])
    len_six.remove(encoding[0])
    encoding[9] = next(iter(len_six))
    display[4] = encoding[8].difference(encoding[9])
    display[6] = encoding[8].difference({d for v in display if v is not None for d in v })
    encoding[2] = [ ] # a, c, d, f, g
    return encoding

if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), FILE_NAME)
    data = load_file(file_path)
    # print(sum(1 for d in data for val in d[1] if len(val) in [2, 3, 4, 7]))

    for display in data:
        signals, output = display
        encoding = decode(signals)
        print(encoding)
        exit()
