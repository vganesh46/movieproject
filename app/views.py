from app import app
import pandas
import json
from pymongo import MongoClient
import vincent
import datetime, time, math
from datetime import timedelta
from flask import render_template
import sys

@app.route('/')
@app.route('/index')
def index():
    
    time_graph_data = []
    time_axis = []
    freq_axis = []
    client = MongoClient('localhost', 27017)
    db = client['movie_analysis_db']
    collection = db['movie_tweets']

    cursor1= collection.find({"entities.hashtags.text" : "KhaidiNo150"}).sort("created_at", -1)
    # print cursor1.count()
    for record in cursor1:
        time_graph_data.append(time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(record['created_at'],'%a %b %d %H:%M:%S +0000 %Y')))

    
    # a list of "1" to count the hashtags
    ones = [1]*len(time_graph_data)
    # the index of the series
    idx = pandas.DatetimeIndex(time_graph_data)
    new_idx = [x+ timedelta(minutes = 330) for x in idx]
    movieChart = pandas.Series(ones, index=new_idx)
    # 
    ## Resampling / bucketing
    per_minute = movieChart.resample('60Min').sum()
    
    for key, value in per_minute.iteritems():
        if math.isnan(value) != True:
            time_axis.append(time.strftime("%Y-%m-%d %H:%M:%S", key.timetuple()))
            freq_axis.append(value)
    print(time_axis, file=sys.stderr)
    return render_template('index.html',
                           time_axis=time_axis,
                           freq_axis=freq_axis)