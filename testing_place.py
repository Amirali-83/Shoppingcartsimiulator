import csv


product_mobile = []
with open('products.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Category'] == 'Mobile':
            product_mobile.extend([row['Category'], row['ID']])

print(product_mobile)
