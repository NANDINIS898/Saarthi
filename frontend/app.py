import streamlit as st
import requests

st.set_page_config(page_title="SmartLoan AI", page_icon="💰", layout="centered")

BASE_URL = "http://127.0.0.1:8000"

# --- Authentication ---
if "user" not in st.session_state:
    st.session_state.user = None

st.title("💰 SmartLoan AI Chatbot")

if not st.session_state.user:
    option = st.sidebar.radio("Choose:", ["Login", "Signup"])
    if option == "Signup":
        name = st.text_input("Name")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        phone = st.text_input("Phone")
        address = st.text_input("Address")
        if st.button("Sign Up"):
            r = requests.post(f"{BASE_URL}/signup", params={"name": name, "email": email, "password": password, "phone": phone, "address": address})
            st.success(r.json()["message"])

    else:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            r = requests.post(f"{BASE_URL}/login", params={"email": email, "password": password})
            if r.status_code == 200:
                st.session_state.user = r.json()["user"]
                st.success("Login Successful ✅")
            else:
                st.error("Invalid credentials")

else:
    st.sidebar.write(f"Logged in as {st.session_state.user['name']}")
    st.subheader("💬 Loan Chatbot")

    amount = st.number_input("Enter loan amount (₹)", min_value=10000.0)
    tenure = st.number_input("Enter tenure (years)", min_value=1, max_value=10)

    if st.button("Apply for Loan"):
        r = requests.post(f"{BASE_URL}/loan/start", params={
            "name": st.session_state.user['name'],
            "amount": amount,
            "tenure": tenure
        })
        st.write(r.json()["result"])
