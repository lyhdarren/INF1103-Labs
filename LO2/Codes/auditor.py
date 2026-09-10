
#Stock Quantity Recorded Officially
stock_quantity_recorded = 0
#number of rejects
rejects = 0
#successfully process
process = 0

#if the program is true it will always run
while (True):

    #Asking the user for an input 
    stock_quantity = input("Enter the quantity: ")

    if stock_quantity.lower() == "quit":
        print("Total Quantity Recorded: ", stock_quantity_recorded)
        print("Number of Failed Entry: ", rejects)
        print("Number of Successful Entry: ", process)
        print("Program End")
        break

    try:

        stock_quantity = int(stock_quantity)

        if (stock_quantity < 0):
            print("Please input a positive value.")
            rejects += 1

        elif (stock_quantity >= 500):
            print(f"Stock Quantity inputted is {stock_quantity} which exceeded the limit of 500")
            rejects += 1
            

        elif (stock_quantity > 0 and stock_quantity < 500):
            stock_quantity_recorded += stock_quantity
            process += 1
            print("Successfully Recorded")

        else:
            print("Unknown Error")

    except ValueError:
        print("Invalid Input. Please input values only.")

        