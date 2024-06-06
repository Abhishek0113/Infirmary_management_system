from datetime import datetime
import mysql.connector
class InvalidPasswordException(Exception):
    def __init__(self, message):
        super().__init__(message)

class MedicalProduct:
    def __init__(self, productId, productName, manufacturer, expiryDate, price, quantityInStock):
        self.productId = productId
        self.productName = productName
        self.manufacturer = manufacturer
        self.expiryDate = expiryDate
        self.price = price
        self.quantityInStock = quantityInStock

    def getProductId(self):
        return self.productId

    def getProductName(self):
        return self.productName

    def getManufacturer(self):
        return self.manufacturer

    def getExpiryDate(self):
        return self.expiryDate

    def getPrice(self):
        return self.price

    def getQuantityInStock(self):
        return self.quantityInStock

    def updateStock(self, quantity):
        self.quantityInStock += quantity

    def isExpired(self):
        currentDate = datetime.now()
        return self.expiryDate < currentDate

    def calculateTotalCost(self, quantity):
        pass                                        #will do 

class Medicine(MedicalProduct):
    def calculateTotalCost(self, quantity):
        return self.getPrice() * quantity

class Inventory:
    def __init__(self, db_connection, cursor):
        self.db_connection = db_connection
        self.cursor = cursor

    def create_products_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                productId INT AUTO_INCREMENT PRIMARY KEY,
                productName VARCHAR(255),
                manufacturer VARCHAR(255),
                expiryDate DATE,
                price DECIMAL(10, 2),
                quantityInStock INT
            )
        """)

    def addProduct(self, product):
        sql = "INSERT INTO products (productName, manufacturer, expiryDate, price, quantityInStock) VALUES (%s, %s, %s, %s, %s)"
        val = (product.productName, product.manufacturer, product.expiryDate, product.price, product.quantityInStock)
        self.cursor.execute(sql, val)
        self.db_connection.commit()

    def displayAllProducts(self):
        print("=======================================")
        print("          All Available Products")
        print("=======================================")
        print("Product ID    | Name                      | Manufacturer             | Expiry Date  | Price   | Quantity in Stock")
        print("=======================================")

        sql = "SELECT * FROM products"
        self.cursor.execute(sql)
        products = self.cursor.fetchall()

        for product in products:
            print("---------------------------------------")
            print("ID:", product[0])
            print("Name:", product[1])
            print("Manufacturer:", product[2])
            print("Expiry Date:", product[3].strftime("%m/%d/%Y"))
            print("Price: $", product[4])
            print("Quantity in Stock:", product[5])

        print("=======================================")

    def findProductById(self, productId):
        sql = "SELECT * FROM products WHERE productId = %s"
        val = (productId,)
        self.cursor.execute(sql, val)
        product = self.cursor.fetchone()
        if product:
            return MedicalProduct(product[0], product[1], product[2], product[3], product[4], product[5])
        return None

    def manageStock(self, managerPassword):
        while True:
            print("Enter the action:\n1. Update stock\n2. Display all products\n3. Exit")
            try:
                actionChoice = int(input())
                if actionChoice == 1:
                    print("Enter the Product ID to update stock:")
                    productId = int(input())
                    selectedProduct = self.findProductById(productId)

                    if selectedProduct:
                        print("Current stock:", selectedProduct.getQuantityInStock())
                        newStock = int(input("Enter the new stock quantity: "))
                        selectedProduct.updateStock(newStock)
                        sql = "UPDATE products SET quantityInStock = %s WHERE productId = %s"
                        val = (selectedProduct.quantityInStock, selectedProduct.productId)
                        self.cursor.execute(sql, val)
                        self.db_connection.commit()
                        print("Stock updated successfully.")
                    else:
                        print("Product with ID", productId, "not found.")
                elif actionChoice == 2:
                    self.displayAllProducts()
                elif actionChoice == 3:
                    return
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def sellProduct(self, productId, quantityToSell):
        sql = "SELECT * FROM products WHERE productId = %s"
        val = (productId,)
        self.cursor.execute(sql, val)
        product = self.cursor.fetchone()

        if product:
            if product[5] >= quantityToSell:
                newStock = product[5] - quantityToSell
                sql = "UPDATE products SET quantityInStock = %s WHERE productId = %s"
                val = (newStock, productId)
                self.cursor.execute(sql, val)
                self.db_connection.commit()
                print("Sold", quantityToSell, "of", product[1])
            else:
                print("Not enough stock to sell.")
        else:
            print("Product with ID", productId, "not found.")

class InfirmaryManagementSystem:
    def __init__(self):
        self.appointments = {}
        self.patients = {}
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="infirmary"
        )
        self.cursor = self.db_connection.cursor()
        
        self.create_patients_table()

    def create_patients_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                sap_id VARCHAR(255) PRIMARY KEY,
                roll_no VARCHAR(255),
                name VARCHAR(255),
                age INT,
                gender VARCHAR(10),
                appointment_datetime DATETIME
            )
        """)

    def addAppointment(self, doctor, patient, time):
        if doctor in self.appointments:
            self.appointments[doctor].append((patient, time))
        else:
            self.appointments[doctor] = [(patient, time)]

    def addPatient(self, roll_no, sap_id, name, age, gender):
        self.patients[sap_id] = {'roll_no': roll_no, 'name': name, 'age': age, 'gender': gender}
        sql = "INSERT INTO patients (sap_id, roll_no, name, age, gender) VALUES (%s, %s, %s, %s, %s)"
        val = (sap_id, roll_no, name, age, gender)
        self.cursor.execute(sql, val)
        self.db_connection.commit()

    def displayAppointments(self):
        print("=======================================")
        print("          Doctor's Appointments")
        print("=======================================")
        for doctor, appointments in self.appointments.items():
            print("Doctor:", doctor)
            for appointment in appointments:
                print("Patient:", appointment[0], "| Time:", appointment[1])
            print("=======================================")

    def displayPatientDetails(self, sap_id):
        sql = "SELECT * FROM patients WHERE sap_id = %s"
        val = (sap_id,)
        self.cursor.execute(sql, val)
        patient = self.cursor.fetchone()
        if patient:
            print("Patient Details:")
            print("SAP ID:", sap_id)
            print("Roll No.:", patient[1])
            print("Name:", patient[2])
            print("Age:", patient[3])
            print("Gender:", patient[4])
        else:
            print("Patient not found.")

    @staticmethod
    def displayMainMenu():
        print("=======================================")
        print("       Infirmary Management System")
        print("=======================================")
        print("Choose your user type:")
        print("  P - Patient")
        print("  D - Doctor")
        print("  M - Manager")
        print("  exit - Exit the program")
        print("=======================================")

    @staticmethod
    def displayPatientMenu():
        print("=======================================")
        print("          Patient Menu")
        print("=======================================")
        print("1. Buy Medicine")
        print("2. Book Appointment")
        print("3. Display All Products")
        print("=======================================")

    @staticmethod
    def displayDoctorMenu():
        print("=======================================")
        print("          Doctor Menu")
        print("=======================================")
        print("1. View My Appointments")
        print("2. View Patient Details")
        print("=======================================")

    @staticmethod
    def displayManagerMenu():
        print("=======================================")
        print("         Manager Menu")
        print("=======================================")
        print("1. Update Stock")
        print("2. Display All Products")
        print("3. Exit")
        print("=======================================")

    def main(self):
        inventory = Inventory(self.db_connection, self.cursor)
        inventory.create_products_table()

        general_doctors = ["Dr. John", "Dr. Mary"]
        injury_doctors = ["Dr. Smith", "Dr. Johnson"]

        while True:
            self.displayMainMenu()
            userType = input("Enter your choice: ")

            if userType.lower() == "exit":
                break

            try:
                if userType.lower() == "p":
                    self.displayPatientMenu()
                    patientActionChoice = int(input("Enter your choice: "))

                    if patientActionChoice == 1:
                        productIdToBuy = int(input("Enter the Product ID to buy: "))
                        quantityToBuy = int(input("Enter the quantity to buy: "))
                        inventory.sellProduct(productIdToBuy, quantityToBuy)
                    elif patientActionChoice == 2:
                        roll_no = input("Enter your Roll No.: ")
                        sap_id = input("Enter your SAP ID: ")
                        name = input("Enter your name: ")
                        age = input("Enter your age: ")
                        gender = input("Enter your gender: ")
                        print("Select doctor category:")
                        print("1. General Illnesses")
                        print("2. Injuries")
                        category_choice = int(input("Enter your choice: "))
                        if category_choice == 1:
                            print("Available general doctors:")
                            for i, doctor in enumerate(general_doctors, start=1):
                                print(f"{i}. {doctor}")
                            doctor_choice = int(input("Select doctor (1, 2): "))
                            selected_doctor = general_doctors[doctor_choice - 1]
                        elif category_choice == 2:
                            print("Available injury doctors:")
                            for i, doctor in enumerate(injury_doctors, start=1):
                                print(f"{i}. {doctor}")
                            doctor_choice = int(input("Select doctor (1, 2): "))
                            selected_doctor = injury_doctors[doctor_choice - 1]
                        else:
                            print("Invalid choice.")
                            continue
                        appointment_time = input("Enter appointment time: ")
                        print(f"Appointment booked with {selected_doctor} at {appointment_time}")
                        self.addAppointment(selected_doctor, sap_id, appointment_time)
                        self.addPatient(roll_no, sap_id, name, age, gender)
                    elif patientActionChoice == 3:
                        inventory.displayAllProducts()
                    else:
                        print("Invalid choice.")

                elif userType.lower() == "d":
                    self.displayDoctorMenu()
                    doctor_choice = int(input("Enter your choice: "))

                    if doctor_choice == 1:
                        doctor_name = input("Enter your name: ")
                        print("Your appointments:")
                        for appointment in self.appointments.get(doctor_name, []):
                            print("Patient:", appointment[0], "| Time:", appointment[1])
                    elif doctor_choice == 2:
                        patient_id = input("Enter patient SAP ID: ")
                        self.displayPatientDetails(patient_id)

                elif userType.lower() == "m":
                    managerPassword = input("Enter manager password (Enter 'exit' to quit): ")

                    if managerPassword.lower() == "exit":
                        break

                    if managerPassword == "managerPassword":  # Assuming the password is "managerPassword"
                        self.displayManagerMenu()
                        managerActionChoice = int(input("Enter your choice: "))

                        if managerActionChoice == 1:
                            inventory.manageStock(managerPassword)
                        elif managerActionChoice == 2:
                            inventory.displayAllProducts()
                        elif managerActionChoice == 3:
                            pass
                        else:
                            print("Invalid choice.")
                    else:
                        raise InvalidPasswordException("Invalid manager password")

                else:
                    print("Invalid user type.")
            except ValueError:
                print("Invalid input. Please enter a valid choice.")

if __name__ == "__main__":
    infirmary_system = InfirmaryManagementSystem()
    infirmary_system.main()
