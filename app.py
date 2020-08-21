from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station



app = Flask(__name__)

@app.route("/")
def home():
    return (
    f"Welcome these are the routes available: <br/>"                             
    f"/api/v1.0/precipitation <br/>"                                          
    f"/api/v1.0/stations <br/>"                                     
    f"/api/v1.0/tobs <br/>"
    f"/api/v1.0/'insert date with xxxx-xx-xx format'<br/>"
    f"/api/v1.0/'insert start date with xxxx-xx-xx format/'insert end date with xxxx-xx-xx format''"                                      
    )

@app.route("/api/v1.0/precipitation/")
def prec():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    
    precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)    
    
    
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():    
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    return jsonify(results)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs, Station.name).filter(Measurement.date >= "2016-08-23").filter(Station.name == "WAIHEE 837.5, HI US").all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).group_by(Measurement.date).all()
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def startandend(start, end):
    session = Session(engine)
    results = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).group_by(Measurement.date).all()
    session.close()

    return jsonify(results)
if __name__ == "__main__":
    app.run(debug=True)









