import mysql.connector

try:
    # Connect to MySQL
    connection = mysql.connector.connect(
        host='localhost',
        user='root',        # Default XAMPP user
        password='',        # Default XAMPP has no password
        port=3306
    )
    
    print("✅ Successfully connected to MySQL!")
    print(f"✅ MySQL version: {connection.get_server_info()}")
    
    # Create a database for your project
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS budgeting_db")
    print("✅ Database 'budgeting_db' created successfully!")
    
    cursor.close()
    connection.close()
    print("✅ Connection closed properly!")
    
except mysql.connector.Error as error:
    print(f"❌ Error: {error}")