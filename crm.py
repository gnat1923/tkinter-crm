from tkinter import *
import mysql.connector
import csv

root = Tk()
root.title("CRM")
root.geometry("400x600")

#connect to mysql
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "1234",
    database = "crm"
)

#print(mydb) this line tested if db was created

#create a db cursor and initialise
my_cursor = mydb.cursor()

#initialise the database
'''
#create a database (this will be run once)
#my_cursor.execute("CREATE DATABASE crm")

#verify creation was successful
#my_cursor.execute("SHOW DATABASES")
#for db in my_cursor:
#    print(db)

#create db tables
my_cursor.execute("CREATE TABLE IF NOT EXISTS customers \
                   (first_name VARCHAR(255),\
                    last_name VARCHAR(255),\
                    zipcode INT(10),\
                    price_paid DECIMAL(10,2),\
                    user_id INT AUTO_INCREMENT PRIMARY KEY)")


#alter table
my_cursor.execute("ALTER TABLE customers ADD (\
                  email VARCHAR(255),\
                  address_1 VARCHAR(255),\
                  address_2 VARCHAR(255),\
                  city VARCHAR(255),\
                  state VARCHAR(255),\
                  country VARCHAR(255),\
                  phone VARCHAR(255),\
                  payment_method VARCHAR(50),\
                  discount_code VARCHAR(255))")

#erase table, in case of mistake
#my_cursor.execute("DROP TABLE customers")

#show table
my_cursor.execute("SELECT * FROM customers")
for thing in my_cursor.description:
    print(thing)
'''

#functions
#clear text fields
def clear_fields():
    first_name_box.delete(0, END)
    last_name_box.delete(0, END)
    address1_box.delete(0, END)
    address2_box.delete(0, END)
    city_box.delete(0, END)
    state_box.delete(0, END)
    zipcode_box.delete(0, END)
    country_box.delete(0, END)
    phone_box.delete(0, END)
    email_box.delete(0, END)
    #username_box.delete(0, END)
    payment_method_box.delete(0, END)
    discount_code_box.delete(0, END)
    price_paid_box.delete(0, END)

#add customer to db
def add_customer():
    sql_command = "INSERT INTO customers (\
                        first_name,\
                        last_name,\
                        address_1,\
                        address_2,\
                        city,\
                        state,\
                        zipcode,\
                        country,\
                        phone,\
                        email,\
                        payment_method,\
                        discount_code,\
                        price_paid)\
                        VALUES (\
                            %s,%s,%s,%s,%s,%s,%s,\
                            %s,%s,%s,%s,%s,%s)"
    values = (
        first_name_box.get(),
        last_name_box.get(),
        address1_box.get(),
        address2_box.get(),
        city_box.get(),
        state_box.get(),
        zipcode_box.get(),
        country_box.get(),
        phone_box.get(),
        email_box.get(),
        payment_method_box.get(),
        discount_code_box.get(),
        price_paid_box.get()
    )

    my_cursor.execute(sql_command, values)

    #commit changes to db
    mydb.commit()

    #clear fields
    clear_fields()

#write to csv function
def write_to_csv(result):
    with open("exports/customers.csv", "a", newline="") as f:
        w = csv.writer(f, dialect="excel")
        for record in result:
            w.writerow(record)

#list customers
def list_customers():
    list_cutomer_query = Tk()
    list_cutomer_query.title("List All Customers")
    list_cutomer_query.geometry("800x600")

    #query the database
    my_cursor.execute("SELECT * FROM customers")
    result = my_cursor.fetchall()
    
    for index, x in enumerate(result):
        num=0
        for y in x:
            lookup_label = Label(list_cutomer_query, text=y)
            lookup_label.grid(row=index, column=num)
            num +=1
    
    csv_button = Button(list_cutomer_query, text="Export as csv", command=lambda: write_to_csv(result))
    csv_button.grid(row=index+1, column=0)

#search customers function
def search_customers():
    search_customers = Tk()
    search_customers.title("Search All Customers")
    search_customers.geometry("800x600")

    def search_now():
        searched = search_box.get()
        sql = "SELECT * FROM customers WHERE last_name = %s" #%s is a place holder value
        name = (searched, ) #name will fill the placeholder. Coma as this must be a tuple
        result = my_cursor.execute(sql, name)
        result = my_cursor.fetchall()

        if not result:
            result = "Record not found"

        searched_label = Label(search_customers, text=result)
        searched_label.grid(row=2, column=0, padx=10)

    #entry box for customer search
    search_box = Entry(search_customers)
    search_box.grid(row=0, column=1, padx=10, pady=10)
    #entry box label
    search_box_label = Label(search_customers, text="Search Customer by Last Name")
    search_box_label.grid(row=0, column=0, padx=10, pady=10)
    #entry box search button
    search_button = Button(search_customers, text="Search Customers", command=search_now)
    search_button.grid(row=1, column=0, padx=10, pady=10)

#create a label
title_label = Label(root, text="Company Customer Database", font=("Helvetica, 16"))
title_label.grid(row=0, column=0, columnspan=2, pady="10")

#create main form to enter customer data
first_name_label = Label(root, text="First Name").grid(row=1, column=0, sticky=W, padx=10)
last_name_label = Label(root, text="Last Name").grid(row=2, column=0, sticky=W, padx=10)
address1_label = Label(root, text="Address 1").grid(row=3, column=0, sticky=W, padx=10)
address2_label = Label(root, text="Address 2").grid(row=4, column=0, sticky=W, padx=10)
city_label = Label(root, text="City").grid(row=5, column=0, sticky=W, padx=10)
state_label = Label(root, text="State").grid(row=6, column=0, sticky=W, padx=10)
zipcode_label = Label(root, text="Zipcode").grid(row=7, column=0, sticky=W, padx=10)
country_label = Label(root, text="Country").grid(row=8, column=0, sticky=W, padx=10)
phone_label = Label(root, text="Phone Number").grid(row=9, column=0, sticky=W, padx=10)
email_label = Label(root, text="Email").grid(row=10, column=0, sticky=W, padx=10)
payment_method_label = Label(root, text="Payment Method").grid(row=11, column=0, sticky=W, padx=10)
discount_code_label = Label(root, text="Discount Code").grid(row=12, column=0, sticky=W, padx=10)
price_paid_label = Label(root, text="Price Paid").grid(row=13, column=0, sticky=W, padx=10)

#create entry boxes
first_name_box = Entry(root)
first_name_box.grid(row=1,column=1,pady=5)

last_name_box = Entry(root)
last_name_box.grid(row=2,column=1,pady=5)

address1_box = Entry(root)
address1_box.grid(row=3,column=1,pady=5)

address2_box = Entry(root)
address2_box.grid(row=4,column=1,pady=5)

city_box = Entry(root)
city_box.grid(row=5,column=1,pady=5)

state_box = Entry(root)
state_box.grid(row=6,column=1,pady=5)

zipcode_box = Entry(root)
zipcode_box.grid(row=7,column=1,pady=5)

country_box = Entry(root)
country_box.grid(row=8,column=1,pady=5)

phone_box = Entry(root)
phone_box.grid(row=9,column=1,pady=5)

email_box = Entry(root)
email_box.grid(row=10,column=1,pady=5)

payment_method_box = Entry(root)
payment_method_box.grid(row=11,column=1,pady=5)

discount_code_box = Entry(root)
discount_code_box.grid(row=12,column=1,pady=5)

price_paid_box = Entry(root)
price_paid_box.grid(row=13,column=1,pady=5)

#create buttons
add_customer_button = Button(root, text="Add Customer To Database", command=add_customer)
add_customer_button.grid(row=14, column=0, padx=10, pady=10)

clear_fields_button = Button(root, text="Clear Fields", command=clear_fields)
clear_fields_button.grid(row=14, column=1, padx=10, pady=10)

list_customers_btn = Button(root, text="List Customers", command=list_customers)
list_customers_btn.grid(row=15, column=0, sticky=W, padx=10)

search_customers_button = Button(root, text="Search Customers", command=search_customers)
search_customers_button.grid(row=15, column=1, sticky=W, padx=10)




root.mainloop()