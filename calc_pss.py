import sys
from tasks import *
from taskinit import *
import casac
import pylab as pl
import os
from optparse import OptionParser

usage = "usage: %prog options"
parser = OptionParser(usage=usage);

# Input Visibility
parser.add_option("--vis", type = 'string', dest='vis', default=None, 
	help = "Input Visibility [None]");
# Tsys
parser.add_option("--tsys", type = 'float', dest = 'tsys', default=30.0, 
	help = 'Tsys [30K]');
# General Efficiency
parser.add_option('--eff', type='float', dest = 'eff', default='0.7', 
	help = 'Overall Efficiency for the Telescope [0.7]');
# Field ID 
parser.add_option('--field-id', type='int', dest = 'field_id', default = 0, 
	help = 'Field for which to calculate pss [0]');


(options, args) = parser.parse_args();

if len(sys.argv)==1: 
	parser.print_help();
	dummy = sys.exit(0);




# Boltzmann's Constant, Converting to Jy
k = 1.38e03;

# Get Number of Antennas N:
tb.open(options.vis+'/ANTENNA');
N = len(tb.getcol('NAME'));

# Get Dish Diameter
D = tb.getcol('DISH_DIAMETER')[0]; 
A = pl.pi*(D/2.)**2;
tb.close();

# Get Total Bandwidth dv
tb.open(options.vis+'/SPECTRAL_WINDOW');
dv = tb.getcol('TOTAL_BANDWIDTH')[0];
Nchan = tb.getcol('NUM_CHAN')[0];
dv_per_chan = tb.getcol('CHAN_WIDTH')
tb.close();

# Total Integration Time
tb.open(options.vis);
Nints = len(pl.where(tb.getcol('FIELD_ID')==options.field_id)[0]);
dt = tb.getcol('EXPOSURE')[0];
T = Nints * dt; #

pss_N = pl.sqrt(2)*options.tsys*k;
pss_D = options.eff * A * pl.sqrt(N*(N-1)*dv*T);
pss = pss_N / pss_D;

pss_D_per_chan = options.eff * A * pl.sqrt(N*(N-1)*dv_per_chan*T);
pss_per_chan = pss_N / pss_D_per_chan;

print "\n"
print "\n"
print "Point Source Sensitivity Parameters for Source "+str(options.field_id);
print "-------------------------------------------------"
print "Total Integration Time [s] = "+str(T);
print "Total Bandwidth [Hz] = "+str(dv);
print "Number of Channels = "+str(Nchan);
print "Number of Antennas = "+str(N);
print "Approximate Dish Area [m^2] = "+str(A);
print "User Input Tsys [K] = "+str(options.tsys);
print "\n"
print "Point Source Sensitivity [Jy] = "+str(pss);
print "Point Source Sensitivity per channel [Jy] = "+str(pss_per_chan);
