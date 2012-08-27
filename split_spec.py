import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser 
import brad_lib as br

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# Input MS
parser.add_option("--vis", type = 'string', dest = 'vis', default=None, 
	help = 'Input visibility to be splitted [None]');

# Output MS
parser.add_option("--splitvis", type='string', dest='splitvis', default=None, 
	help = 'Name of Splitted MS [None]')

# Centre Frequency 
parser.add_option('--fi', type = 'string', dest='fi', default=None, 
	help = "Centre frequency about which to extract MS [1418MHz]")

# Number of Channels
parser.add_option('di', type='string', dest='di', default=None, 
	help = 'Number of channels on either side of fi to subtract [100]')

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

spw_lower, spw_upper = br.get_chans(options.vis, fi=float(options.fi), 
	di = int(options.di))

print '\n'
print '\n'
print 'Splitting '+msfile+' from '+spw_lower+' to '+spw_upper;
print '\n'
print '\n'

split(vis = options.vis, 
	outputvis = options.splitvis, 
	datacolumn = 'data', 
	spw = '0:'+spw_lower+'~'+spw_upper);
