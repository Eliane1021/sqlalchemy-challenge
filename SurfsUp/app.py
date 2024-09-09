# Import the dependencies.
from asyncio import start_server
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///hawaii.sqlite")

#################################################
# Database Setup
#################################################



# reflect an existing database into a new model
Base = automap_base()

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station= Base.classes.station

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
        f"/api/v1.0/start/end"
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

    station_data = session.query(Station.station,Station.id).all()

    session.close()

    stations_values = []
    for station, id in station_data:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_values.append(stations_values_dict)
    return jsonify (stations_values) 

# Query the dates and temperature observations of the most-active station for the previous year of data.

# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs") 
def tobs():
    session = Session(engine)

    station_temp = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.date)

    session.close()

    all_days_temp=list(np.ravel(dates_temp_mostactive))

    return jsonify(all_days_temp)

# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def input(start=None, end=None):
    session=Session(engine)

    if not end:
        only_start_andgreater=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
        .filter(Measurement.date >=start).all()
        
        only_start_andgreater_stats=list(np.ravel(only_start_andgreater))

        return jsonify(only_start_andgreater_stats)

    start_and_end=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
    .filter(Measurement.date >=start).filter(Measurement.date<=end).all()

    start_and_end_stats=list(np.ravel(start_and_end))

    return jsonify(start_and_end_stats)

    session.close()


# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.

@app.route("/api/v1.0/<start>")
def start_temp(start):
    session=Session(engine)

    
    specific_day_temp_stats=session.query(Measurement.date,func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
    .filter(Measurement.date >=start).all()

    session.close()

    temps_pickday=list(np.ravel(specific_day_temp_stats))

    return jsonify(temps_pickday)

# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

@app.route("/api/v1.0/<start>/<end>")
def end_to_start(start,end):
    session=Session(engine)

    date_interval_stats=session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs))\
    .filter(Measurement.date >=start).filter(Measurement.date<=end).all()

    session.close()
    
    user_picks_dates=list(np.ravel(date_interval_stats))

    return jsonify(user_picks_dates)


if __name__ == '__main__':
    app.run(debug=True) 


#################################################
# Flask Routes
#################################################

   