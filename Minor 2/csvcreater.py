import csv

# Dummy data
data = [
    ['medical_condition', 'drug_name'],
    ['Headache', 'Aspirin'],
    ['Fever', 'Paracetamol'],
    ['Allergy', 'Cetirizine'],
    # Add more data as needed
]

# Write data to CSV file
with open('drugs_for_common_treatments.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("CSV file 'drugs_for_common_treatments.csv' has been created.")
