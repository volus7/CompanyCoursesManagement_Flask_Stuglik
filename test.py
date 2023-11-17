import sqlite3

connection = sqlite3.connect("data/users.sqlite", check_same_thread=False)
cursor = connection.cursor()
# cursor.execute("SELECT * FROM teams")
# result = cursor.fetchone()
    
    
print('\nColumns in TEAMS table:') 
data=cursor.execute('''SELECT * FROM teams''') 
for column in data.description: 
    print(column[0])
    
print('\nData in TEAMS table:') 
data=cursor.execute('''SELECT * FROM teams''') 
for row in data: 
    print(row) 
    
        
    
print('\nColumns in USERS table:') 
data=cursor.execute('''SELECT * FROM users''') 
for column in data.description: 
    print(column[0])
    
print('\nData in USERS table:') 
data=cursor.execute('''SELECT * FROM users''') 
for row in data: 
    print(row) 