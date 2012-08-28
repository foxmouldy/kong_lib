from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser

def get_chans(msfile, fi=1418e06, di=100):
	'''
	For msfile, takes a desired frequency (in Hz) 
	and returns the lower and upper bounds for a 
	window on either side of fi, in lengths of di
	'''
	tb.open(msfile+'/SPECTRAL_WINDOW');
	f1 = chan_freq = tb.getcol('CHAN_FREQ')[0];
	df = tb.getcol('CHAN_WIDTH')[0];
	i = pl.round_((f1-fi)/df);
	tb.close();
	spw_lower  = i - di; spw_upper = i + di; 
	if spw_lower < 0:
		spw_lower = 0;
		spw_upper = 200;
	return(str(int(spw_lower)), str(int(spw_upper)));
