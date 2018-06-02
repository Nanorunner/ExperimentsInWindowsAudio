import pyaudio
import os

chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()

if __name__ == "__main__":
    for x in range(100):
        p.get_device_info_by_index(x)
    os.system("PAUSE")
def grabDeviceIndex(search):
    for x in range(100):
        if p.get_device_info_by_index(x)["name"].find(search) != -1:
            return p.get_device_info_by_index(x)["index"]
