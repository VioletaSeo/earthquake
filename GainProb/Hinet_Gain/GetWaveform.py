# Calculate particle motions (P and S) of teleseismic earthquakes detected by the HiNet staion
# Date range: 2004/01/01-2016/04/30
# Magnitude range: M_w>=6.0, Distance range: 30<=d<=90 degrees from the reference coordinate
# SNR ratio>=2.0 (How to calculate?)
# Use obspy.signal.polarization.particle_motion_odr to calculate particle motion of trace form the P, S onset

# Import necessary libraries
from obspy.core.stream import Stream
from obspy.signal.polarization import particle_motion_odr
from obspy.clients.fdsn import Client
from obspy.core.utcdatetime import UTCDateTime
from obspy.taup import TauPyModel
from obspy.geodetics.base import locations2degrees

# Get lists of teleseismic earthquakes satisfying the conditions
client=Client("IRIS")
cat=client.get_events(starttime=UTCDateTime(2004, 1, 1, 0, 0, 0), endtime=UTCDateTime(2016, 4, 30, 23, 59, 59), latitude=36.80060501882054, longitude=137.6569971141782, 
	mindepth=60, minmagnitude=6, minradius=30, maxradius=90)
print(cat)

# Calculate travel time for the accurate picking of onset from teleseismic waveform
p_tttable=[]
s_tttable=[]
sta_lat, sta_long = 35.5038, 136.7939 # latitude and longitude of specified station (N.TKTH)
model = TauPyModel(model="iasp91")
for i in range(len(cat)):
	distance=locations2degrees(sta_lat, sta_long, cat[i].origins[0].latitude, cat[i].origins[0].longitude)
	parrivals = model.get_travel_times(source_depth_in_km=cat[i].origins[0].depth/1000, distance_in_degree=distance, phase_list=['P'])
	sarrivals = model.get_travel_times(source_depth_in_km=cat[i].origins[0].depth/1000, distance_in_degree=distance, phase_list=['S'])
	p_time=parrivals[0].time
	s_time=sarrivals[0].time
	p_tttable.append(p_time)
	s_tttable.append(s_time)

# Get P and S onset time of each earthquakes
p_starttime=[]
s_starttime=[]

for i in range(len(cat)):
	dt=cat[i].origins[0].time
	p_utc_dt=dt+32400+p_tttable[i]-10 # Convert UTC datetime to Japan regional time which is suitable for HinetPy data downloading and add P traveltime
	s_utc_dt=dt+32400+s_tttable[i]-10 # Convert UTC datetime to Japan regional time which is suitable for HinetPy data downloading and add S traveltime
	p_starttime.append(str(p_utc_dt)[0:4]+str(p_utc_dt)[5:7]+str(p_utc_dt)[8:10]+str(p_utc_dt)[11:13]+str(p_utc_dt)[14:16]+str(p_utc_dt)[17:19])
	s_starttime.append(str(s_utc_dt)[0:4]+str(s_utc_dt)[5:7]+str(s_utc_dt)[8:10]+str(s_utc_dt)[11:13]+str(s_utc_dt)[14:16]+str(s_utc_dt)[17:19])

# Make traces starting from P & S wave onset time based on calculated travel times

from HinetPy import Client, win32
client=Client("msseo97", "minseong97")
client.select_stations('0101', ['N.TKTH'])
for i in range(0, 99):
	data, ctable = client.get_continuous_waveform('0101', p_starttime[i], 20, outdir="P_data_TKTH")
	win32.extract_sac(data, ctable, suffix="", outdir=f"/home/msseo/2019-2020_Intern/GainProb/Hinet_Gain/P_data_TKTH/{i}", with_pz=True)
	data, ctable = client.get_continuous_waveform('0101', s_starttime[i], 20, outdir="S_data_TKTH")
	win32.extract_sac(data, ctable, suffix="", outdir=f"/home/msseo/2019-2020_Intern/GainProb/Hinet_Gain/S_data_TKTH/{i}", with_pz=True)
