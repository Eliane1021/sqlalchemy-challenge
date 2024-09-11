# Import the dependencies.

from asyncio import start_server
import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import text
from flask import Flask, jsonify
from datetime import datetime

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
print(Base.metadata.tables.keys())
# Access the classes
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


#################################################
# Flask Routes
#################################################
# Start at the homepage.

# List all the available routes.

@app.route("/")
def welcome():
    return (
        f"Available Routes in Hawaii Climate API:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
    session=Session(engine)

    pre_data= session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23')

    session.close()

    precipitation_data = []
    
    for prcp, date in pre_data:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitation_data.append(precipitation_dict)

    # Fix the variable name passed to jsonify (should be precipitation_data)
    return jsonify(precipitation_data)

#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def station(): 
    session = Session(engine)

    # Query all station data
    station_data = session.query(Station.name, Station.station).all()

    session.close()

    stations_values = []
    for station, id in station_data:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['name'] = id
        stations_values.append(stations_values_dict)

    return jsonify(stations_values)


# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs") 
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date,  Measurement.tobs,Measurement.prcp).\
                filter(Measurement.date >= '2016-08-23').\
                filter(Measurement.station=='USC00519281').\
                order_by(Measurement.date).all()

    session.close()

#     # Convert to a list
    dates_tobs_values = []
    for date, tobs, station in dates_tobs_results:
        dates_tobs_dict = {}
        dates_tobs_dict["date"] = date
        dates_tobs_dict["tobs"] = tobs
        dates_tobs_dict["station"] = station
        dates_tobs_values.append(dates_tobs_dict)
    return jsonify(dates_tobs_values) 

#     

# # Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)
    
    start_date_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= startDate).all()

    session.close()

    dates_values = []                       
    for  min, avg,max in start_date_results:
        date_dict = {}  
        date_dict["Min_tobs"] = min
        date_dict["Avg_tobs"] = avg
        date_dict["Max_tobs"] = max
        dates_values.append(date_dict)
    return jsonify(dates_values)

@app.route("/api/v1.0/<start>/<end>")

# Define function, set start and end dates entered by user as parameters for start_end_date decorator
def Start_end_date(start, end):
    session = Session(engine)

    

    start_end_date_results =  session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    

    session.close()

     # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_date_values = []
    for min, avg, max in start_end_date_results:
        start_end_date_dict = {}
        start_end_date_dict["Date"] = date
        start_end_date_dict["min_tobs"] = min
        start_end_date_dict["avg_tobs"] = avg
        start_end_date_dict["max_tobs"] = max
        start_end_date_values.append(start_end_date_dict) 
    

    return jsonify(start_end_date_values)



if __name__ == '__main__':
    app.run(debug=True) 


#################################################
# Flask Routes
#################################################

   