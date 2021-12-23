import sqlite3;
conn = sqlite3.connect('items.db'); 
c = conn.cursor();

def main():
    user = input('Press 1 to view items: \n'
            'press 2 to login : \n'
            'other to Quit:\n')
    user = int(user)
    typeChecker()
    if user == 1 :
        customer()
    elif user ==2 :
        login()
    else:
        print("Thanks for visiting :")

# ==================================================================================================================
#User side
def customer():
    displayItems()
    choice = input('Enter Sno. of the item you wanna buy : \n'
                        'Other to quit:'
    )
    choice = int(choice)
    chosenItem(choice)

def chosenItem(choice):
    c.execute('SELECT * FROM items WHERE id =:id',{'id':choice})
    item = c.fetchone()
    if item:
        # print(item)
        print("Items\tPrice\tQuantity\tDescription")
        print(item[1],"\t",item[2],"\t",item[3],"\t",item[4])
        wannaBuy = input("\nEnter the number of quantity you wanna purchase :")
        wannaBuy = int(wannaBuy)
        buyItem(choice,wannaBuy)
    else:
        print("\n\n\n=========================Please enter the id of the listed items")
        customer()
    
def buyItem(choice,wannaBuy):
    c.execute('SELECT * FROM items WHERE id =:id',{'id':choice})
    item = c.fetchone()
    if wannaBuy > item[3]:
        print("\n\n====================================Sorry we dont have that items in Such quantity . .============================= \n")
        customer()
    customerRecord(choice,wannaBuy)
    newQuantity = item[3] - wannaBuy 
    with conn:
        c.execute("""UPDATE items SET quantity = :newQuantity
        WHERE id = :choice """,{'newQuantity': newQuantity,'choice':choice})
    
def discount(choice,wannaBuy,typo):
    c.execute('SELECT * FROM items WHERE id =:id',{'id':choice})
    item = c.fetchone()  
    total = item[2]*wannaBuy
    if typo == "normal":
        discount = 0 
    elif typo == "brown":
        discount = total * 0.1
        print("\n\tYou Get 10 percentage discount")
    elif typo == "silver":
        discount = total * 0.2
        print("\n\tYou Get 20 percentage discount")
    elif typo == "gold":
        discount = total * 0.3
        print("\n\tYou Get 30 percentage discount")
    total = total - discount
    return total

def customerRecord(choice,wannaBuy):
    option = input("Press 1 if you are new here ! :\nPress 2 if you have shopped here already:")
    option =int(option)
    if option == 1:
        customerDetailing()
    elif option == 2 :
        print("Welcome Back !!")
    else:
        print("Please enter carefully:")
        customerRecord(choice,wannaBuy)
    token = input("Please enter your Token number:")
    c.execute('SELECT * FROM items WHERE id =:id',{'id':choice})
    item = c.fetchone()
    c.execute('SELECT * FROM customer WHERE id =:id',{'id':token})
    cus = c.fetchone()
    typo = cus[4]
    total = discount(choice,wannaBuy,typo)
    c.execute("SELECT * FROM cusBought")
    bought = c.fetchall()
    id = len(bought) + 1
    grandtotal = total + cus[5]
    c.execute("UPDATE customer SET total=:total",{'total':grandtotal})
    c.execute("INSERT INTO cusBought VALUES (:name,:price,:quantity,:total,:description,:cusId)"
    ,{ 'name': item[1],'price':item[2],'quantity':wannaBuy,'total':total,'description':item[4],'cusId':token})
    #billing
    print("\n\n\n Gautam Fancy Store   \n") 
    print('Sno.\tItems\tprice')
    print('1\t',item[1],'\t\t',item[2],'\n\n')
    print('quantity\t\t',wannaBuy)
    total = item[2]*wannaBuy
    print('Total :\t\t',total)

def customerDetailing(): 
    name = input("Please Enter your name:\n")
    address = input("\nEnter your address:\n")
    number = input("\nEnter your number:\n")
    types = "normal"
    c.execute("SELECT * FROM customer")
    items = c.fetchall()
    print(items)
    id = len(items) + 1
    print(id)
    total = 0
    c.execute("INSERT INTO customer VALUES (:id,:name,:address,:number,:type,:total)"
    ,{ 'id':id,'name': name,'address':address,'number':number,'type':types,'total':total })
    print("Your Token number is :",id)

# =========================================================================================================
#Admin side
def login():
    print("\n\t\t\t\tLogin Form :")
    name = input("Enter your name:\n")
    password = input("Enter your password:\n")
    adminName = 'root'
    adminPassword = 'admin'
    if name != adminName:
        print("Wrong user")
        login()
    if password != adminPassword:
        print("password error!!")
        login()
    recordTracker()
    dashboard()
    
def dashboard():
    print("******************************Welcome***************************************")

    choice = input("""
                Press 1 to view items\n
                Press 2 to update items\n
                Press 3 to Store items\n  
                Press 4 to Delete items\n  
                Press 5 to check Sell details\n  
                Press 6 to Check Customer Details\n
                Press Other to logout          
        """)
    choice = int(choice)
    if choice == 1 :
        displayItems()
        dashboard()
    elif choice == 2 :
        updateItems()
        dashboard()
    elif choice == 3 :
        inputItem()
        dashboard()
    elif choice == 4 :
        deleteItems()  
        dashboard()
    elif choice == 5 :
        cusBoughtDetail()  
        dashboard()
    elif choice == 6 :
        customerDetail()  
        dashboard()
    else:
        main()

#delete
def deleteItems():
    displayItems()
    choice = input("Enter the Sno. of the Product:\n")
    c.execute('DELETE FROM items WHERE id =:id',{'id':choice})

#update
def updateItems():
    displayItems()
    choice = input("Enter the sno. of the product to update :")
    c.execute('SELECT * FROM items WHERE id =:id',{'id':choice})
    item = c.fetchone()
    if item:
        print("Sno.\tItems\tPrice\tQuantity\tDescription")
        print(item[0],"\t",item[1],"\t",item[2],"\t",item[3],"\t",item[4])
        wannaChange = input("\n\nPress 1 to change name \nPress 2 to change Price\nPress 3 to change Quantity\nPress 4 to change Description:\n")
        wannaChange =int(wannaChange)
        if wannaChange == 1 :
            print("Current value is ",item[1])
            change = input("Enter the value to replace it :\n")
            name = change
            price = item[2]
            quantity = item[3]
            description = item[4]
        elif wannaChange == 2 : 
            print("Current value is ",item[2])
            change = input("Enter the value to replace it :\n")
            name = item[1]
            price = change
            quantity = item[3]
            description = item[4]

        elif wannaChange == 3 :
            print("Current value is ",item[3])
            change = input("Enter the value to replace it :\n")
            name = item[1]
            price = item[2]
            quantity = change
            description = item[4]
        elif wannaChange == 4 :
            print("Current value is ",item[4])
            change = input("Enter the value to replace it :\n")
            name = item[1]
            price = item[2]
            quantity = item[3]
            description = change    
        else:
            print("\n\n\t\tError!! Enter the correct value...!!!!")
        with conn:
            c.execute("""UPDATE items SET name = :name , price = :price, quantity = :quantity, description=:description
            WHERE id = :id """,{ 'id':choice,'name': name,'price':price,'quantity':quantity,'description':description })
    else:
        print("\n\n\n=========================Please enter the id of the listed items")
        updateItems()
    print("\n\n\t\tDatabase After the Update :")
    displayItems()
    dashboard()

#create
def createItem(name,price,quantity,description):
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    id = len(items) + 1
    c.execute("INSERT INTO items VALUES (:id,:name,:price,:quantity,:description)"
    ,{ 'id':id,'name': name,'price':price,'quantity':quantity,'description':description })

def inputItem():
    print("Please fill up the following form to insert Item ::")
    name = input("Enter the name of item:")
    price = input("Enter the price of the product:")
    price = int(price)
    quantity = input("Enter the number of product:")
    quantity = int(quantity)
    description = input("Enter the Description of the product:")
    print(name, '\t',price,'\t',quantity,'\t',description)
    createItem(name,price,quantity,description)

def displayItems():
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    print("Sno.\tItems\tPrice\tQuantity\t\t\tDescription")
    for item in items: 
        print(item[0],'\t',item[1],"\t",item[2],"\t",item[3],"\t\t\t",item[4])

def customerDetail():
    c.execute("SELECT * FROM customer")
    items = c.fetchall()
    print("Customer_Name\t Address\t\tPhone_no\t Type\t\t Total Purchases")
    for item in items: 
        print(item[1],"\t",item[2],"\t\t",item[3],"\t\t",item[4],"\t\t",item[5])
  
def cusBoughtDetail():
    c.execute("SELECT * FROM cusBought")
    bought = c.fetchall()
    c.execute("SELECT * FROM customer")
    items = c.fetchall()
    print("Product\t\tPrice\tQuantity\tTotal\t\tBought By\t\t\tDescription:")
    for item in bought: 
        c.execute("SELECT name FROM customer WHERE id= :id",{'id':item[5]})
        name = c.fetchone()
        print(item[0],'\t\t',item[1],"\t",item[2],"\t\t",item[3],"\t\t",name[0],"\t\t\t",item[4])

def recordTracker():
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    print("\nALERT !!!!!!!!          ALERT !!!!!!!!!!!!!!!!         ALERT !!!!!!!!!!!!!!!!!!\n")
    for item in items: 
        if item[3] < 10 :
            print("The Product",item[1],"is near to empty.")
    
def typeChecker():
    c.execute("SELECT * FROM customer")
    items = c.fetchall()  
    for item in items:
        if item[5] > 50000:
            typo = "gold"
            with conn:
                c.execute("""UPDATE customer SET type = :type WHERE id = :id """,
                { 'id': item[0], 'type':typo})
        if item[5] > 30000:
            typo = "gold"
            with conn:
                c.execute("""UPDATE customer SET type = :type WHERE id = :id """,
                { 'id': item[0], 'type':typo})
        if item[5] > 10000:
            typo = "gold"
            with conn:
                c.execute("""UPDATE customer SET type = :type WHERE id = :id """,
                { 'id': item[0], 'type':typo})

main()
conn.commit()
conn.close()


