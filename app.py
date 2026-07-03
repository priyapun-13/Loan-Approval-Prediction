from flask import Flask, render_template, request
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load model and scaler
model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Numerical Features
        person_age = float(request.form['person_age'])
        person_income = float(request.form['person_income'])
        person_emp_exp = float(request.form['person_emp_exp'])
        loan_amnt = float(request.form['loan_amnt'])
        loan_int_rate = float(request.form['loan_int_rate'])
        loan_percent_income = float(request.form['loan_percent_income'])
        cb_person_cred_hist_length = float(request.form['cb_person_cred_hist_length'])
        credit_score = float(request.form['credit_score'])

        # Dropdown Values
        gender = request.form['gender']
        education = request.form['education']
        ownership = request.form['ownership']
        intent = request.form['intent']
        previous_default = request.form['default']

        # Gender Encoding
        person_gender_male = 1 if gender == "male" else 0

        # Education Encoding
        person_education_Bachelor = 1 if education == "Bachelor" else 0
        person_education_Doctorate = 1 if education == "Doctorate" else 0
        person_education_High_School = 1 if education == "High School" else 0
        person_education_Master = 1 if education == "Master" else 0

        # Home Ownership Encoding
        person_home_ownership_OTHER = 1 if ownership == "OTHER" else 0
        person_home_ownership_OWN = 1 if ownership == "OWN" else 0
        person_home_ownership_RENT = 1 if ownership == "RENT" else 0

        # Loan Intent Encoding
        loan_intent_EDUCATION = 1 if intent == "EDUCATION" else 0
        loan_intent_HOMEIMPROVEMENT = 1 if intent == "HOMEIMPROVEMENT" else 0
        loan_intent_MEDICAL = 1 if intent == "MEDICAL" else 0
        loan_intent_PERSONAL = 1 if intent == "PERSONAL" else 0
        loan_intent_VENTURE = 1 if intent == "VENTURE" else 0

        # Previous Loan Default
        previous_loan_defaults_on_file_Yes = int(previous_default)

        

        features = [[
    person_age,
    person_income,
    person_emp_exp,
    loan_amnt,
    loan_int_rate,
    loan_percent_income,
    cb_person_cred_hist_length,
    credit_score,
    person_gender_male,
    person_education_Bachelor,
    person_education_Doctorate,
    person_education_High_School,
    person_education_Master,
    person_home_ownership_OTHER,
    person_home_ownership_OWN,
    person_home_ownership_RENT,
    loan_intent_EDUCATION,
    loan_intent_HOMEIMPROVEMENT,
    loan_intent_MEDICAL,
    loan_intent_PERSONAL,
    loan_intent_VENTURE,
    previous_loan_defaults_on_file_Yes
]]



   
        features = scaler.transform(features)

        # Prediction
        prediction = model.predict(features)[0]

        # Confidence
        probability = model.predict_proba(features)[0]
        confidence = round(max(probability) * 100, 2)

        if prediction == 1:
            result = f"✅ LOAN APPROVED ({confidence}% Confidence)"
        else:
            result = f"❌ LOAN REJECTED ({confidence}% Confidence)"

        return render_template(
            'index.html',
            prediction_text=result
        )

    except Exception as e:
        return render_template(
            'index.html',
            prediction_text=f"Error: {str(e)}"
        )


if __name__ == "__main__":
    app.run(debug=True)