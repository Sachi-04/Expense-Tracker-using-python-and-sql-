# Expense-Tracker-using-python-and-sql-
💰 Personal Expense Tracker (Python/Tkinter/MySQL)
📝 Overview
This is a simple, yet robust, desktop application built using Python and its built-in Tkinter library for the Graphical User Interface (GUI). It allows users to track their daily expenses, manage a starting budget, and view their transactions, which are stored in a MySQL database.

✨ Key Features
GUI Interface: User-friendly desktop application built with Tkinter.

Database Integration: Uses mysql.connector to persist expense data in a MySQL database.

Budget Management: Automatically calculates the remaining balance based on a fixed initial budget and new expenses.

Expense Tracking: Allows adding, viewing, and deleting expenses with categories, notes, and dates.

Search Functionality: Quickly search for a specific expense by its ID.

Dynamic Budget Update: Ability to add new income (salary) to the base budget.

🛠️ Installation and Setup
1. Prerequisites
You need to have Python and a MySQL server installed on your system.

Python 3.x

MySQL Server (e.g., MySQL Community Server, XAMPP, or MAMP)

2. Install Python Libraries
Install the required Python libraries using pip:

Bash

pip install tkinter # Usually built-in, but good practice
pip install mysql-connector-python
3. MySQL Database Setup
The application connects to a specific database and table. You need to create them first.

A. Database Connection Details: The application code uses the following hardcoded credentials (you will likely want to change these for security in a real deployment, but use them for local testing):

Host: localhost

User: root

Password: Srinidhi#04

Database: expense_data

B. SQL Commands: Use your MySQL client (e.g., MySQL Workbench, command line) to run these commands:

SQL

-- 1. Create the Database
CREATE DATABASE expense_data;

-- 2. Select the Database
USE expense_data;

-- 3. Create the Expenses Table
CREATE TABLE Expenses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50),
    note VARCHAR(255)
);
4. Running the Application
Save the provided code as a Python file (e.g., expense_tracker.py).

Ensure your MySQL server is running.

Execute the Python script:

Bash

python expense_tracker.py
⚙️ How to Use
Database Connection: On launch, the app attempts to connect to the MySQL database. If successful, you'll see "Database connected" in your console.

Initial Budget: The application starts with an initial_budget_base of Rs1000.00.

Set Budget: Use the Salary input field and the Set Budget button to add income to your base budget. (e.g., if you enter 5000, your base budget becomes 6000).

Add Expense:

Enter the Amount.

Select a Category (Food, Transport, Rent, etc.).

Add an optional Note.

Enter the Date in YYYY-MM-DD format (e.g., 2025-12-14).

Click Add expense.

View Expenses: The expenses are displayed in the table view and are automatically updated upon adding or deleting. You can also click View Expenses to refresh the list.

Delete Expense: Select a row in the table and click Delete Expense.

Search: Enter the ID (the first column) in the search bar and click Search.

🤝 Contribution
Feel free to fork the repository, make improvements, and submit pull requests. Any suggestions for new features or bug fixes are welcome!

📄 License
This project is open source and available under the MIT License.
