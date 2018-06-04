# ExperimentsInWindowsAudio
Personal projects with audio, mainly various DSPs. Will tie everything together at some point.<br /><br />
maineq.py is meant to be a basic equalizer for .wav files. It functions by taking a .csv file called FreqGain.csv with (currently 3) increasing (frequency, gain) pairs and altering said frequencies to match the gains mapped to it. <br />
As is, it only works with mono .wav files passed through and needs to be tweaked to function with the Windows audio stream <br />
This particular file is written with Python scipy and pyaudio.<br /><br />
realtimeprocessing.py is a very basic framework with two implementations of real time audio processing, one using the native functions in pyaudio, and the other using double buffering and threading to modify and write to two buffers at the same time and then swap them and repeat until stream ends. If it's not working for whatever reason make sure you updated all the placeholder values to what you need them to be.<br /><br />

showAudioDeviceIndicies displays the indicies of the first 100 audio dievices on your corrent machine, for use with selecting which device to point pyaudio at.<br /><br />
easyVuMeter is a quick and dirty left and right vu meters in the console window.<br /><br />
