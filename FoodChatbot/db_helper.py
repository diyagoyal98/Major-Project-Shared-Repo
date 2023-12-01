import decimal

import mysql.connector
global cnx

# Function to fetch the order status from the order_tracking table

cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="iMshray@64",
        database="pandeyji_eatery"
    )

def insert_order_tracking(order_id,status):
    cursor = cnx.cursor()

    # Inserting the record into the order_tracking table
    insert_query = "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query, (order_id, status))

    # Committing the changes
    cnx.commit()

    # Closing the cursor
    cursor.close()


def get_total_order_price(order_id):
    try:
        cursor = cnx.cursor()

        # Execute SQL query to calculate the total price for the given order_id
        query = """
                SELECT SUM(total_price) as total_price
                FROM orders
                WHERE order_id = %s
               """
        cursor.execute(query, (order_id,))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor
        cursor.close()
        if result and result[0] is not None:
            return decimal.Decimal(result[0])
        else:
            return decimal.Decimal(0)

    except mysql.connector.Error as err:
        print(f"Error fetching total order price: {err}")
        return decimal.Decimal(0)

    except Exception as e:
        print(f"An error occurred: {e}")
        return decimal.Decimal(0)

def insert_order_item(food_item,quantity,order_id):
    try:
        cursor = cnx.cursor()
        query = "SELECT item_id, price FROM food_items WHERE name = %s"
        cursor.execute(query, (food_item,))
        item_details = cursor.fetchone()
        quantity_decimal = decimal.Decimal(quantity)

        if item_details:
            item_id = item_details[0]
            price = item_details[1] * quantity_decimal

            insert_query = "INSERT INTO orders (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s,%s)"
            cursor.execute(insert_query, (order_id, item_id, quantity, price))
            cnx.commit()

            print(f"Order {order_id} added successfully!")
            return "successfull"
        else:
            print(f"Error: Food item '{food_item}' not found.")
            return -1
            #return "food item not found in table"

    except mysql.connector.Error as err:
        print(f"Error inserting order item: {err}")

        #rollback
        cnx.rollback()

        return -1
        #return f"myswl error {err}"

    except Exception as e:
        print(f"An error occured: {e}")
        cnx.rollback()

        return -1
        #return f"exception {e}"




def get_next_order_id():
    cursor = cnx.cursor()

    # Executing the SQL query to get the next available order_id
    query = "SELECT MAX(order_id) FROM orders"
    cursor.execute(query)

    # Fetching the result
    result = cursor.fetchone()[0]

    # Closing the cursor
    cursor.close()

    # Returning the next available order_id
    if result is None:
        return 1
    else:
        return result + 1



def get_order_status(order_id):

    cursor = cnx.cursor()

    # Write the sql query
    query = ("SELECT status FROM order_tracking WHERE order_id = %s")

    #Execute the query
    cursor.execute(query,(order_id,))

    # Fetching the result
    result = cursor.fetchone()

    # Closing the cursor
    cursor.close()


    # Returning the order status
    if result is not None:
        return result[0]
    else:
        return None



