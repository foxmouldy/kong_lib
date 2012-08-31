import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser 

usage = "usage: %prog options\n\n"
usage = usage+"kalreduce.py performs the following: \n"
usage = usage+ "setjy --> gaincal (ini phase) --> gaincal (K) --> bandpass --> gaincal (amp&phase) --> fluxscale \n"
usage = usage+ "Differs from calreduce.py with Initial Phase Cal and K Correction. \n"
parser = OptionParser(usage=usage);

parser.add_option('--vis', type='string', dest = 'vis', default=None, 
	help = 'Input MS [None]');
parser.add_option('--cal', type='string', dest='cal', default=None, 
	help = 'Calibrator [None]');
parser.add_option('--cal2', type='string', dest='cal2', default='',
	help = 'Second Calibrator to Solve for [None]')
parser.add_option('--ipspw', type='string', dest='ipspw', default='0:1900~2100', 
	help = 'SPW for initial phase cal [0:1900~2100]')
parser.add_option('--gaspw', type='string', dest='gaspw', default=None, 
	help = 'SPW over which to solve for gain solutions [ALL]');
parser.add_option('--tag', type='string', dest='tag', default=None, 
	help = 'Optional prefix tag for table naming [None]')
parser.add_option('--refant', type='string', dest='refant', default='ant5', 
	help = 'Reference antenna for calibration [ant5]')
parser.add_option("--gasolint", type='string', dest='gasolint', default='inf', 
	help = 'Solution interval to be used when doing gaincal [\'inf\']')
parser.add_option("--ksolint", type='string', dest='ksolint', default='inf', 
	help = "Solution interval over which to track K delays [inf]")

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
		parser.print_help();
		dummy = sys.exit(0);

if options.tag!=None: 
	prefix = options.tag;
else:
	prefix = options.vis;

giptable = prefix+'.kr.iptable';
ktable = prefix+'.kr.ktable';
btable = prefix+'.kr.btable';
gtable = prefix+'.kr.gtable';
ftable = prefix+'.kr.ftable';

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
print '-----------------'
print 'Running GAINCAL'
print "Initial Phase Cal"
print '-----------------'
print '\n'

gaincal(vis = options.vis, caltable = giptable, field = options.cal+','+options.cal2, 
	refant = options.refant, spw= options.ipspw, gaintype='G', calmode='p', solint='int')

print '\n'
print '-----------------'
print 'Running GAINCAL'
print "K Correction"
print '-----------------'
print '\n'

gaincal(vis = options.vis, caltable = ktable, field=options.cal, refant = options.refant, 
	spw = options.gaspw, gaintype = 'K', solint=options.ksolint, combine='scan', 
	gaintable = giptable);

print '\n'
print '----------------'
print 'Running BANDPASS'
print '----------------'
print '\n'

bandpass(vis = options.vis, caltable = btable, interp = '', 
	field = options.cal, solint = 'inf', combine = 'scan', 
	refant = options.refant, gaintable = [giptable, ktable], minsnr=3.0);

print '\n'
print '----------------'
print 'Running GAINCAL'
print '----------------'
print '\n'

fields = options.cal+','+options.cal2;

gaincal(vis = options.vis, caltable=gtable, field=fields, 
	interp='nearest', spw=options.gaspw, solint=options.gasolint, 
	refant = options.refant, gaintable = [btable, ktable], minsnr=3.0);

fluxscale(vis = options.vis, fluxtable = ftable, caltable = gtable, 
	reference = options.cal, transfer = options.cal2);
