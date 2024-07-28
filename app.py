from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
import pandas as pd
import os

app = Flask(__name__)
model = pickle.load(open("flight_rf.pkl", "rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        Dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        Dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Duration
        dur_hour = abs(Arrival_hour - Dep_hour)
        dur_min = abs(Arrival_min - Dep_min)

        # Total Stops
        Total_stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        Jet_Airways = 1 if airline == 'Jet Airways' else 0
        IndiGo = 1 if airline == 'IndiGo' else 0
        Air_India = 1 if airline == 'Air India' else 0
        Multiple_carriers = 1 if airline == 'Multiple carriers' else 0
        SpiceJet = 1 if airline == 'SpiceJet' else 0
        Vistara = 1 if airline == 'Vistara' else 0
        GoAir = 1 if airline == 'GoAir' else 0
        Multiple_carriers_Premium_economy = 1 if airline == 'Multiple carriers Premium economy' else 0
        Jet_Airways_Business = 1 if airline == 'Jet Airways Business' else 0
        Vistara_Premium_economy = 1 if airline == 'Vistara Premium economy' else 0
        Trujet = 1 if airline == 'Trujet' else 0

        # Source
        Source = request.form["Source"]
        s_Delhi = 1 if Source == 'Delhi' else 0
        s_Kolkata = 1 if Source == 'Kolkata' else 0
        s_Mumbai = 1 if Source == 'Mumbai' else 0
        s_Chennai = 1 if Source == 'Chennai' else 0

        # Destination
        Destination = request.form["Destination"]
        d_Cochin = 1 if Destination == 'Cochin' else 0
        d_Delhi = 1 if Destination == 'Delhi' else 0
        d_New_Delhi = 1 if Destination == 'New_Delhi' else 0
        d_Hyderabad = 1 if Destination == 'Hyderabad' else 0
        d_Kolkata = 1 if Destination == 'Kolkata' else 0

        prediction = model.predict([[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight price is Rs. {}".format(output))

    return render_template("home.html")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
