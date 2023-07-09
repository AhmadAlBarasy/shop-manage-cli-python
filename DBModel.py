from psycopg2 import connect,DatabaseError
from psycopg2.errors import UniqueViolation,NumericValueOutOfRange,CheckViolation
from configparser import ConfigParser

global _con,schema
_con = None 
schema = None

class ResultSet():
    def __init__(self,result,names):
        self.result = result
        self.names = names
    def getNames(self) ->list:
        return self.names
    def getResult(self) ->list:
        return self.result


def config(filename:str = 'config.ini',section:str = 'postgresql') -> dict:
    parser = ConfigParser()
    try:
        parser.read(filename)
        configuration = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                configuration[param[0]] = param[1]
            return configuration
        else:
            print('Error in configuration !')
    except FileExistsError:
        print("Configration File missing.")


def initializeConnection() -> None:
    try:
         dbParams = config()
         global schema
         schema = dbParams.pop('schema')
         global _con
         _con = connect(**dbParams) 
    except(DatabaseError):
        print('**Error Connecting to the database**')


def closeConnection() -> None:
    if _con !=None:
        _con.close()


def returnConnection():
    return _con
    

def productExists(prod_id:str) ->bool:
    try:
        cursor = _con.cursor()
        cursor.execute("select * from {}.products where product_id = '{}';".format(schema,prod_id))
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return True
    except(DatabaseError):
        cursor.execute("rollback")
        return False
    

def returnAllProducts() ->ResultSet:
    cursor = _con.cursor()
    cursor.execute("select * from {}.products order by product_id desc;".format(schema))
    columns = cursor.description
    result = cursor.fetchall()
    if len(result) ==0:
        return None
    return ResultSet(result=result,names=columns)


def addProduct(userInput:list)-> None:
    cursor = _con.cursor()
    try:
        cursor.execute("insert into {}.products values('{}','{}','{}',{},{});".format(schema,userInput[0],userInput[1],userInput[2],userInput[3],userInput[4]))
        _con.commit()
    except(UniqueViolation):
        print("Record with id {} already exists.".format(userInput[0]))
        cursor.execute("rollback")
    except(NumericValueOutOfRange):
        print("wholesale_price must have at most 2 numbers after the decimal point and lies in range between 0 and 9500 $")
        cursor.execute("rollback")
    except (DatabaseError):
        print("Something Wong happened")
        cursor.execute("rollback")
    else:
        print("Record successfully added to the database.")


def deleteProductFromDB(userInput:str) ->None:
    try:   
        cursor = _con.cursor()
        if userInput != '[quit]':
            cursor.execute("delete from {}.products where product_id = '{}';".format(schema,userInput))
            _con.commit()
            print("Successfully deleted product from the database.")
        else:
            print("Operation canceled.")
    except(DatabaseError):
        print("Product not found.")


def editProductFromDB(editOption:str,newValue:str,productId:str) ->None:
    try:
        cursor = _con.cursor()
        if editOption == "product_name" or "category":
            cursor.execute("update {}.products set {} = '{}' where product_id = '{}';".format(schema,editOption,newValue,productId))
            _con.commit()
        else:
            cursor.execute("update {}.products set {} = {} where product_id = '{}';".format(schema,editOption,newValue,productId))
            _con.commit()
    except DatabaseError:
        print("Something wrong happened.")
        cursor.execute("rollback")
    else:
        print("Product updated successfully.")


def recieptExists(recId:str) ->bool:
    cursor = _con.cursor()
    cursor.execute("select * from {}.reciept where rec_id = '{}'".format(schema,recId))
    result = cursor.fetchall()
    if len(result) != 0:
        return True
    else:
        return False


def createRecieptRecord(recId:str) -> bool:
    try:
        cursor = _con.cursor()
        cursor.execute("insert into {}.reciept values('{}',now(),now());".format(schema,recId))
        _con.commit()
        return True
    except UniqueViolation:
        print("This ID already Exists.")
        cursor.execute("rollback")
        return False
    except DatabaseError:
        print("Something wrong happened")
        cursor.execute("rollback")
        return False


def addProductstoReciptDB(recId:str,product_id:str,quantity:int) ->None:
    try:
        cursor = _con.cursor()
        cursor.execute("insert into {}.sales values({},{},{})".format(schema,product_id,recId,quantity))
        cursor.execute("update {}.products set quantity = quantity - {} where product_id = '{}'".format(schema,quantity,product_id))
        _con.commit()
    except CheckViolation:
        print("Quantity is not availabe.")
        cursor.execute("rollback")
    except DatabaseError:
        print("Something wrong happened.")
        cursor.execute("rollback")
    else:
        print("Added successfully.")


def deleteRecieptDB(recId) ->None:
    if not recieptExists(recId):
        print("Reciept not found.")
    else:
        try:
            cursor = _con.cursor()
            cursor.execute("delete from {}.reciept where rec_id = '{}'".format(schema,recId))
            _con.commit()
        except DatabaseError:
            print("Something wrong happened.")
        else:
            print("Reciept successfully deleted from the database.")


def printRecieptDB(recId:str) ->ResultSet:
    cursor = _con.cursor()
    cursor.execute('''select products.product_id as "product ID", product_name as "product name", sales.quantity, final_price as "unit price",(sales.quantity*final_price) as "total price"
                        from {}.products inner JOIN {}.sales on sales.product_id = products.product_id
                        where rec_id = '{}';'''.format(schema,schema,recId))
    columns = cursor.description
    result = cursor.fetchall()
    if len(result) ==0:
        return None
    return ResultSet(result=result,names=columns)
    

def finalPriceForReciept(recId:str) ->float:
    cursor = _con.cursor()
    cursor.execute('''select sum(sales.quantity*final_price) as "final price"
                    from {}.products inner JOIN {}.sales on sales.product_id = products.product_id
                    where rec_id = '{}';'''.format(schema,schema,recId))
    result = cursor.fetchall()
    return result[0][0]