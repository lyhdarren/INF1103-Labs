import json

#pre defined variables

#pre defined functions

            
#---------------- LO3 FUNCTIONS ---------------------

def get_valid_input():

    while(True):

        stock_quantity = input("\nEnter the quantity: ")

        if (stock_quantity.strip().lower() == 'quit'):
            return "quit"

        try:

            stock_quantity = int(stock_quantity)

            if (stock_quantity < 0):
                print("Please input a positive value.")
                return 0

            elif (stock_quantity >= 500):
                print(f"Stock Quantity inputted is {stock_quantity} which exceeded the limit of 500")
                return 0
                

            elif (stock_quantity > 0 and stock_quantity < 500):
                return stock_quantity

            else:
                print("Unknown Error")
                return 0

        except ValueError:
            print("Invalid Input. Please input values only.")
            return 0

def process_delivery(current_total, new_value):

    check_overflow = current_total + new_value

    if (check_overflow >= 500):

        return 0

    else: 

        current_total = check_overflow
        return current_total

def calculate_tax(amount):
    amount = amount*0.10
    return amount

def generate_report(total_units, failed_attempts):
    print("\n--------SUMMARY REPORT----------")
    print("Total Units Recorded: ", total_units)
    print("Total Failed Attempts: ", failed_attempts)

# --------------------- LO4 FUNCTIONS ----------------------

def load_inventory():
    
    try: 
        
        with open("inventory.txt", "r") as file:
            
            data = file.readlines()
            inventory = []
            
            if len(data) == 0:
                print("No Data Shown!\n")
            
            for line in data:
                data = line.strip().split(",")
                inventory.append(data)
                
            return inventory
            
    except FileNotFoundError:
        print("text file do not exist.")
        return []
    
def save_inventory(obj):
    
    new_item = obj
    
    try:
        new_inventory = (
            f"{new_item['product_id']},"
            f"{new_item['product_name']},"
            f"{new_item['product_price']},"
            f"{new_item['product_stock']}\n"
        )
        
        with open("inventory.txt", "a") as file:
            
            file.writelines(new_inventory)
            print("\nNew Item Added:")
            print("Order Successfully saved to inventory.txt")
            
    except FileNotFoundError:
        print("text file do not exist.")
        return
    
def get_latest_order_id():
    
    storage = load_inventory()
    
    if len(storage) > 0:
        latest = int(storage[-1][0][1:]) + 1
    else:
        latest = 1
    
    order_id = f"P{latest:03d}"
    
    print(order_id)
    
    return order_id

def get_valid_input_LO4():
    
    while(True):
        
        user_productname = input("Enter Product Name: ")
        
        if (user_productname.lower() == 'quit'):
            print("Exitting...")
            break
        
        try:
            
            user_quantity = int(input("Enter Quantity: "))
            save_inventory(user_productname, user_quantity)
            
        except ValueError as err:
            
            print(f"Error\n {err} \n")

# --------------------- LO5 FUNCTIONS -------------------------

def update_inventory(obj):
    
    try:
        with open("inventory.txt", "r") as file:
            records = file.readlines()

        updated_records = []

        for record in records:
            
            data = record.strip().split(",")

            if data[0] == obj["id"]:
                data[1] = obj["name"]
                data[2] = str(obj["price"])
                data[3] = str(obj["stock"])

            updated_records.append(",".join(data) + "\n")

        with open("inventory.txt", "w") as file:
            file.writelines(updated_records)
            return True

    except FileNotFoundError:
        print("Inventory file not found.")
        return False

def search_product(id):
    
    data = load_inventory()
    
    for x in data:
        
        if (x[0] == id):
            
            productfound = {
                
                "id": x[0],
                "name": x[1].strip(),
                "price": float(x[2]),
                "stock": int(x[3])
                
            }
            
            print("Product Found")
            print("-------------------------")
            print(f"ID: {productfound['id']}")
            print(f"Name: {productfound['name']}")
            print(f"Price: ${productfound['price']}")
            print(f"Stock: {productfound['stock']}")
            print("-------------------------")
            
            return productfound
        
    return None

def add_product():
    
    latestid = get_latest_order_id()
    
    print("\n--------------")
    print("Add New Product")
    print("----------------")
    
    print(f"Product ID: {latestid}")
    new_productname = str(input("Product Name: "))
    
    try:
        new_price = float(input("Enter Price: "))
        
        if (new_price < 0):
            
            print("Price cannot be negative")
            
    except ValueError:
        
        print("Invalid Price. Please enter an integer")
        
    try:
    
        new_stockquantity = int(input("Enter Stock Quantity: "))
        
        if (new_stockquantity < 0):
            
            print("Stock quantity cannot be negative")
            
    except ValueError:
        
        print("Invalid stock quantity. Please enter a whole number.")
    
    new_product = {
        
        "product_id": latestid,
        "product_name": new_productname,
        "product_price": new_price,
        "product_stock": new_stockquantity
        
    }
    
    save_inventory(new_product)
    return

def update_product():
    
    productid = input("Enter Product ID: ")
    
    result = search_product(productid)
    
    if (result is not None):
    
        
        try:
            
            new_stockquantity = int(input("Enter Stock Quantity: "))
            
            if new_stockquantity < 0:
                
                print("Stock quantity cannot be negative.")
                return
            
            else:
                
                result['stock'] = new_stockquantity
                
                updateresult = update_inventory(result)
                
                if updateresult == True:
                    
                    print("Stock Update Successfully!")
                    return
                    
                else: 
                    
                    print("Error!")
                    return
                

        except ValueError:
            
            print("Invalid stock quantity. Please enter a whole number.")
            return
        
    else: 
        
        print("Product Not Found!")
        print("---------------------------")

def convert_to_json():
    
    try:
        
        with open("inventory.txt", "r") as file:
            records = file.readlines()
            
        inventory = []
        
        for x in records:
            
            x = x.strip()
            
            data = x.split(",")
            
            product = {
                
                "productid": data[0],
                "name": data[1],
                "price": float(data[2]),
                "stock": int(data[3])
                
            }
            
            inventory.append(product)
            
        with open("inventory.json", "w") as file:
            json.dump(inventory, file, indent=4)
            
        return True

    except FileNotFoundError:
        return False
        
    except ValueError:
        return False
        
#main code

def main():
    
    data = load_inventory()
    
    if (data != ""):
        
        print("inventory.json found!")
        print("Inventory Loaded Sucessfully")
    
    print("===========================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("===========================")
    
    print("----------- MENU ----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")
    
    while (True):
        
        data = load_inventory()
        
        useroption = input("\nEnter Option:")
        
        if (useroption == '1'):
            
            print("\nCurrent Order: \n")
            print("====================")
            
            for x in data:
                
                print(f"ID: {x[0]} | Name: {x[1].strip()} | Price: ${float(x[2]):.2f} | Stock: {x[3]}")
                
            print("====================")
            
        elif (useroption == '2'):
            
            add_product()
            
        elif (useroption == '3'):
            
            update_product()
            
        elif (useroption == '4'):
            
            print("Search Product")
            print("---------------")
            search_id = input("Enter Product ID: ")
            
            result = search_product(search_id)
            
            if result == "":
                
                print("No Records Found!")
                
        elif (useroption == '5'):
            
            print("Saving Inventory...")
            print("Inventory saved successfuly to inventory.json")
                        
        
        elif (useroption == '6'):
            
            validity = convert_to_json()
            
            if(validity == True):
            
                print("\nSaving Inventory before exit...")
                print("Inventory Saved Successfully.")
                
                print("\nThank you for using Inventory Management System")
                print("Program Terminated")
                break
        
            else: 
                
                print("Error")
        
        
        
        

if __name__ == "__main__":
    main()