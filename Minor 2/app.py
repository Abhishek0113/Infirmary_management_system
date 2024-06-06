import streamlit as st
import mysql.connector
from enum import Enum

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="abhishek@",  # Update with your MySQL password
            database="infirmary"
        )
        self.cursor = self.connection.cursor()
        
    def initialize_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                sap_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                age INT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                price DECIMAL(10, 2),
                qty INT
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sap_id VARCHAR(255),
                doctor_name ENUM('Dr. Mary', 'Dr. John', 'Dr. Smith', 'Dr. Lary'),
                date DATE,
                time TIME,
                FOREIGN KEY (sap_id) REFERENCES patients(sap_id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS meds_sale (
                bill_id INT AUTO_INCREMENT PRIMARY KEY,
                sap_id VARCHAR(255),
                product_id INT,
                qty_sold INT,
                FOREIGN KEY (sap_id) REFERENCES patients(sap_id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        self.connection.commit()


    def execute_query(self, query, data=None):
        self.cursor.execute(query, data)
        result = self.cursor.fetchall()
        self.connection.commit()
        return result

class UserType(Enum):
    PATIENT = "Patient"
    DOCTOR = "Doctor"
    MANAGER = "Manager"

class Patient:
    def __init__(self, sap_id, name, age):
        self.sap_id = sap_id
        self.name = name
        self.age = age

    def buy_product(self, product_id, quantity):
        query = "SELECT * FROM products WHERE id = %s"
        data = (product_id,)
        product = database.execute_query(query, data)
        if product:
            if product[0][3] >= quantity:
                new_quantity = product[0][3] - quantity
                query = "UPDATE products SET qty = %s WHERE id = %s"
                data = (new_quantity, product_id)
                database.execute_query(query, data)
                query = "INSERT INTO meds_sale (sap_id, product_id, qty_sold) VALUES (%s, %s, %s)"
                data = (self.sap_id, product_id, quantity)
                database.execute_query(query, data)
                st.success(f"{quantity} units of {product[0][1]} bought successfully!")
            else:
                st.error("Not enough stock available.")
        else:
            st.error("Product not found.")

    def book_appointment(self, doctor_name, appointment_date, appointment_time):
        query = "INSERT INTO appointments (sap_id, doctor_name, date, time) VALUES (%s, %s, %s, %s)"
        data = (self.sap_id, doctor_name, appointment_date, appointment_time)
        database.execute_query(query, data)
        st.success("Appointment booked successfully!")

    def add_patient(self, sap_id, name, age):
        query = "SELECT * FROM patients WHERE sap_id = %s"
        data = (sap_id,)
        patient = database.execute_query(query, data)
        if not patient:
            query = "INSERT INTO patients (sap_id, name, age) VALUES (%s, %s, %s)"
            data = (sap_id, name, age)
            database.execute_query(query, data)
            st.success("Patient added successfully!")
        else:
            st.warning("Patient already exists in the database.")


class Doctor:
    def __init__(self, name):
        self.name = name

    def view_appointments(self):
        query = "SELECT * FROM appointments WHERE doctor_name = %s"
        data = (self.name,)
        appointments = database.execute_query(query, data)
        if appointments:
            st.write("Your Appointments:")
            for appointment in appointments:
                st.write(f"Appointment ID: {appointment[0]}")
                st.write(f"SAP ID: {appointment[1]}")
                st.write(f"Date: {appointment[3]}, Time: {appointment[4]}")
                st.write("-------------")
        else:
            st.write("No appointments found.")

    def view_patient_details(self, patient_sap_id):
        query = "SELECT * FROM patients WHERE sap_id = %s"
        data = (patient_sap_id,)
        patient = database.execute_query(query, data)
        if patient:
            st.write("Patient Details:")
            st.write(f"SAP ID: {patient[0][0]}")
            st.write(f"Name: {patient[0][1]}")
            st.write(f"Age: {patient[0][2]}")
        else:
            st.error("Patient not found.")

class Manager:
    def __init__(self, password):
        self.password = password

    def add_product(self, name, price, quantity):
        query = "INSERT INTO products (name, price, qty) VALUES (%s, %s, %s)"
        data = (name, price, quantity)
        database.execute_query(query, data)
        st.success("Product added successfully!")

    def update_stock(self, product_id, quantity):
        query = "UPDATE products SET qty = qty + %s WHERE id = %s"
        data = (quantity, product_id)
        database.execute_query(query, data)
        st.success("Stock updated successfully!")

    def view_patient_details(self, sap_id):
        query = "SELECT * FROM patients WHERE sap_id = %s"
        data = (sap_id,)
        patient = database.execute_query(query, data)
        if patient:
            st.write("Patient Details:")
            st.write(f"SAP ID: {patient[0][0]}")
            st.write(f"Name: {patient[0][1]}")
            st.write(f"Age: {patient[0][2]}")
        else:
            st.error("Patient not found.")

    def view_current_inventory(self):
        query = "SELECT * FROM products"
        products = database.execute_query(query)
        if products:
            st.write("Current Inventory:")
            for product in products:
                st.write(f"Product ID: {product[0]}")
                st.write(f"Name: {product[1]}")
                st.write(f"Price: {product[2]}")
                st.write(f"Quantity: {product[3]}")
                st.write("-------------")
        else:
            st.warning("Inventory is empty.")

    def view_sales_record(self):
        query = "SELECT * FROM meds_sale"
        sales = database.execute_query(query)
        if sales:
            st.write("Sales Record:")
            for sale in sales:
                st.write(f"Bill ID: {sale[0]}")
                st.write(f"SAP ID: {sale[1]}")
                st.write(f"Product ID: {sale[2]}")
                st.write(f"Quantity Sold: {sale[3]}")
                st.write("-------------")
        else:
            st.warning("No sales record found.")

def main():
    st.title("Infirmary Management System")
    global database
    database = Database()
    database.initialize_tables()
    user_type = st.sidebar.selectbox("Choose your user type:", [ut.value for ut in UserType])

    if user_type == UserType.PATIENT.value:
        st.subheader("Patient Menu")
        name = st.text_input("Enter your name:")
        age = st.number_input("Enter your age:", min_value=0, step=1)
        sap_id = st.text_input("Enter your SAP ID:")
        st.write("If you are a new patient, then only click register below.")
        register = st.button("Register")
        if register:
            patient = Patient(sap_id, name, age)
            patient.add_patient(sap_id, name, age)
        action = st.radio("Select an action:", ["See Available Products", "Buy Product", "Book Appointment"])
        if action == "See Available Products":
            query = "SELECT * FROM products"
            products = database.execute_query(query)
            if products:
                st.write("Available Products:")
                for product in products:
                    st.write(f"Product ID: {product[0]}")
                    st.write(f"Name: {product[1]}")
                    st.write(f"Price: {product[2]}")
                    st.write(f"Quantity: {product[3]}")
                    st.write("-------------")
            else:
                st.warning("No products available.")
        elif action == "Buy Product":
            product_id = st.number_input("Enter Product ID:", min_value=1, step=1)
            quantity = st.number_input("Enter Quantity:", min_value=1, step=1)
            if st.button("Buy"):
                patient = Patient(sap_id, name, age)
                patient.buy_product(product_id, quantity)
        elif action == "Book Appointment":
            doctor_name = st.selectbox("Select Doctor:", ['Dr. Mary', 'Dr. John', 'Dr. Smith', 'Dr. Lary'])
            appointment_date = st.date_input("Enter Appointment Date:")
            appointment_time = st.time_input("Enter Appointment Time:")
            if st.button("Book Appointment"):
                patient = Patient(sap_id, name, age)
                patient.book_appointment(doctor_name, appointment_date, appointment_time)

    elif user_type == UserType.DOCTOR.value:
        st.subheader("Doctor Menu")
        doctor_name = st.selectbox("Select your name:", ['Dr. Mary', 'Dr. John', 'Dr. Smith', 'Dr. Lary'])
        action = st.radio("Select an action:", ["View Appointments", "View Patient Details"])
        if action == "View Appointments":
            doctor = Doctor(doctor_name)
            doctor.view_appointments()
        elif action == "View Patient Details":
            patient_sap_id = st.text_input("Enter patient SAP ID:")
            if st.button("View Details"):
                doctor = Doctor(doctor_name)
                doctor.view_patient_details(patient_sap_id)

    elif user_type == UserType.MANAGER.value:
        manager_password = st.sidebar.text_input("Enter manager password:", type="password")
        if manager_password == "managerPassword":  # Assuming the password is "managerPassword"
            st.subheader("Manager Menu")
            action = st.radio("Select an action:", ["Add Product", "Update Stock", "View Patient Details", "View Current Inventory", "View Sales Record"])
            if action == "Add Product":
                name = st.text_input("Enter Product Name:")
                price = st.number_input("Enter Product Price:", min_value=0.0, step=0.01)
                quantity = st.number_input("Enter Initial Quantity:", min_value=0, step=1)
                if st.button("Add Product"):
                    manager = Manager(manager_password)
                    manager.add_product(name, price, quantity)
            elif action == "Update Stock":
                product_id = st.number_input("Enter Product ID:", min_value=1, step=1)
                quantity = st.number_input("Enter Quantity to Add:", min_value=0, step=1)
                if st.button("Update Stock"):
                    manager = Manager(manager_password)
                    manager.update_stock(product_id, quantity)
            elif action == "View Patient Details":
                sap_id = st.text_input("Enter patient SAP ID:")
                if st.button("View Details"):
                    manager = Manager(manager_password)
                    manager.view_patient_details(sap_id)
            elif action == "View Current Inventory":
                manager = Manager(manager_password)
                manager.view_current_inventory()
            elif action == "View Sales Record":
                manager = Manager(manager_password)
                manager.view_sales_record()
        else:
            st.error("Invalid manager password.")

if __name__ == "__main__":
    main()
