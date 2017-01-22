import pandas
from pymongo import MongoClient
import vincent
from datetime import timedelta
import math, time

time_graph_data = []
time_axis = []
freq_axis = []
client = MongoClient('localhost', 27017)
db = client['movie_analysis_db']
collection = db['movie_tweets']

cursor1= collection.find({"entities.hashtags.text" : "2Point0"}).limit(10)
# print cursor1.count()
for record in cursor1:
    time_graph_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(record['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))

# a list of "1" to count the hashtags
ones = [1]*len(time_graph_data)
# the index of the series
idx = pandas.DatetimeIndex(time_graph_data)
new_idx = [x+ timedelta(minutes = 330) for x in idx]
# print new_idx
# the actual series (at series of 1s for the moment)
movieChart = pandas.Series(ones, index=new_idx)
# 
## Resampling / bucketing
per_minute = movieChart.resample('10Min').sum()
# print per_minute
for key, value in per_minute.iteritems():
    if math.isnan(value) != True:
        time_axis.append(time.strftime("%Y-%m-%d %H:%M:%S", key.timetuple()))
        freq_axis.append(value)
print time_axis
#time_chart = vincent.Line(per_minute)
#time_chart.axis_titles(x='Time', y='Freq')
#time_chart.to_json('time_chart.json')
#time_chart.display()