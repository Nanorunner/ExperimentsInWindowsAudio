########################################################################################################################
# Author: Enders Kong                                                                                                  #
# This is meant to be a basic equalizer for .wav files. It functions by taking a .csv file called FreqGain.csv with    #
# (frequency, gain) pairs and altering said frequencies to match the gains mapped to it.                               #
########################################################################################################################

# for reverb dsp function try following:
# for (int i = 0; i < length; i++)
#   out += i
#   out += i * some time measured decay
# try, prime vals of i, and make for two channel audio


# TODO: perhaps implement a less obtuse input method than a .csv
# TODO: make use with stereo sound
# TODO: make gui, or export data to other language with better gui workability
# TODO: make it work with windows's native audio stream, as is, only works with .wav files passed in
# TODO: implement filters
# for "real time" processing try following:
#Recording Thread:
#   1.) Record a buffer
#   2.) Push the data on the Deque
#   3.) Repeat from 1

#Main Process:
#   1.) If the Deque has buffers then
#   2.) Pull a buffer from the Deque
#   3.) Process it
#   4.) Repeat from 1

# or, alternatively, offload to arduino acting as passthrough for usb audio?




import csv
import pyaudio
import math
import wave
import struct
import scipy as sp
from scipy import signal



# dict of frequencies mapped to gains to modify them by
# allows for an essentially infinite number of frequencies to be modified, and dict implementation ensures that no
# no duplicates are allowed
# However, current implementation is a three band eq, so currently only supports 3 dict entries.
FreqGain = {}
foo = 0

# parses a csv of which frequency vals to modify and the gain by which to modify them by
# FreqGain.csv should be formatted per row as follows: freq, gain
def parseFreqGain():
    global FreqGain
    with open("FreqGain.csv", "rb") as csvfile:
        filin = csv.reader(csvfile, delimiter=' ', quotechar='|')           # generic csv parser
        for row in filin:
            frequency, gain = row
            FreqGain[frequency] = gain

class implementFilterEquations():
    def __init__(self):
        playfile = "test.wav"                                               # TODO: change to use an actual input method
        self.wf = wave.open(playfile, "rb")                                 # open .wav file
        self.wfNumChannels = self.wf.getnchannels()                         # get number of channels, should be mono
        # shelving and peak filters, adapted from audio eq cookbook
        # set cutoff frequencies for low and high shelf
        self.lowFreqShelving = 500
        self.highFreqShelving = 10000
        # set gain for shelving filters
        self.dbGainShelving = 0
        # low shelving constant(s):
        lowVar = math.tan(math.pi * self.lowFreqShelving / self.wf.getframerate())  # getframerate() returns sample rate
        # high shelving constant(s):
        highVar = math.tan(math.pi * self.highFreqShelving / self.wf.getframerate())
        shelvingCoeff = 10 ** (self.dbGainShelving / 20)
        self.a0 = 1
        # shelving filters' equations:
        self.b0Low = (1 + math.sqrt(2 * shelvingCoeff) * lowVar + shelvingCoeff * (lowVar ** 2)) /\
                     (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b0High = (shelvingCoeff + math.sqrt(2 * shelvingCoeff) * highVar + (highVar ** 2)) /\
                      (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.b1Low = (2 * (shelvingCoeff * (lowVar ** 2) - 1)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b1High = (2 * ((highVar ** 2) - shelvingCoeff)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.b2Low = (1 - math.sqrt(2) * lowVar + (lowVar ** 2)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b2High = (shelvingCoeff - math.sqrt(2 * shelvingCoeff) * highVar + (highVar ** 2)) /\
                      (1 + math.sqrt(2) * highVar + (highVar ** 2))
        # skip a0 for both high and low filters
        self.a1Low = (2 * ((lowVar ** 2) - 1)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.a1High = (2 * ((highVar ** 2) - 1)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.a2Low = (1 - math.sqrt(2) * lowVar + (lowVar ** 2)) / (1 + math.sqrt(2 * lowVar) + (lowVar ** 2))
        self.a2High = (1 - math.sqrt(2) * highVar + (highVar ** 2)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        # set peak filter frequencies
        self.peakFreq = 20000
        # set gain for peak filter
        self.dbGainPeak = 1
        self.peakConst = 0                                                  # TODO: update val
        # peak filter constant(s)
        peakVar = math.tan(math.pi * self.dbGainPeak / self.wf.getframerate())
        peakCoeff = 10 ** (self.dbGainPeak / 20)
        # peak filter's equations:
        self.b0Peak = (1 + (peakCoeff / self.peakConst) * peakVar + (peakVar ** 2)) /\
                      (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.b1Peak = (2 * ((peakVar ** 2) - 1)) / (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.b2Peak = (1 - (peakCoeff / self.peakConst) * peakVar + (peakVar ** 2)) /\
                      (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        # once again, no a0
        self.a1Peak = (2 * ((peakVar **2) - 1)) / (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.a2peak = (1 - (1 / self.peakConst) * peakVar + (peakVar ** 2)) /\
                      (1 + (1/self.peakConst) * peakVar + (peakVar ** 2))

def implementFilters(self):
    global FreqGain
    # start audio stream                                                      TODO: fix to initialize with proper vars
    wavFileOpen = pyaudio.PyAudio()
    wavFile = wavFileOpen.open(format="FORMAT", channels="CHANNELS", rate="RATE", input="True",
                               frames_per_buffer="CHUNK")
    chunkSize = 0                                                           # TODO: find suitable chunk size
    # chunks for each part of filter
    chunks = [0 for n in range(chunkSize)]
    self.chunksLow = chunks
    self.chunksHigh = chunks
    self.chunksPeak = chunks
    chunksInFile = int(math.floor(self.wf.getnframes / chunkSize))
    # sort for ease of readability
    self.bLow = [self.b0Low, self.b1Low, self.b2Low]
    self.aLow = [self.a0, self.a1Low, self.a2Low]
    self.bHigh = [self.b0High, self.b1High, self.b2High]
    self.aHigh = [self.a0, self.a1High, self.a2High]
    self.bPeak = [self.b0Peak, self.b1Peak, self.b2Peak]
    self.aPeak = [self.a0, self.a1Peak, self.a2Peak]
    allFreq = list(FreqGain.keys())
    for i in range(chunksInFile):
        chunks = self.wf.readframes(chunkSize)
        buffer = struct.unpack ("h" * chunkSize, chunks)
        temp = buffer
        self.lowFilterVar = sp.signal.lfilter(self.bLow, self.aLow, temp)
        self.highFilterVar = sp.signal.lfilter(self.b0High, self.aHigh, self.lowFilterVar)
        self.peakFilterVar = sp.signal.lfilter(self.bPeak, self.aPeak, self.highFilterVar)
        temp = self.peakFilterVar
        temp = limitTo16Bit(temp, foo)                                      # TODO: set foo to correct depth
        stri = struct.pack('h'*chunkSize, *temp)
        wavFile.write(stri)
        # shelving and peak filters, adapted from audio eq cookbook
        # set cutoff frequencies for low and high shelf
        self.lowFreqShelving = allFreq[0]
        self.highFreqShelving = allFreq[2]
        # set gain for shelving filters
        self.dbGainShelving = 0
        # low shelving constant(s):
        lowVar = math.tan(math.pi * self.lowFreqShelving / self.wf.getframerate())  # getframerate() returns sample rate
        # high shelving constant(s):
        highVar = math.tan(math.pi * self.highFreqShelving / self.wf.getframerate())
        shelvingCoeff = 10 ** (self.dbGainShelving / 20)
        self.a0 = 1
        # shelving filters' equations:
        self.b0Low = (1 + math.sqrt(2 * shelvingCoeff) * lowVar + shelvingCoeff * (lowVar ** 2)) / \
                     (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b0High = (shelvingCoeff + math.sqrt(2 * shelvingCoeff) * highVar + (highVar ** 2)) / \
                      (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.b1Low = (2 * (shelvingCoeff * (lowVar ** 2) - 1)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b1High = (2 * ((highVar ** 2) - shelvingCoeff)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.b2Low = (1 - math.sqrt(2) * lowVar + (lowVar ** 2)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.b2High = (shelvingCoeff - math.sqrt(2 * shelvingCoeff) * highVar + (highVar ** 2)) / \
                      (1 + math.sqrt(2) * highVar + (highVar ** 2))
        # skip a0 for both high and low filters
        self.a1Low = (2 * ((lowVar ** 2) - 1)) / (1 + math.sqrt(2) * lowVar + (lowVar ** 2))
        self.a1High = (2 * ((highVar ** 2) - 1)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        self.a2Low = (1 - math.sqrt(2) * lowVar + (lowVar ** 2)) / (1 + math.sqrt(2 * lowVar) + (lowVar ** 2))
        self.a2High = (1 - math.sqrt(2) * highVar + (highVar ** 2)) / (1 + math.sqrt(2) * highVar + (highVar ** 2))
        # set peak filter frequencies
        self.peakFreq = allFreq[1]
        # set gain for peak filter
        self.dbGainPeak = 1
        self.peakConst = 0                                                  # TODO: update val
        # peak filter constant(s)
        peakVar = math.tan(math.pi * self.dbGainPeak / self.wf.getframerate())
        peakCoeff = 10 ** (self.dbGainPeak / 20)
        # peak filter's equations:
        self.b0Peak = (1 + (peakCoeff / self.peakConst) * peakVar + (peakVar ** 2)) / \
                      (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.b1Peak = (2 * ((peakVar ** 2) - 1)) / (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.b2Peak = (1 - (peakCoeff / self.peakConst) * peakVar + (peakVar ** 2)) / \
                      (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        # once again, no a0
        self.a1Peak = (2 * ((peakVar ** 2) - 1)) / (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.a2peak = (1 - (1 / self.peakConst) * peakVar + (peakVar ** 2)) / \
                      (1 + (1 / self.peakConst) * peakVar + (peakVar ** 2))
        self.bLow = [self.b0Low, self.b1Low, self.b2Low]
        self.aLow = [self.a0, self.a1Low, self.a2Low]
        self.bHigh = [self.b0High, self.b1High, self.b2High]
        self.aHigh = [self.a0, self.a1High, self.a2High]
        self.bPeak = [self.b0Peak, self.b1Peak, self.b2Peak]
        self.aPeak = [self.a0, self.a1Peak, self.a2Peak]
    wavFile.stop_stream()
    wavFile.close
    wavFileOpen.terminate()

# limits elements of n to a number of at most a specific number of bits
def limitTo16Bit(n, bits):
    x = 2**bits
    for i in range(len(n)):
        if n[i] > (x / 2):
            n[i] = (x/2)
        elif n[i] < (-1 * x / 2):
            n[i] = (-1 * x / 2)
    return n
