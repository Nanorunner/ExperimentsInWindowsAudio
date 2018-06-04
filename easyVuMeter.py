import pyaudio
from showAudioDeviceIndicies import grabDeviceIndex
import numpy as np
import os

chunk = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
INDEX = grabDeviceIndex("Digital") # select device index with digital in name
clear = lambda: os.system('cls')
if __name__ == "__main__":
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=2, rate=RATE, input=True, frames_per_bffer=chunk,
                    input_device_index=INDEX)   # select which input device to use, can be microphone, WASAPI, etc. use
                                                # grabDeviceIndex() to get index of needed device
    while True:
        data = np.fromstring(stream.read(1024), dtype=np.int16)
        dataL = data[0::2]
        dataR = data[1::2]
        peakL = np.abs(np.max(dataL) - np.min(dataL)) / 4096
        peakR = np.abs(np.max(dataR) - np.min(dataR)) / 4096
        # for left and right vu meters per chunk
        lString = "+" * int(peakL * 40) + "-" * int(40 - peakL * 40)
        rString = "+" * int(peakR * 40) + "-" * int(40 - peakR * 40)
        clear()
        print("L=[%s]\tR=[%s]" % (lString, rString))
