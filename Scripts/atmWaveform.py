#!/usr/bin/env python

'''
Demonstration script to read waveforms from ATM HDF5 files
Requires h5py (http://docs.h5py.org/en/latest/quick.html)

'''
import sys, os, glob, h5py, time
import numpy as np
from pylab import *

# Function to print groups and datasets contained in HDF5 file
def printContents(name, item):
	l = len(name.split('/'))
	tab = l * '|  '
	tab = tab[:-2] + '--'
	if 'description' in f[name].attrs.keys(): # if item has a description, print item information with description
		print '{}{} ({}) : {}'.format(tab, name.split('/')[-1], len(item), f[name].attrs['description'])
	else: # if no description, then leave that part out
		print '{}{} ({})'.format(tab, name.split('/')[-1], len(item))
	
# Function to retrieve waveform
def getWaveform(ii):
	'''
	Retrieve waveform information and pointers for specific laser shot
	'''
	shot_gate_start = shot_gate_starts[ii] # pointer to gate_len and gate_pos
	num_gates = num_gatess[ii] # number of gates for laser shot
	gate_len = gate_lens[shot_gate_start:shot_gate_start+num_gates] # list of gate lengths for each gate in waveform
	gate_pos = gate_poss[shot_gate_start:shot_gate_start+num_gates] # list of sample position for each gate in waveform
	wf_pointer = wf_pointers[shot_gate_start] - index_base # pointer to wvfm_amplitude to retrieve amplitudes for first gate
	waveformx, waveformy = [], [] # initialize empty lists to hold waveform x- and y-values for each gate
	for gate in range(num_gates): # loop through each gate in waveform
		wfx = np.arange(float(gate_pos[gate]), gate_pos[gate]+gate_len[gate]) # create an array for gate x-values
		wfy = wf_amps[wf_pointer:wf_pointer+gate_len[gate]] # extract waveform amplitudes from wf_pointer to wf_pointer+gate_len
		waveformy.append(wfy) # add current gate y-values to list
		waveformx.append(wfx) # add current gate x-values to list
		wf_pointer = wf_pointer+gate_len[gate] # increment wf_pointer to start of next gate
	return waveformx, waveformy

# Account for the fact that python begins indexing at 0, but HDF5 file starts indexing at 1
index_base = 1

# Get filename from arguments
for arg in sys.argv:
	if arg.endswith('.h5'):
		filename = arg

filename='../Data/ILATM1B_20170309_133117.atm6AT6.snippet.h5'
# Open HDF5 file for reading
f = h5py.File(filename, 'r')

# Print contents of HDF5 file
print '\n{0}\nContents of {1}:\n{0}'.format('='*50, filename)
f.visititems(printContents) # method to iterate through each item in the HDF5 file and calls "printContents" func on each
print

# Load waveform-specific parameters from HDF5 file
shot_gate_starts = f['waveforms/twv/shot/gate_start'][:] - index_base # pointers to gate_len and gate_pos for each laser shot
num_gatess = f['waveforms/twv/shot/gate_count'][:] # number of gates for each laser shot
gate_lens = f['waveforms/twv/gate/wvfm_length'][:] # number of samples in the gate for each gate
gate_poss = f['waveforms/twv/gate/position'][:] # sample position for the start of each gate
wf_pointers = f['waveforms/twv/gate/wvfm_start'][:] # pointer to wvfm_amplitude to retrieve amplitudes for each gate
wf_amps = f['waveforms/twv/wvfm/amplitude'][:] # waveform amplitude values

# Examples of loading other useful parameters (unused in this script)
utc = f['time/seconds_of_day'][:]  # UTC seconds of day

# Loop through all laser shot records and extract waveforms
nrec = len(utc) # calculate number of laser shot records
waveforms_x, waveforms_y = [], [] # initialize empty lists to hold x- and y- values for waveforms
for i in range(nrec):  # loop through laser shots...
	wfx, wfy = getWaveform(i) # call waveform extraction function
	waveforms_x.append(wfx)
	waveforms_y.append(wfy)

# To access the waveform from the first laser shot:
waveforms_y[0] # list containing a list of amplitude values (one sublist for each gate in the waveform)
waveforms_x[0] # list containing a list of digitizer sample positions (one sublist for each gate in the waveform)

# This snippet will output the waveform gates from the first 20 laser shots to the screen
for w,wfy in enumerate(waveforms_y): # loop through waveforms
	print
	for g,wf in enumerate(wfy): # loop through gates in waveform
		print 'Waveform {}, Gate {} ({} samples)'.format(w+index_base, g+index_base, len(wf))
		print wf
	if w > 20:
		break

cmap = cm.viridis                            


fig, axs = plt.subplots(nrows=3, ncols=4, figsize=(8, 8))

i=0
for ax in axs.flatten():
	print ax
	sca(ax)
	c_colors = cmap(np.linspace(0, 1, num_gatess[i]))
	for x in xrange(num_gatess[i]):
		plot(waveforms_y[i][x], color=c_colors[x])
		#plot(waveforms_y[i][1], color='r')
	i+=1
plt.tight_layout()
savefig('../Figures/testWaveform.jpg')









		