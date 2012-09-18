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
tb.close();

# Total Integration Time
tb.open(options.vis);
Nints = len(pl.where(tb.getcol('FIELD_ID')==options.field_id)[0]);
dt = tb.getcol('EXPOSURE')[0];
T = Nints * dt; #

pss_N = pl.sqrt(2)*options.tsys*k;
pss_D = options.eff * A * pl.sqrt(N*(N-1)*dv*T);
pss = pss_N / pss_D;

print "\n"
print "\n"
print "Point Source Sensitivity Parameters for Source "+str(options.field_id);
print "-------------------------------------------------"
print "Total Integration Time [s] = "+str(T);
print "Total Bandwidth [Hz] = "+str(dv);
print "Number of Antennas = "+str(N);
print "Approximate Dish Area [m^2] = "+str(A);
print "User Input Tsys [K] = "+str(options.tsys);
print "\n"
print "Point Source Sensitivity [Jy] = "+str(pss);

'''
To get number of antennas: 
tb.open('1347704083.hh_vv.sc0to95.spw500to3500.ms/ANTENNA');
N = len(tb.getcol('NAME')

'''

''''
tb.colnames()
  Out[97]: 
['UVW',
 'FLAG',
 'FLAG_CATEGORY',
 'WEIGHT',
 'SIGMA',
 'ANTENNA1',
 'ANTENNA2',
 'ARRAY_ID',
 'DATA_DESC_ID',
 'EXPOSURE',
 'FEED1',
 'FEED2',
 'FIELD_ID',
 'FLAG_ROW',
 'INTERVAL',
 'OBSERVATION_ID',
 'PROCESSOR_ID',
 'SCAN_NUMBER',
 'STATE_ID',
 'TIME',
 'TIME_CENTROID',
 'DATA',
 'WEIGHT_SPECTRUM',
 'MODEL_DATA',
 'CORRECTED_DATA']

 tb.getcol('FIELD_ID')==3

tb.getdesc()
  Out[33]: 
{'DISH_DIAMETER': {'comment': 'Physical diameter of dish',
                   'dataManagerGroup': 'StandardStMan',
                   'dataManagerType': 'StandardStMan',
                   'maxlen': 0,
                   'option': 0,
                   'valueType': 'double'},
 'FLAG_ROW': {'comment': 'Flag for this row',
              'dataManagerGroup': 'StandardStMan',
              'dataManagerType': 'StandardStMan',
              'maxlen': 0,
              'option': 0,
              'valueType': 'boolean'},
 'MOUNT': {'comment': 'Mount type e.g. alt-az, equatorial, etc.',
           'dataManagerGroup': 'StandardStMan',
           'dataManagerType': 'StandardStMan',
           'maxlen': 0,
           'option': 0,
           'valueType': 'string'},
 'NAME': {'comment': 'Antenna name, e.g. VLA22, CA03',
          'dataManagerGroup': 'StandardStMan',
          'dataManagerType': 'StandardStMan',
          'maxlen': 0,
          'option': 0,
          'valueType': 'string'},
 'OFFSET': {'comment': 'Axes offset of mount to FEED REFERENCE point',
            'dataManagerGroup': 'StandardStMan',
            'dataManagerType': 'StandardStMan',
            'maxlen': 0,
            'ndim': 1,
            'option': 5,
            'shape': array([3], dtype=int32),
            'valueType': 'double'},
 'POSITION': {'comment': 'Antenna X,Y,Z phase reference position',
              'dataManagerGroup': 'StandardStMan',
              'dataManagerType': 'StandardStMan',
              'maxlen': 0,
              'ndim': 1,
              'option': 5,
              'shape': array([3], dtype=int32),
              'valueType': 'double'},
 'STATION': {'comment': 'Station (antenna pad) name',
             'dataManagerGroup': 'StandardStMan',
             'dataManagerType': 'StandardStMan',
             'maxlen': 0,
             'option': 0,
             'valueType': 'string'},
 'TYPE': {'comment': 'Antenna type (e.g. SPACE-BASED)',
          'dataManagerGroup': 'StandardStMan',
          'dataManagerType': 'StandardStMan',
          'maxlen': 0,
          'option': 0,
          'valueType': 'string'},
 '_define_hypercolumn_': {}}

 
'''

