import pyaudio
from showAudioDeviceIndicies import grabDeviceIndex
import numpy as np
import os


# add decay?

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
    counter = 0
    currMaxL = 0
    currVL = 0
    currMaxR = 0
    currVR = 0
    while True:
        data = np.fromstring(stream.read(1024), dtype=np.int16)
        dataL = data[0::2]
        dataR = data[1::2]
        peakL = np.abs(np.max(dataL) - np.min(dataL)) / 4096
        if peakL > currMaxL:
            currMaxL = peakL
            currVL = currMaxL * 8
        peakR = np.abs(np.max(dataR) - np.min(dataR)) / 4096
        if peakR > currMaxR:
            currMaxR = peakR
            currVR = currMaxR * 8
        # for left and right vu meters per chunk
        lString = "+" * int(peakL * 40) + "-" * int(40 - peakL * 40)
        lString[currMaxL] = "|" # decay display functionality? untested and purely for visual effect
        currMaxL -= currVL
        rString = "+" * int(peakR * 40) + "-" * int(40 - peakR * 40)
        rString[currMaxR] = "|"
        currMaxR -= currVR
        clear()
        print("L=[%s]\tR=[%s]" % (lString, rString))