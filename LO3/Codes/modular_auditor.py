#pre defined variables
total_units = 0
rejects = 0
processed = 0

#pre defined functions

def get_valid_input():

    while(True):

        stock_quantity = input("Enter the quantity: ")

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
    current_total = current_total + new_value
    return current_total

def calculate_tax(amount):
    amount = amount*0.10
    return amount

def generate_report(total_units, failed_attempts):
    print("\n--------SUMMARY REPORT----------")
    print("Total Units Recorded: ", total_units)
    print("Total Failed Attempts: ", failed_attempts)


#main code

while(True):

    result = get_valid_input()

    if (result == 'quit'):
        break

    elif (result == 0):
        rejects += 1

    elif (result > 0):

        processed += 1
        total_units = process_delivery(total_units, result)
        tax = calculate_tax(result)

        print("\nDelivery Confirmed: ", result)
        print("Delivery Tax: ", tax)

    else: 
        print("Error")
        rejects += 1

generate_report(total_units, rejects)