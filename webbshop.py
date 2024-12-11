'''
webbshop.py: Det här är min simpla lilla webbshop som har lite enkla funktioener som gör att man kan kolla på en speciell produkt och man kan 
ändra produkter och man kan ta bort och lägga till.  

__author__  = "Nicklas Hall"
__version__ = "1.0.0"
__email__   = "nicklas.hall@elev.ga.ntig.se"
'''
import csv
import os
from time import sleep

def load_data(filename): 
    products = [] 
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append({
                "id": id,
                "name": name,
                "desc": desc,
                "price": price,
                "quantity": quantity
            })
    return products

def remove_product(products, id):
    temp_product = None 
    for product in products:
        if product["id"] == id:
            temp_product = product
            break

    if temp_product:
        products.remove(temp_product)
        return f"Product: {id} {temp_product['name']} was removed"
    else:
        return f"Product with id {id} not found"

def view_product(products, id):
    for product in products:
        if product["id"] == id:
            return (f"Produktnamn: {product['name']}\n"
                    f"Beskrivning: {product['desc']}\n"
                    f"Pris: {product['price']:.2f} kr\n"
                    f"Kvantitet: {product['quantity']}")
    return "Produkten hittas inte"

def view_products(products):
    header = f"{'Nr':<10}{'Name':<30}{'Description':<45}{'Price':>17}{'Quantity':>20}"
    separator = "-" * len(header)
    product_list = [header, separator]
    max_desc_length = 50
    
    for index, product in enumerate(products, 1):
        desc = product['desc']
        if len(desc) > max_desc_length:
            desc = desc[:max_desc_length - 4] + "..."
        
        product_info = f"{index:<10}{product['name']:<30}{desc:<45}{product['price']:>15} kr{product['quantity']:>10}"
        product_list.append(product_info)
    
    return "\n".join(product_list)

def add_product(products, name, desc, price, quantity):
    max_id = max(products, key=lambda x: x['id'])
    new_id = max_id['id'] + 1
    products.append({
        "id": new_id,
        "name": name,
        "desc": desc,
        "price": price,
        "quantity": quantity
    })
    return f"Lyckades lägga till {name}"

def edit_product(products):
    id = int(input("Vilken produkt vill du ändra? (id): "))
    name = input("Namn på produkten: ")
    desc = input("Beskrivning på produkten: ")
    price = float(input("Pris på produkten: "))
    quantity = int(input("Antal produkter: "))
    for product in products:
        if product['id'] == id:
            product["name"] = name
            product["desc"] = desc
            product["price"] = price
            product["quantity"] = quantity

def save_products(products):
    csv_file_path = "db_products.csv"
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)
    print(f"Data successfully saved to {csv_file_path}")

os.system('cls' if os.name == 'nt' else 'clear')
products = load_data('db_products.csv')
while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print(view_products(products))  
    
    choice = input("Ange produktnummer för att visa information eller välj (T)a bort, (L)ägga till eller (Ä)ndra Eller för mer information skriv nummret: ").strip().upper()

    if choice == "L":  # lägga till
        name = input("Namn: ")
        desc = input("Beskrivning: ")
        while True:
            try:
                price = float(input("Pris: "))
                break
            except ValueError:
                print("nummer")
        while True:
            try:
                quantity = int(input("Kvantitet: "))
                break
            except ValueError:
                print("nummer")
        
        print(add_product(products, name, desc, price, quantity))
        save_products(products)

    elif choice == "Ä":  # Ändra
        edit_product(products)
        save_products(products)

    elif choice == "T":  # ta bort
        try:
            index = int(input("Ange produktnummer för att ta bort: "))
            if 1 <= index <= len(products):  
                selected_product = products[index - 1]  
                id = selected_product['id']  
                print(remove_product(products, id))
                save_products(products)
                sleep(2)
            else:
                print("Ogiltigt produktnummer")
                sleep(2)
        except ValueError:
            print("Ange ett giltigt nummer")
            sleep(2)

    else:
        try:
            index = int(choice)  
            if 1 <= index <= len(products):  
                selected_product = products[index - 1]  
                id = selected_product['id']  
                print(view_product(products, id))  
                input("Tryck på Enter för att fortsätta...")
            else:
                print("Ogiltigt produktnummer")
                sleep(3)
        except ValueError:
            print("Ogiltigt val, försök igen")
            sleep(1)
