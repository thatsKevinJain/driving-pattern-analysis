'''
Author - Kevin Jain

DRIVING PATTERN ANALYSIS
This app will analyse the driving pattern of 1 driver who has completed 100 trips 
and will detect the signs of bad driving behavior patterns. 
These signs are as follows - 
1. Harsh acceleration
2. Harsh breaking
3. Ratio of vehicle speed to engine speed
4. Ratio of throttle position to vehicle speed
5. Excessive Engine Load
'''

# NUMPY #
import numpy as np

# Extract the CSV file and load it into NumPY Array # 
data = np.genfromtxt('train-obd2.csv', delimiter=',', skip_header=1)

# Get the total number of trips #
total_trips = int(data.shape[0]/1000) + 1

# Create an empty numpy array to store the results #
result = np.empty((int(total_trips), 7))

# Iterate the file and aggregate results for each trip #
# There are 100 trips for each driver #
def main():
	for trip_no in range(1, total_trips):

		print('Trip No. %d' %(trip_no))
		calculate_events(trip_no)
	else:
		save_results()

def calculate_events(trip_no):

	# Extract data for current Trip No. X #
	data_of_trip = data[(trip_no-1)*1000:trip_no*1000,:]

	# Count for harsh events #
	highAccCount = count(data_of_trip[:,4]>2.74)
	highDeccCount = count(data_of_trip[:,4]<-2.74)
	highEV = count(data_of_trip[:,8]>2.0)
	lowEV = count(data_of_trip[:,8]<0)
	highTV = count(data_of_trip[:,7]>10.0)
	lowTV = count(data_of_trip[:,7]<0)
	highLoad = count(data_of_trip[:,3]>97)
	lowLoad = count(data_of_trip[:,3]<0)

	# Allowed Events per KM #
	allowed_events_per_km = 1

	# Total Distance # 
	total_distance = (data_of_trip[:,1].sum())/1000

	# Total harsh events occured in 1 trip #
	events_occured = (highAccCount + highDeccCount + highEV + lowEV + highTV + lowTV + highLoad + lowLoad)

	# Assign a default eco score #
	eco = 10

	# ECO Driving Score #
	if events_occured != 0:
		eco = (10 / (events_occured/(total_distance*allowed_events_per_km)))/total_distance

	# Append the values to result array #
	append(trip_no, highAccCount, highDeccCount, highEV + lowEV, highTV + lowTV, highLoad + lowLoad, eco)


# Save the results to a CSV File #
def save_results():
	np.savetxt('results-obd2.csv',result,fmt='%.2f',delimiter=',')

# Append to array and print #
def append(trip_no, highAccCount, highDeccCount, ratio_vehicle_engine, ratio_throttle_vehicle, engine_load, eco):

	# Save the results for each trip #
	result[trip_no-1,0] = trip_no
	result[trip_no-1,1] = highAccCount
	result[trip_no-1,2] = highDeccCount
	result[trip_no-1,3] = ratio_vehicle_engine
	result[trip_no-1,4] = ratio_throttle_vehicle
	result[trip_no-1,5] = engine_load
	result[trip_no-1,6] = eco

# Count for events from Boolean Array #
def count(var):
	c = 0
	for x in var: 
		if x: 
			c += 1
	return c

# Classification of Driver Rating based on ECO Score #
def score_classify(eco):
	if eco>8:
		return 'Excellent'
	elif eco>6:
		return 'Good'
	elif eco>4:
		return 'Not Good'
	elif eco>2: 
		return 'Bad'
	else:
		return 'Very Bad'
		

# Run the Main Function on script load #
if __name__ == '__main__':
	main()