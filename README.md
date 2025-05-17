# Library-Management-System-Python
Library-Management-System-Python

Library Management System is a command-line application written in Python. It uses CSV files as a simple database (books.csv, members.csv, loans.csv) and the standard library plus bcrypt for password hashing.
The system has two user roles – Librarian and Member – each with different capabilities (adding books, registering users, issuing/returning books, searching catalog, etc.).
Command-line argument parsing is handled with Python’s argparse module and data is stored using the built-in csv module. Passwords are securely hashed using bcrypt (a hashing library). 
The due date for issued books is computed with datetime.timedelta (adding 14 days to the current date)



I have uses bcrypt for password hashing to installed it # (pip install bcrypt).

# Run the app with :- python main.py --data-dir mydata

Note for me only :- python main.py --data-dir mydata to use a specific data folder we can replace mydata with data also 
