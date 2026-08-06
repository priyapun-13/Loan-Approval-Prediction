from database import users

result = users.insert_one({
    "name": "Test User",
    "email": "test@test.com",
    "password": "123456",
    "role": "client"
})

print("Inserted ID:", result.inserted_id)