#!/usr/bin/env python

'''
Demonstration functions for rading in atm waveforms
Requires h5py (http://docs.h5py.org/en/latest/quick.html)
Provided by the ATM team

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
	

def getWaveform(ii):
	
	# Account for the fact that python begins indexing at 0, but HDF5 file starts indexing at 1
	index_base = 1

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
