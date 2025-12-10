def get_customer_details(name):
    dummy_db = {
        "Nandini": {"phone": "9876543210", "address": "Delhi, India"},
        "Ravi": {"phone": "9123456780", "address": "Mumbai, India"},
        "Demo User": {"phone": "9999999999", "address": "Bangalore, India"},
        "Test User": {"phone": "8888888888", "address": "Pune, India"},
        "Harshit Mittal": {"phone": "7777777777", "address": "Noida, India"},
    }
    return dummy_db.get(name)
