########################################################################################################################
# Author: Enders Kong                                                                                                  #
# Some very basic framework double buffering for "real time" audio processing, need to use this as main and pass funs  #
# for trueRealTime no need for buffers. Functions may not perform well on single threaded CPUS, try multithread        #
########################################################################################################################


from pyaudio import PyAudio
import threading

chunks1 = 0
# opening and initializing audio streams, should be using .wav files
wavStreamOpen = PyAudio()
wavStream = wavStreamOpen.open(format="format1", channels="channels1", rate="rate1", input="input1",
                               frames_per_buffer="chunks1")
# initializing both buffers
buff1 = [0 for n in range(chunks1)]
buff2 = [0 for n in range(chunks1)]
# write to buffer1 before loop
buff1 = wavStream.read(chunks1)


def foo():
    i = 0
    print("you're still using foo, swap it with your actual function")
    return i


def writeBuf1():
    global wavStream
    global buff1
    buff1 = wavStream.read(chunks1)


def writeBuf2():
    global wavStream
    global buff2
    buff2 = wavStream.read(chunks1)


# the performance unfriendly and very dumb way of doing real time processing
def dubBuffer(format1, channels1, rate1, input1):
    global wavStream
    global wavStreamOpen
    tWrBuff1 = threading.thread(target=writeBuf1, args=10)
    tWrBuff2 = threading.thread(target=writeBuf2, args=10)
    # change foo to desired function for both funs
    tMdBuff1 = threading.thread(target=foo, args=10)
    tMdBuff2 = threading.thread(target=foo, args=10)
    while wavStream.is_active():
        # writing to buffer2 and modifying and playing buffer1 at the same time
        tWrBuff2.start()
        tMdBuff1.start()
        tWrBuff2.join()
        tMdBuff1.join()

        # writing to buffer1 and modifying and playing buffer2 at the same time
        tWrBuff1.start()
        tMdBuff2.start()
        tWrBuff1.join()
        tMdBuff2.join()
    # when stream is done terminate
    wavStream.close()
    wavStreamOpen.terminate()


# actual way you are supposed to do real time audio
def trueRealTime(format1, channels1, rate1, input1):
    streamOpen = PyAudio()
    stream = streamOpen.open(format=format1, channels=channels1, rate=rate1, input=input1,
                             frames_per_buffer=chunks1)
    while stream.is_active():
        # insert function you need doing here, remove return statement below
        return foo()
        break
    stream.close()
    streamOpen.terminate()