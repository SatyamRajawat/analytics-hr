import numpy as np
import pandas as pd
from flask import Flask, request, render_template
import pickle
import json

app = Flask(__name__)

# ============ Loading model ================================

with open('./model/model_employee.pkl', 'rb') as f:
    model = pickle.load(f)



__data_columns = None

#  =============== Loading functions here ====================

def predict_employee(Department,satisfaction_level,average_montly_hours,promotion_last_5years,Work_accident,salary_ord):
    try:
       
        loc_index = __data_columns.index(Department.lower())
    except:
        loc_index = -1
    s = len(__data_columns)
    x = np.zeros(s)
    x[0] = satisfaction_level
    x[1] = average_montly_hours
    x[2] = promotion_last_5years
    x[3] = Work_accident
    x[4] = salary_ord
    if loc_index >= 0:
        x[loc_index] = 1
    print([x])
    prediction =  model.predict([x])[0]
    print("Predict data model is satyam ",prediction)
    # if prediction == 1:
    #     data = 'Employee may left Organization '
    # else :
    #     data = 'Employee will continue in the Organization '
    return prediction

def saved_artifacts():
    print("loading saved artifacts...start")
    global  __data_columns
    global  Department

    with open("./model/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        Department = data_columns[5:]
    print(Department)
    print("loading saved artifacts...done")



# ============================ Calling html page=======================================
@app.route('/')
def index():
    with open("./model/columns.json", "r") as f:
        data_columns = json.load(f)['data_columns']
        dep = data_columns[5:]
    return render_template('index.html', var=dep)


@app.route('/employee', methods=['POST'])
def form_post():
    department = request.form['Department']
    satisfaction_level = request.form['satisfaction_level']
    average_montly_hours = request.form['average_montly_hours']
    promotion_last_5years = request.form['promotion_last_5years']
    Work_accident = request.form['Work_accident']
    salary_ord = request.form['salary_ord']

    print("Predicting model start ........")
    data = predict_employee(department,satisfaction_level,average_montly_hours,promotion_last_5years,Work_accident,salary_ord)
    print('data predicted.........satya',data)
    dep = __Department
    return render_template('index.html',data=data,var=dep, output=True)





if __name__ == "__main__":
    saved_artifacts()
    app.run(debug=True)
