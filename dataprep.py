import pandas as pd
import time
import sounddevice as sd
from scipy.io.wavfile import write
from os import path
import threading
import sys
import re

file_prefix = "data/uugan_voice_"
metadata = "uugna_metadata.csv"
data_file = "mn_books_1.txt"
start_from = 0
seconds = 0
fs = 44100

if path.exists(metadata):
    tmp = pd.read_csv(metadata, delimiter="|").tail(1).iloc[:, 0].item()
    start_from = int(re.search("voice_(.*).wav", tmp).group(1))
    print("starting from " + str(start_from))


def print_time():
    for remaining in range(seconds, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        time.sleep(1)


for i, line in enumerate(open(data_file)):
    if i > start_from:
        line = line.strip()
        print(line)
        seconds = int(input("how many seconds u need?: "))
        if seconds == -1:
            continue
        t1 = threading.Thread(target=print_time)
        t1.start()
        t = time.time()

        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        filename = f"{file_prefix + str(i)}.wav"
        write(filename, fs, myrecording)
        print(f"Saved {filename}")

        duration = time.time() - t
        df = pd.DataFrame({"fname": [filename], "duration": [duration], "text": [line]})
        lol = input("Enter to continue, \"q\" to quit, \"s\" to skip\n")
        if lol != "s":
            df.to_csv(metadata, mode="a", index=False, header=False, sep="|")
        if lol == "q":
            break
