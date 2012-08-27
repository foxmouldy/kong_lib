import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# visfile
parser.add_option("--vis", type='string', dest = 'vis', default=None, 
	help = 'MS to be flagged [None]');

# autocorrelations?
parser.add_option("--flagauto", type='string', dest = 'flagauto', 
	default=None, help='Flag autocorrelations? [False]')

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

if bool(options.flagauto.upper())==True:
	
	print "\n"
	print "Easy Flag!"
	print "Flagging Autocorrelations"
	print '\n'
	print '\n'
	flagautocorr(vis = msfile);

print '\n'
print 'Flagging Shadow\'d Visibilities'
print '\n'
print '\n'
tflagdata(vis = options.vis, mode='shadow');

print '\n'
print 'Running rflagger'
print '\n'
print '\n'
tflagdata(vis = options.vis, mode='rflag');

print '\n'
print 'DONE'
print '\n'
print '\n'
