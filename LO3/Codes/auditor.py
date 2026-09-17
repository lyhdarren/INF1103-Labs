#pre defined variables

stock_quantity_recorded = 0
rejects = 0

#pre defined functions

def get_valid_input():

    while(True):

        stock_quantity = input("Enter the quantity: ")

        if (stock_quantity.lower() == 'quit'):
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


#main code

while(True):

    result = get_valid_input()

    if (result == 'quit'):
        print("Total Quantity Recorded: ", stock_quantity_recorded)
        print("Number of Failed Entry: ", rejects)
        print("Program End")
        break

    elif (result == 0):
        rejects += 1

    elif (result > 0):
        stock_quantity_recorded += result