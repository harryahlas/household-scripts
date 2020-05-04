# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 20:01:52 2018

@author: Anyone
"""



'''
Works similar to detect silence in DAWs
In this instance we are splitting a single take from one microphone
would be useful say for splitting kick drum samples

First step
Import packages
'''

# waverdwave.py
import numpy as np
#from numpy import array
import struct
import wave
import matplotlib.pyplot as plt


'''
Function to read audio file
Works for this wave file, others may not work.
refer to 
Cameron MacLeod has a more robust method
https://www.cameronmacleod.com/blog/reading-wave-python
'''
def read_whole(filename):
    wav_r = wave.open(filename, 'r')
    ret = []
    while wav_r.tell() < wav_r.getnframes():
        decoded = struct.unpack("<h", wav_r.readframes(1))
        ret.append(decoded)
    return ret

'''
# Import recorded file with drum sample hits
Again, this would be someone doing single hits on a kick drum for instance
You can see 17 distinct hits.  Goal is to split each one of these hits.
Incidentally, these samples were created using my daughters' toy hand drum.  Doesn't sound too shabby!
'''
drum_samples = read_whole("C:\Development\Python\encoder_decoder\encoder_decoder_sounds\Audio\drum_only_01.wav")

plt.plot(drum_samples)

'''
Let's look closer at one of the hits.  You can see there is a sudden spike When the initial attack of the drum sample hits followed by a gradual descent.  
Note the numbers are positive and negative.  
'''
plt.plot(drum_samples[527000:550000])
'''
So how do we identify hitpoints?
Next we need to identify hitpoints.  we are looking for that sudden jump.
Probably a lot of ways to do it.  I elected to look at the moving average.

You may be asking Why moving average? Why not just look at a certain threshold.  The logic behind the decision was to account for any sporadic noise that may pop up.  The moving average seemed more robust.

However, as I noted, there are both positive and negative values.  So the moving average will always be somewhere around 0.
So, what we can do instead is look at the absolute value of the waves.
'''
# Determine hitpoints by looking at the moving average of absolute values
drum_samples_abs = np.array(drum_samples)
drum_samples_abs = [abs(number) for number in drum_samples_abs] 

'''
Note the values in drum_samples_abs are all 0 or greater, which will make it easier for us to calculate a moving average and identify spikes.
Here is the same hit:
'''
# can remove
plt.plot(drum_samples_abs[527000:550000])


'''
Now we'll create the movint average
I somewhat arbitrarily chose 1000 samples. 
Then create a function to calculate the moving average.
In the graph you can clearly see the 17 hits.
'''
moving_average_window = 1000


# IF that doesn't work then use this. This is the original but i am concerned it may not work on long files.  Keep both?
def moving_average(a, n = moving_average_window) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

drum_samples_moving_average = moving_average(drum_samples_abs, n = moving_average_window)

plt.plot(drum_samples_moving_average)


'''
This section identifies hitpoints 
First set up a hitpoint list
Then look at the moving average and see when it exceeds a threshold (min_moving_avg_value, in this case 1000)
So it looks for the first time the moving average is at least 1000.
it then creates a hitpoint back 200 samples (the buffer to account for the moving average)
Then skips ahead the single_drum_sample_length number of samples to make sure it doesn't count the same hit twice.
There are 44100 samples in a second so 8820 samples is 1/5 of a second. 
These values worked for me but I would encourage you to toy with these values if you want to improve your results
'''

min_moving_avg_value = 1000
single_drum_sample_length = 8820
hitpoint_buffer = 200

hitpoints = []
last_endpoint = 0

for i in range(len(drum_samples_moving_average)):
    if i < last_endpoint:
        continue
    if drum_samples_moving_average[i] > min_moving_avg_value:
        hitpoints.append(i + moving_average_window - hitpoint_buffer) # Move hitpoint to start of sample 
        last_endpoint = i + single_drum_sample_length

'''
Here you can see the time of each hitpoint
'''
for hitpoint in hitpoints:
    print(round(hitpoint/44100,2), "seconds")

'''
Here is what the 10th sample will look like:
'''
testpoint = 10
plt.plot(drum_samples[hitpoints[testpoint]:hitpoints[testpoint] + single_drum_sample_length])


version_number = "001"
version_name = "zztoss"

###old:
#
#    ifile = wave.open("C:\Development\Python\encoder_decoder\encoder_decoder_sounds\Audio\drum_sample-01.wav")
#sampwidth = ifile.getsampwidth()
#ifile.close() 
#fmts = (None, "=B", "=h", None, "=l")
#fmt = fmts[sampwidth]
#dcs  = (None, 128, 0, None, 0)
#dc = dcs[sampwidth]
#
#sample_number = 0

#for sample_number in range(len(hitpoints)):
#    #print sample
#    ofile = wave.open("C:\Development\Python\encoder_decoder\encoder_decoder_sounds\Audio\\" + version_name + version_number + str(sample_number) + ".wav", "w")
#    ofile.setparams(ifile.getparams())
#    
#    f = drum_samples[hitpoints[sample_number]:hitpoints[sample_number] + single_drum_sample_length]
#    f = np.array(f)
#    f = f.astype('int16')
#    f = f.reshape(single_drum_sample_length)
#    for i in range(len(f)):
#        oframe = f[i]
#        oframe += dc
#        oframe = struct.pack(fmt, oframe)
#        ofile.writeframes(oframe)
#    ofile.close()

''' Formatting for wave output'''
sampwidth = 2
fmts = (None, "=B", "=h", None, "=l")
fmt = fmts[sampwidth]
dcs  = (None, 128, 0, None, 0)
dc = dcs[sampwidth]

sample_number = 0

''' Print out the hits'''

for sample_number in range(len(hitpoints)):
    ofile = wave.open("C:\Development\Python\encoder_decoder\encoder_decoder_sounds\Audio\\" + version_name + version_number + "-" + str(sample_number) + ".wav", "w")
    ofile.setparams((1, 2, 44100, 8820, 'NONE', 'not compressed'))
    #(nchannels=1, sampwidth=2, framerate=44100, nframes=8820, comptype='NONE', compname='not compressed')

    f = drum_samples[hitpoints[sample_number]:hitpoints[sample_number] + single_drum_sample_length]
    f = np.array(f)
    f = f.astype('int16')
    f = f.reshape(single_drum_sample_length)
    for i in range(len(f)):
        oframe = f[i]
        oframe += dc
        oframe = struct.pack(fmt, oframe)
        ofile.writeframes(oframe)
    ofile.close()


