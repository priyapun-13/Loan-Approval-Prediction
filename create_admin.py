from flask import Flask
from flask_bcrypt import Bcrypt
from database import users

app = Flask(__name__)
bcrypt = Bcrypt(app)

password = "admin123"

hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

print("Hashed Password:")
print(hashed_password)

users.delete_many({"role": "admin"})

users.insert_one({
    "name": "Administrator",
    "email": "admin@gmail.com",
    "password": hashed_password,
    "role": "admin"
})

print("Admin created successfully!")