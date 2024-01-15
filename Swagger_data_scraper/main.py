import requests
import json
import csv

url = "https://di-cl-dev.qymera.tech/api/v1/docs/?format=openapi"

response = requests.get(url)
data = json.loads(response.text)

# Access the paths and request methods
paths = data['paths']

# Create a list to store the extracted data
data_list = []

# Iterate over the paths and extract the data
for path, methods in paths.items():
    for method, details in methods.items():
        if method == 'parameters':
            continue
        else:
            schema_name = ''
            if 'schema' in details.get('responses', {}).get('200', {}):
                schema = details['responses']['200']['schema']
                if '$ref' in schema:
                    schema_name = schema['$ref'].split('/')[-1]
            elif 'schema' in details.get('responses', {}).get('201', {}):
                schema = details['responses']['201']['schema']
                if '$ref' in schema:
                    schema_name = schema['$ref'].split('/')[-1]

            data_list.append([path, schema_name, method])

# Specify the path to save the CSV file
csv_file = r"C:\Users\Joviel Niel Baltazar\Desktop\digi\data.csv"

# Write the extracted data to the CSV file
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['endpoint', 'table', 'action'])
    writer.writerows(data_list)

print(f"Data has been saved to {csv_file}.")
