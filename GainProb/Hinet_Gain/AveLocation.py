# Compute the average location of all HiNet stations (latitude, longitude) in degrees

from HinetPy import Client

client=Client("msseo97", "minseong97") # User login
stations = client.get_station_list('0101') # Get all the station info of HiNet
lat_sum, long_sum, count=0, 0, 0

for station in stations:
	lat_sum += station.latitude
	long_sum += station.longitude
	count += 1

	print(station)

lat_ave=lat_sum / count
long_ave=long_sum / count
print(f"Average Latitude: {lat_ave}")
print(f"Average Longitude: {long_ave}")
