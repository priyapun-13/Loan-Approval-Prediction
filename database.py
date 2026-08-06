from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://elsapandey:LoanApproval%40123@cluster0.mhgbsjk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)


db = client["loan_prediction"]

users = db["users"]

loan_applications = db["loan_applications"]