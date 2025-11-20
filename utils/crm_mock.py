def get_customer_details(name):
    dummy_db = {
        "Nandini": {"phone": "9876543210", "address": "Delhi, India"},
        "Ravi": {"phone": "9123456780", "address": "Mumbai, India"},
    }
    return dummy_db.get(name)
