#!/usr/bin/env python

'''
Demonstration functions for rading in atm waveforms
Requires h5py (http://docs.h5py.org/en/latest/quick.html)
Initial functions provided by Matt Linkswiler and the ATM team

'''
import sys, os, glob, h5py, time
import numpy as np
from pylab import *


def printContents(name, item):
	'''
	print groups and datasets contained in HDF5 file
	'''
	l = len(name.split('/'))
	tab = l * '|  '
	tab = tab[:-2] + '--'
	if 'description' in f[name].attrs.keys(): # if item has a description, print item information with description
		print '{}{} ({}) : {}'.format(tab, name.split('/')[-1], len(item), f[name].attrs['description'])
	else: # if no description, then leave that part out
		print '{}{} ({})'.format(tab, name.split('/')[-1], len(item))
	

def getWaveform(f):

	# Account for the fact that python begins indexing at 0, but HDF5 file starts indexing at 1
	index_base = 1
	
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
		#wfx, wfy = aF.getWaveform(f, i) # call waveform extraction function

		shot_gate_start = shot_gate_starts[i] # pointer to gate_len and gate_pos
		num_gates = num_gatess[i] # number of gates for laser shot
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
		waveforms_x.append(waveformx)
		waveforms_y.append(waveformy)

	return waveforms_x, waveforms_y, num_gatess
