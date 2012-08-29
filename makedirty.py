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
parser.add_option("--vis", type = 'string', dest = 'vis', default=None, 
	help = 'Input MS to be imaged');

# sources to be imaged
parser.add_option("--sources", type='string', dest='sources', default=None, 
	help = "Sources to be imaged src1,src2,src3....[None]")

# output tag
parser.add_option("--tag", type='string', dest='tag', default=None, 
	help = "Tag for output images [vistag]");

# cellsize 
parser.add_option("--cell", type='string', dest='cell', default='30.0arcsec', 
	help = "Cell size for image [30.0arcsec]");

parser.add_option("--imspw", type='string', dest='imspw', default='', 
	help = 'Channels to be imaged [0:all]')

(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

if options.tag!=None: 
	tag = options.tag;
else:
	tag = options.vis;

split(vis = options.vis, outputvis = options.vis.replace('.ms','')+'.corrected.ms', 
	datacolumn = 'corrected', field = options.sources, spw=options.imspw);

for source in options.sources.split(','):
	print "\n"
	print "Making dirty image for source "+source;
	print "\n"
	clean(vis=options.vis.replace('.ms','')+'.corrected.ms', imagename=tag+'.src'+source+'.'+'dirty', niter=0, 
		cell = options.cell, spw=options.imspw);


