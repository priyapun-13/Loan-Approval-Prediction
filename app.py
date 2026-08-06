from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np
import pandas as pd
from database import users, loan_applications
from flask_bcrypt import Bcrypt

# Create Flask app first
app = Flask(__name__)

# Secret key for session
app.secret_key = "loanapprovalsecretkey"

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Load model and scaler
model = joblib.load("model/model.pkl")
scaler = joblib.load("model/scaler.pkl")


@app.route('/')
def home():
    return render_template('home.html')
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:
            return render_template(
                "register.html",
                message="Passwords do not match"
            )

        if users.find_one({"email": email}):
            return render_template(
                "register.html",
                message="Email already exists"
            )

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        print("Inserting into MongoDB...")
        users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "role": "client"
            
        })
        print("User inserted successfully!")
        print("Register button clicked")

        name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]

        print(name)
        print(email)

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"].lower()
        password = request.form["password"]

        user = users.find_one({"email": email})

        if user and bcrypt.check_password_hash(user["password"], password):

            session["name"] = user["name"]
            session["email"] = user["email"]
            session["role"] = user["role"]

            if user["role"] == "admin":
                return redirect(url_for("admin_dashboard"))

            return redirect(url_for("client_dashboard"))

        return render_template(
            "login.html",
            message="❌ Invalid email or password."
        )

    return render_template("login.html")
@app.route('/client/dashboard')
def client_dashboard():
    return render_template('client_dashboard.html')




@app.route("/history")
def history():

    if "email" not in session:
        return redirect(url_for("login"))

    applications = loan_applications.find(
        {"user_email": session["email"]}
    ).sort("created_at", -1)

    return render_template(
        "history.html",
        applications=applications
    )

@app.route("/admin/dashboard")
def admin_dashboard():

    total_users = users.count_documents({"role": "client"})

    total_applications = loan_applications.count_documents({})

    approved = loan_applications.count_documents({"prediction": "Approved"})

    rejected = loan_applications.count_documents({"prediction": "Rejected"})

    applications = list(loan_applications.find())

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_applications=total_applications,
        approved=approved,
        rejected=rejected,
        applications=applications
    )


@app.route('/view-users')
def view_users():
    return render_template('view_users.html')

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
        from datetime import datetime

        print("Before insert")

        insert_result = loan_applications.update_one(
    {"user_email": session["email"]},
    {
        "$set": {
            "person_age": person_age,
            "person_income": person_income,
            "person_emp_exp": person_emp_exp,
            "loan_amount": loan_amnt,
            "interest_rate": loan_int_rate,
            "loan_percent_income": loan_percent_income,
            "credit_history_length": cb_person_cred_hist_length,
            "credit_score": credit_score,
            "gender": gender,
            "education": education,
            "home_ownership": ownership,
            "loan_intent": intent,
            "previous_default": previous_default,
            "prediction": result,
            "confidence": confidence,
            "created_at": datetime.now()
        }
    },
      upsert=True
)

        print("Inserted Successfully!")
        print("Matched:", insert_result.matched_count)
        print("Modified:", insert_result.modified_count)
        return render_template(
    "result.html",
    prediction_text=result,
    confidence=confidence,
    loan_amount=loan_amnt,
    income=person_income,
    credit_score=credit_score,
    interest_rate=loan_int_rate
)

    except Exception as e:
      print(e)
      raise

@app.route("/admin/management")
def admin_management():

    if session.get("role") != "admin":
        return redirect(url_for("login"))

    all_users = list(users.find())
    all_applications = list(loan_applications.find())

    return render_template(
    "admin_management.html",
    users=all_users,
    applications=all_applications,
    total_users=len(all_users),
    total_applications=len(all_applications)
)

from bson.objectid import ObjectId

@app.route("/delete_user/<id>")
def delete_user(id):

    users.delete_one({
        "_id": ObjectId(id)
    })

    return redirect(url_for("admin_management"))

@app.route("/delete_application/<id>")
def delete_application(id):

    loan_applications.delete_one({
        "_id": ObjectId(id)
    })

    return redirect(url_for("admin_management"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/update_profile", methods=["GET", "POST"])
def update_profile():

    if "email" not in session:
        return redirect(url_for("login"))

    user = users.find_one({"email": session["email"]})

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"].lower()

        password = request.form["password"]
        confirm = request.form["confirm_password"]

        update_data = {
            "name": name,
            "email": email
        }

        if password != "":

            if password != confirm:
                return render_template(
                    "update_profile.html",
                    user=user,
                    message="Passwords do not match!"
                )

            update_data["password"] = bcrypt.generate_password_hash(password).decode("utf-8")

        users.update_one(
            {"email": session["email"]},
            {"$set": update_data}
        )

        session["name"] = name
        session["email"] = email

        user = users.find_one({"email": email})

        return render_template(
            "update_profile.html",
            user=user,
            message="Profile updated successfully!"
        )

    return render_template(
        "update_profile.html",
        user=user
    )

@app.route("/update_application")
def update_application():

    if "email" not in session:
        return redirect(url_for("login"))

    application = loan_applications.find_one(
        {"user_email": session["email"]},
        sort=[("created_at", -1)]
    )

    return render_template(
    "client_dashboard.html",
    application=application
)

if __name__ == "__main__":
    app.run(debug=True)