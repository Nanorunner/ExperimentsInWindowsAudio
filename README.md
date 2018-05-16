# ExperimentsInWindowsAudio
Personal projects with audio, mainly various DSPs. <br /><br />
maineq.py is meant to be a basic equalizer for .wav files. It functions by taking a .csv file called FreqGain.csv with (currently 3) increasing (frequency, gain) pairs and altering said frequencies to match the gains mapped to it. <br />
As is, it only works with mono .wav files passed through and needs to be tweaked to function with the Windows audio stream <br />
This particular project is written with Python scipy and pyaudio.
