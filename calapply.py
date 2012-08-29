import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser 

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# vis
parser.add_option('--vis', type='string', dest = 'vis', default=None, 
	help = 'Input MS [None]');

# ftable 
#parser.add_option('--ftable', type='string', dest='ftable', default=None, 
#	help = 'Flux table to be applied [None]')

# btable 
parser.add_option('--tables', type='string', dest='btable', default=None, 
	help = 'Cal tables to be applied. [None]')

# cal
parser.add_option('--cal', type='string', dest='cal', default=None, 
	help = 'Calibrator [None]');

# cal2
parser.add_option('--cal2', type='string', dest='cal2', default='',
	help = 'Second Calibrator to Solve for. [None]')

# source
parser.add_option('--source', type='string', dest='source', default='', 
	help = 'Sources over which to apply the calibration. [None]')

# gaspw
parser.add_option('--gaspw', type='string', dest='gaspw', default='', 
	help = 'spw over which to apply the calibrations');

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
		parser.print_help();
		dummy = sys.exit(0);

applycal(vis = options.vis, gaintable = options.tables.split(','), 
	gainfield = [options.cal2, '*'], interp = ['linear', 'nearest'], 
	field = options.cal2+','+options.source, spw=options.gaspw);

applycal(vis = options.vis, gaintable = options.tables.split(','), 
	gainfield = [options.cal, '*'], interp = ['linear', 'nearest'], 
	field = options.cal, spw=options.gaspw);
