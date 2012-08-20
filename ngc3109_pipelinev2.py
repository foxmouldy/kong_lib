import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser 
# Bradley Frank, July 2012
# For use NGC3109 data, observed in WBC8k with KAT-7

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

parser.add_option("--tag", type = 'string', dest = 'tag', default=None, 
	help = 'File tag to use in this run');
parser.add_option("--retag", type='string', dest = 'retag', default=None, 
	help = 'New tag to use');
parser.add_option("--calls", type='string', dest = 'calls', default=None, 
	help = 'Custom pipeline (input each block in sequence)')
parser.add_option("--ui", type='string', dest='ui', default=None, 
	help = "Optional Settings File");
(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);

global ui;

def read_inps(fname):
	'''
	This reads in the inputs from the text file fname. Each line in the text file should
	contain the desired user-input. For example: 
	spw = 0:100~200
	will produce ui['spw'] = '0:100~200'
	'''
	f = open(fname);
	global ui;
	ui = {};
	for line in f: 
		k,v = line.strip().split('=');
		ui[k.strip()] = v.strip();
	f.close();
	return(ui);

def get_chans(msfile, fi=1418e06, di=100):
	'''
	For msfile, takes a desired frequency (in Hz) and returns the lower and upper bounds for a 
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

def set_jy():
	'''
	Single Standalone Application of Setjy on the ampfield
	'''
	setjy(vis = msfile, 
		field = ampfield);

def easy_flag():
	'''
	Just do the generic flagging. 
	'''
	print 'Clearing flags and previous calibration.'
	print '\n'
	print '\n'
	

	tflagdata(vis = msfile, 
		mode = 'unflag');
	clearcal(vis = msfile);
	print "\n"
	print "Easy Flag!"
	print "Flagging Autocorrelations"
	print '\n'
	print '\n'
	
	flagautocorr(vis = msfile); 

	ui['manualflag_spw'] = ui['manualflag_spw'].upper()=='TRUE';
	if ui['manualflag_spw']==True: 
		print '\n';
		print 'manualflag_spw == True ';
		print '\n';
		tflagdata(vis = msfile, 
			mode = 'manual', 
			spw = ui['mf_spw']);

	print "Flagging shadowed visibilities -> rflag -> tfcrop";
	print '\n'
	print '\n'
	
	tflagdata(vis = msfile, 
		mode = 'shadow');	
	tflagdata(vis = msfile, 
		mode = 'tfcrop');
	tflagdata(vis = msfile, 
		mode = 'rflag');

def heavy_flag():
	'''
	This is used to hammer the data into shape. Is useful if preceded with a good manual flag.  
	'''
	print '\n'
	print "Heavy Flagging"
	print '\n'
	tflagdata(vis = msfile, 
		mode = 'elevation', 
		lowerlimit = 5.0);
	# Source 0
	tflagdata(vis = msfile, 
		mode = 'tfcrop', 
		field = ampfield,
		combinescans = True, 
		datacolumn = 'data', 
		flagdimension = 'freq')
		#usewindowstats = 'both')
	# Source 1
	tflagdata(vis = msfile, 
		mode = 'tfcrop', 
		field = source,
		combinescans = True, 
		datacolumn = 'data', 
		flagdimension = 'freq'); 
		#usewindowstats = 'both')
	# Source 2
	tflagdata(vis = msfile, 
		mode = 'tfcrop', 
		field = phasefield,
		combinescans = True, 
		datacolumn = 'data', 
		flagdimension = 'freq') 
		#usewindowstats = 'both')

def easy_cal():
	print '\n'
	print 'Calibration'
	print '\n'
	clearcal(vis = msfile);	
	os.system('rm -r '+btable);
	os.system('rm -r '+ftable);
	os.system('rm -r '+gtable);
	# First we do setjy on the amplitude/flux/bandpass/primary calibrators. 
	setjy(vis = msfile, 
		field = ampfield);
	bandpass(vis = msfile, 
		caltable = btable, 
		interp = '', 
		field = ampfield, 
		bandtype = 'B', 
		solint = 'inf', 
		combine = 'scan', 
		refant = ref_ant);
	
	# Gain Calibration
	# We're going to average channels 150~200 
	gaincal(vis = msfile, 
		caltable = gtable, 
		gainfield = '', 
		gaintable = btable, 
		field = ampfield+','+phasefield,
		interp='nearest', 
		spw= ui['gaspw'], 
		solint = 'inf', 
		calmode='ap', 
		refant = ref_ant);
	
	# Fluxscale
	# This gives us our first indicator of whether our calibration is going well or not. 
	# The flux for 1018* is ~ 3.5Jy, so we want to get within this ballpark.
	
	fluxscale(vis = msfile, 
		fluxtable = ftable, 
		caltable = gtable, 
		reference = ampfield, 
		transfer = phasefield);
	
	applycal(vis = msfile, 
		gaintable = [ftable, btable], 
		gainfield = [phasefield, '*'],
		interp = ['linear', 'nearest'],
		field = phasefield+','+source);
	applycal(vis = msfile, 
		gaintable = [ftable, btable], 
		gainfield = [ampfield, '*']);
	
def split_spec():
	global tag, msfile, spw_lower, spw_upper, btable, gtable, ftable;
	spw_lower, spw_upper = get_chans(msfile, pl.float32(ui['fi']), int(ui['di']));
	print '\n'
	print '\n'
	print 'Splitting '+msfile+' from '+spw_lower+' to '+spw_upper;
	print '\n'
	print '\n'
	tag = options.retag+'.'+spw_lower+'to'+spw_upper;
	#print "breakpoint: split_spec"
	#print  tag
	split(vis = msfile, 
		outputvis = tag+'.ms', 
		datacolumn = 'data', 
		spw = '0:'+spw_lower+'~'+spw_upper);
	msfile = tag+'.ms';
	btable = tag+'.B0';
	gtable = tag+'.G0';
	ftable = tag+'.F0';

def split_sub():
	# Continuum Subtraction and splitting 
	global tag;
	splittag = tag+'.'+source+'.split';
	if os.path.exists(splittag+'.ms')==True: 
		print "\n"
		print 'Deleting Old Split MS'
		print "\n"
		os.system('rm -r '+splittag+'.ms');
	if os.path.exists(splittag+'.ms.contsub')==True: 
		print "\n"
		print "Deleting Old UVContSub'd MSs"
		print "\n"
		os.system('rm -r '+splittag+'.ms.cont*')
	print "\n"
	print 'Creating New Split MS'
	print "\n"
	split(vis = msfile, 
		outputvis = splittag+'.ms', 
		field = source, 
		spw = '', 
		datacolumn = 'corrected');
	print "\n"
	print 'Continuum Subtraction'
	print "\n"
	uvcontsub(vis = splittag+'.ms', 
		field = source, 
		fitspw = ui['fitspw'], 
		spw='0', 
		solint=0.0, 
		fitorder = 0, 
		want_cont = True);
	tag = splittag+'.ms';


def easy_im():
	print '\n'
	print '\n'
	print "Cleaning over Spectral Range"
	print '\n'
	print '\n'
	imname = options.retag+'.contsub.'+ui['niter']+'iters';  
	if os.path.exists(imname)==True: 
		print '\n';
		print 'Deleting old contsub image';
		print '\n'
		os.system('rm -r '+imname)
	clean(vis = tag+'.contsub', 
		imagename = imname,  
		field = source, 
		selectdata = False, 
		mode = 'channel', 
		niter = int(ui['niter']), 
		interactive = False, 
		imsize = int(ui['imsize']), 
		cell = ui['cell'], 
		restfreq = '1420.406MHz', 
		pbcor=ui['pbcor'], minpb=pl.float32(ui['minpb']));
	im.open(tag+'.contsub');
	pss = im.sensitivity();
	pss = pss['pointsource']['value']
	os.system('rm -r '+imname+'image.mom*')	
	immoments(imagename = imname+'.image', 
		moments = [0,1,2], 
		includepix = [5*pss,1000000], 
		outfile = imname+'.image.mom');
	im.close();
	
	print '\n'
	print '\n'
	print "Cleaning Continuum"
	print '\n'
	print '\n'
	imname = options.retag+'.cont.'+ui['niter']+'iters';
	if os.path.exists(imname)==True: 
		print '\n';
		print 'Deleting old cont image';
		print '\n'
		os.system('rm -r '+imname)
	clean(vis = tag+'.cont', 
		imagename = imname, 
		field = source, 
		selectdata = False, 
		mode = 'channel', 
		niter = int(ui['niter']), 
		interactive = False, 
		imsize = int(ui['imsize']), 
		cell = ui['cell'], 
		restfreq = '1420.406MHz',
		pbcor=ui['pbcor'], minpb=pl.float32(ui['minpb']));
	
	im.open(tag+'.contsub');
	os.system('rm -r '+imname+'image.mom*')	
	pss = im.sensitivity();
	pss = pss['pointsource']['value']
	immoments(imagename = imname+".image", 
		moments = [0,1,2], 
		includepix = [5*pss,1000000],
		outfile = imname+'.image.mom')
def plotem():
	'''
	Plotting subfunction, not included in the default pipeline. 
	Should be used if you want to do a quick 
	'''
	plotcal(caltable = btable, 
		field = ampfield, 
		subplot = 211, 
		yaxis = 'amp');
	plotcal(caltable = btable, 
		subplot = 212,
		yaxis = 'phase', 
		figfile = btable+'.png');


	plotcal(caltable = ftable, 
		field =  ampfield+','+phasefield,
		subplot = 211,
		yaxis = 'amp');
	plotcal(caltable = ftable,
		subplot = 212,
		yaxis = 'phase',
		figfile= ftable+'.png')

	# Plot the bandpass
	plotcal(caltable = btable, 
		field = ampfield, 
		subplot = 211, 
		yaxis = 'amp'); 
	plotcal(caltable = btable,
		subplot = 212,
		yaxis = 'phase',
		figfile= btable+'.png');

	plotxy(vis = msfile, 
		xaxis = 'phase', 
		yaxis = 'amp', 
		datacolumn = 'corrected', 
		field = ampfield, 
		interactive = False, 
		figfile = tag+'_amphase.'+ampfield+'.png')

	plotxy(vis = msfile, 
		xaxis = 'phase', 
		yaxis = 'amp', 
		datacolumn = 'corrected', 
		field = phasefield, 
		averagemode = 'vector', 
		width='100',
		interactive = False, 
		figfile = tag+'_amphase.'+phasefield+'.png')

	# Now plot the spectrum of the source
	plotxy(vis = msfile, 
		xaxis = 'frequency', 
		yaxis = 'amp', 
		datacolumn = 'corrected', 
		field = source, 
		averagemode='vector', 
		timebin = 'all', 
		crossscans = True, 
		crossbls = True, 
		restfreq = '1420.406MHz', 
		figfile = tag+'_spectrum.'+source+'.png');

	
global tag, msfile, btable, gtable, ftable, ampfield, phasefield, source, ref_ant, rest_freq, splitms

tag = options.tag; 
if options.retag==None: 
	options.retag=tag; 
msfile = options.tag+'.ms';
btable = options.retag+'.B0';
gtable = options.retag+'.G0';
ftable = options.retag+'.F0'; 
#ampfield = '1934*';
#phasefield = '1018*';
#source = 'NGC3109*';
rest_freq = '1420.406e06MHz'

global ui;
if options.ui!=None:
	ui = read_inps(options.ui);
else:
	if os.path.exists('ngc3109_pipelinesettings.txt')==False:
		print "Defaults not found. Copy from ~/brad_lib/ to . and try again :)"
		sys.exit(0);
	else: 
		ui = read_inps('ngc3109_pipelinesettings.txt');

ref_ant = ui['ref_ant'];
ui['pbcor'] = ui['pbcor'].upper()=='TRUE';
ampfield = ui['ampfield'];
phasefield = ui['phasefield'];
source = ui['source'];
#print msfile;
#sys.exit(0);

if options.calls!=None:
	for c in options.calls.split(','):
		exec(c+'()');
else:
	split_spec();
	set_jy();
	easy_flag();
	easy_cal();
	split_sub();
	easy_im();

