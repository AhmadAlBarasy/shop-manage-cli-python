from DBModel import returnConnection,returnAllProducts,addProduct,deleteProductFromDB,productExists,editProductFromDB,createRecieptRecord,addProductstoReciptDB,deleteRecieptDB,printRecieptDB,finalPriceForReciept,recieptExists,ResultSet
from prettytable import PrettyTable

def validateConnection() -> bool:
    connection = returnConnection()
    if connection == None:
        return False
    else:
        return True


def printTable(resSet:ResultSet) ->None:
    columnsNames = [name[0] for name in resSet.getNames()]
    table = PrettyTable(columnsNames)
    for row in resSet.getResult():
        table.add_row(row)
    print(table)


def listAllProducts() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        resSet = returnAllProducts()
        if resSet == None:
            table = PrettyTable(["No data found"])
            print(table)
        else:
            printTable(resSet)


def insertProduct() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        userInput = input("Enter product details separated by commas, example: id,name,category,wholesale_price,quantity: ")
        userInput =userInput.split(',')
        if len(userInput) != 5:
            print("You must enter 5 values for a product, as mentioned above.") 
        else:
            try:
                userInput[3] = float(userInput[3])
                userInput[4] = float(userInput[4])
            except ValueError:
                print("Quantity and wholesale_price must be numbers")
            else:
                addProduct(userInput)


def deleteProduct() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        userInput = input("Enter the product_id you want to delete,type [quit] to cancel: ")
        deleteProductFromDB(userInput)


def editProductMainInterface() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        productId = input("enter product id: ")
        if productExists(productId):
            print("-----------------------------------------")
            userEditChoice = input("Choose what do you want to edit\n1.quantity\n2.wholesale_price\n3.category\n4.name\n5.cancel\nyour choice: ")
            try:
                userEditChoice = int(userEditChoice)
            except (ValueError):
                print("Invalid choice")
            else:
                match userEditChoice:
                    case 1:
                        editProduct(editOption= 'quantity',productId=productId)
                    case 2:
                        editProduct(editOption= 'wholesale_price',productId=productId)
                    case 3:
                        editProduct(editOption= 'category',productId=productId)
                    case 4:
                        editProduct(editOption= 'product_name',productId=productId)
                    case 5:
                        print('Operation canceled.')
                    case _:
                        print("Invalid choice")
        else:
            print("Product not found.")


def editProduct(editOption:str,productId:str) ->None:
        newValue = input("Enter the new {}: ".format(editOption))
        if editOption == "quantity":
            try:
                newValue = int(newValue)
            except ValueError:
                print("Invalid new value.")
            else:
                editProductFromDB(editOption,newValue,productId)
                
        elif editOption == "wholesale_price":
            try:
                newValue = float(newValue)
            except ValueError:
                print("Invalid new value.")
            else:
                editProductFromDB(editOption,newValue,productId)
        else :
            editProductFromDB(editOption,newValue,productId)


def createReciept() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        recId = input("Enter an ID for the reciept: ")
        if createRecieptRecord(recId):
            addProductsToReciept(recId)


def addProductsToReciept(recId:str) ->None:
    finished = False
    while not finished:
        userInput = input("Enter product_id and quantity separated by a coma,enter [quit] to finish this process: ")
        if userInput == "[quit]":
            finished = True
        else:
            userInput = userInput.split(',')
            if not productExists(userInput[0]):
                print("Product doesn't exist.")
                print("-----------------------------------------")
            else:
                try:
                    userInput[1] = int(userInput[1])
                except ValueError:
                    print("invalid quantity.")
                    print("-----------------------------------------")
                else:
                    addProductstoReciptDB(recId,userInput[0],userInput[1])
                    print("-----------------------------------------")


def deleteReciept() ->None:
     if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
     else:
        recId = input("Enter the ID of the reciept you want to delete: ")
        deleteRecieptDB(recId)


def printReciept() ->None:
    if not validateConnection():
        print("Connection to database Failed, can't proccess this request.")
    else:
        recId = input("Enter the ID of the reciept you want to display: ")
        if not recieptExists(recId):
            print("Reciept not found.")
        else:
            resSet = printRecieptDB(recId)
            if resSet == None:
                table = PrettyTable(["No data found"])
                print(table)
            else:
                printTable(resSet)
                print("Final price is: {}".format(finalPriceForReciept(recId)))
    
