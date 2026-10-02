#pre defined variables


#pre defined functions

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
    
def save_inventory(x, y):
    
    x = str(x)
    y = str(y)
    
    try: 
        
        latestorderid = get_latest_order_id()
        new_inventory = [f"{latestorderid},{x},{y}\n"]
        
        with open("inventory.txt", "a") as file:
            
            file.writelines(new_inventory)
            print("\nNew Order Added:")
            print(f"{latestorderid},{x},{y}\n")
            print("Order Successfully saved to inventory.txt")
            
    except FileNotFoundError:
        print("text file do not exist.")
        return
    

def get_latest_order_id():
    
    storage = load_inventory()
    latest = 0
    
    if int(len(storage) > 0):
        
        latest = int(storage[len(storage)-1][0])+1
        
    else:
        
        latest += 1
    
    print(latest)
    
    return latest

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


#main code

def main():
    
    # -------------------- LO4 CODES ARE BELOW -----------------
    
    data = load_inventory()
    
    print("Current Order: \n")
    
    for x in data:
        print(f"{x[0]}, {x[1].strip()}, {x[2].strip()}")
        
    get_valid_input_LO4()
    
        
    # -------------------- LO3 CODES ARE BELOW -----------------

    total_units = 0
    rejects = 0
    processed = 0

    # while(True):

    #     result = get_valid_input()

    #     if (result == 'quit'):
    #         break

    #     elif (result == 0):
    #         rejects += 1

    #     elif (result > 0):

    #         processed += 1
        
    #         if (process_delivery(total_units, result) <= 0):
    #             print("There is an overflow and have hit the limit of 500. ")
    #             rejects += 1

    #         else:
    #             total_units = process_delivery(total_units, result)

    #             tax = calculate_tax(result)

    #             print("\nDelivery Confirmed: ", result)
    #             print("Delivery Tax: ", tax)

    #     else: 

    #         print("Error")
    #         rejects += 1

    # generate_report(total_units, rejects)


if __name__ == "__main__":
    main()