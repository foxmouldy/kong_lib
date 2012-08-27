import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser 

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

parser.add_option('--vis', type='string', dest = 'vis', default=None, 
	help = 'Input MS [None]');
parser.add_option('--cal', type='string', dest='cal', default=None, 
	help = 'Calibrator [None]');
parser.add_option('--cal2', type='string', dest='cal2', default='',
	help = 'Second Calibrator to Solve for [None]')
parser.add_option('--gaspw', type='string', dest='gaspw', default=None, 
	help = 'SPW over which to solve for gain solutions [ALL]');
parser.add_option('--tag', type='string', dest='tag', default=None, 
	help = 'Optional prefix tag for table naming [None]')


(options, args) = parser.parse_args();

if len(sys.argv)==1: 
		parser.print_help();
		dummy = sys.exit(0);

if options.tag!=None: 
	prefix = options.tag;
else:
	prefix = options.vis;

btable = prefix+'.'+options.cal+'.calreduce.B0';
gtable = prefix+'.'+options.cal+'.'+options.cal2+'.calreduce.G0';
ftable = prefix+'.'+options.cal+'.'+options.cal2+'.calreduce.F0';

print '\n'
print '-------------'
print 'Running SETJY'
print '-------------'
print '\n'

if options.cal=='1018-317':
	setjy(vis = options.vis, field = options.cal, fluxdensity=[3.17,0.,0.,0.]);
else:
	setjy(vis = options.vis, field = options.cal);

print '\n'
print '----------------'
print 'Running BANDPASS'
print '----------------'
print '\n'

bandpass(vis = options.vis, caltable = btable, interp = '', 
	field = options.cal, solint = 'inf', combine = 'scan', 
	refant = 'ant3', minsnr=3.0);

print '\n'
print '-------------'
print 'Running GAINCAL'
print '-------------'
print '\n'

fields = options.cal+','+options.cal2;

gaincal(vis = options.vis, caltable=gtable, field=fields, 
	interp='nearest', spw=options.gaspw, solint='int', 
	refant = 'ant3', gaintable = btable, minsnr=3.0);

fluxscale(vis = options.vis, fluxtable = ftable, caltable = gtable, 
	reference = options.cal, transfer = options.cal2);