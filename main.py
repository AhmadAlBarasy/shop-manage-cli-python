from pwinput import pwinput
from DBModel import initializeConnection,closeConnection,config
import userPrompts

def main() ->None:
    passwordConfig = config(section = 'main')
    password = passwordConfig.pop('password')
    print("**Welcome To Shop Managemanet System**\n_____________________________________")
    print("Enter the system password to continue: ",end="")
    userInput = pwinput(mask = '*')
    while userInput != password:  
       print("Wrong password, please try again: ",end="")
       userInput = pwinput(mask = '*')
    initializeConnection()
    startProgram()


def startProgram() -> None:
    while True:
        validChoice = False
        print("Choose your prompt:\n-------------------\n1. List all products\n2. Add a product\n3. Delete a product"
            +"\n4.Edit existing product\n5. Create a reciept\n6. Delete a reciept\n7. Print a Reciept\n8. Exit program")
        userChoice = input("Enter your choice: ")
        validChoice = validateChoice(userChoice)
        while not validChoice:
            userChoice = input("Invalid choice, try again: ")
            validChoice = validateChoice(userChoice)
        match int(userChoice):
            case 1:
                userPrompts.listAllProducts()
            case 2:
                userPrompts.insertProduct()
            case 3:
                userPrompts.deleteProduct()
            case 4:
                userPrompts.editProductMainInterface()
            case 5:
                userPrompts.createReciept()
            case 6:
                userPrompts.deleteReciept()
            case 7:
                userPrompts.printReciept()
                pass
            case 8:
                closeConnection()
                break
            case _:
                print("Invalid number...you managed to enter it...somehow :-)")


def validateChoice(userChoice: str) ->bool:
    try:
        userChoice = int(userChoice)
    except ValueError:
        return False
    else:
        if userChoice>8 or userChoice<1:
            return False
    return True

if __name__ == "__main__":
    main()