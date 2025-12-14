import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import datetime


Font_style="Times New Roman",14,"bold"

# creating user interface 
class ExpenseTracker:
    def __init__(self,master):
        self.master=master
        master.title("Expense Tracker")
        master.geometry("680x700")
        
        # --- BUDGET VARIABLE INITIALIZATION (FIXED) ---
        # 1. Base Budget (CONSTANT: The starting point for all calculations)
        self.initial_budget_base = 1000.0 
        # 2. Current Balance (DYNAMIC: The result of subtraction, used for display)
        self.current_balance = 0.0     

        self.setup_db()
        
        self.budget_display_var = tk.StringVar(master)
        # Calculate the initial state (1000 - existing expenses)
        self.calculate_current_balance() 

        self.middle_frame=tk.Frame(master)
        self.middle_frame.grid()
        self.header_frame = tk.Frame(master)
        self.header_frame.grid(pady=10)

        self.input_frame = tk.Frame(master)
        self.input_frame.grid(pady=10)
        
        self.button_frame = tk.Frame(master)
        self.button_frame.grid(pady=10)

        self.label = tk.Label(self.master, text="Expense Tracker", font=("Arial", 24,"bold"))
        self.label.grid(row=0,column=0,padx=1,pady=1)

    #    total budget display
        self.total_budget=tk.Label(self.header_frame,textvariable=self.budget_display_var,font=("Arial", 15,"bold")).grid(row=1, column=1,columnspan=3,sticky="W",padx=10, pady=10)
        
    #    salary input (used for new budget/salary)
        self.salary=tk.Label(self.header_frame, text="Salary",font=Font_style).grid(row=2, column=1, sticky="E", padx=10,pady=5)
        self.salary_entry=tk.Entry(self.header_frame)
        self.salary_entry.grid(row=2, column=2, sticky="W", padx=5,pady=5)
        tk.Button(self.header_frame, text="Set Budget", command=self.set_budget).grid(row=2, column=3, sticky="W", padx=1,pady=1)


        # adding amount lable and entry
        self.add_amount_lable = tk.Label(self.input_frame, text="Enter Amount",font=Font_style)
        self.amount_entry=tk.Entry(self.input_frame,width=16)
        self.amount_entry.grid(row=0,column=1,sticky="W",padx=5,pady=5)
        self.add_amount_lable.grid(row=0,column=0,sticky="W",padx=10,pady=5)
        
        # category lable and entry
        self.option=["Food","Transport","Rent","Groceries","Entertainment","Utilities","Others"]
        # IMPORTANT: Use self.master instead of root here, as root may not be defined yet
        self.selected_option=tk.StringVar(master) 
        self.selected_option.set(self.option[0])

        self.category=tk.Label(self.input_frame,text="Category",font=Font_style).grid(row=0,column=3,columnspan=2,sticky="ew",padx=1,pady=5)
        ttk.OptionMenu(self.input_frame,self.selected_option,*self.option).grid(row=0,column=4,columnspan=2,sticky="ew",padx=1,pady=5)


        # note lable and entry
        self.note_label=tk.Label(self.input_frame,text="Note",font=Font_style)
        self.note_entry=tk.Entry(self.input_frame,width=16) 
        self.note_label.grid(row=1,column=0,sticky="W",padx=5,pady=5)
        self.note_entry.grid(row=1,column=1,sticky="W",padx=5,pady=5) 

        # date lable and entry
        self.date_label=tk.Label(self.input_frame,text="Date (YYYY-MM-DD):",font=Font_style)
        self.entry_date=tk.Entry(self.input_frame,width=10)
        self.date_label.grid(row=1, column=3, sticky="ew", padx=10, pady=5)
        self.entry_date.grid(row=1, column=4, sticky="ew", padx=5, pady=5)

        # search bar entry ,label and button
        # ... (Existing Buttons) ...
        self.view_expenses_button = tk.Button(self.button_frame, text="View Expenses", command=self.view_expenses).grid(row=0, column=2, padx=10, pady=5)
        tk.Label(self.button_frame, text="Search ID:", font=("Times New Roman",8,"bold")).grid(row=0, column=3, padx=10, pady=5, sticky="W")
        self.search_entry = tk.Entry(self.button_frame, width=10)
        self.search_entry.grid(row=0, column=4, padx=5, pady=5, sticky="W")

        # Butons
        tk.Button(self.button_frame,text="Add expense",command=self.add_expense).grid(row=0, column=0, padx=10, pady=5)
        tk.Button(self.button_frame,text="delete Expense",command=self.delete_expense).grid(row=0,column=1,padx=5,pady=5)
        tk.Button(self.button_frame, text="View Expenses", command=self.view_expenses).grid(row=0, column=2, padx=10, pady=5)
        tk.Button(self.button_frame, text="Search", command=self.search_expense_by_id).grid(row=0, column=5, padx=5, pady=5)

        self.setup_table()

    # sql connection:-------------------------------------------->
    def setup_db(self):
        try:
           
                self.my_db=mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="Srinidhi#04",
                    database="expense_data")
                print("Database connected")
                self.cursor=self.my_db.cursor()
                self.cursor.execute("select * from Expenses")
                self.cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database error",f"could not connect to datbase {err}")
            self.my_db=None
            self.cursor=None
    # adding expense ----------------------------------->
    def add_expense(self):
        amount=self.amount_entry.get()
        category=self.selected_option.get()  
        note=self.note_entry.get()
        date=self.entry_date.get()
        
        try:
            amount=float(amount)
            if amount<=0:
                messagebox.showerror("Input Warning","Amount must be greater than zero")
                return
        except ValueError:
            messagebox.showerror("Input Error","Please enter a valid amount")
            return
        date_format = "%Y-%m-%d"
        try:
            # datetime.datetime.strptime attempts to parse the 'date' string
            # using the specified format. If it fails, it raises a ValueError.
            datetime.datetime.strptime(date, date_format)
        except ValueError:
            messagebox.showerror("Input Error", 
                                 f"Invalid date format. Please use the required format: {date_format} (e.g., 2025-01-31).")
            return

        sql="Insert into Expenses (date,amount,category,note) Values(%s,%s,%s,%s)"
        Values=(date,amount,category,note)
        
        if self.cursor:
            try:
                self.cursor.execute(sql,Values)
                self.my_db.commit()
                
                # Clear inputs
                self.amount_entry.delete(0, tk.END)
                self.note_entry.delete(0, tk.END)
                self.entry_date.delete(0, tk.END)

                self.view_expenses()
                self.calculate_current_balance()
                messagebox.showinfo("Amount added","The amount has been added")
            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", f"Error adding expense: {e}")
        else:
            messagebox.showerror("Connection Error","Database not connected.")

    # Creating Table View:------------------------------------->
    def setup_table(self):
        self.Table_view=ttk.Treeview(self.master,columns=("ID","Date","Amount","Category","Note"),show="headings",height=15)
        # ... (heading and column setup remains the same) ...
        self.Table_view.heading("ID",text="ID")
        self.Table_view.heading("Date",text="Date")
        self.Table_view.heading("Amount",text="Amount")
        self.Table_view.heading("Category",text="Category")
        self.Table_view.heading("Note",text="Note")

        self.Table_view.column("ID",width=50,anchor=tk.CENTER)
        self.Table_view.column("Date",width=50,anchor=tk.CENTER)
        self.Table_view.column("Amount",width=100,anchor=tk.CENTER)
        self.Table_view.column("Category",width=100,anchor=tk.CENTER)
        self.Table_view.column("Note",width=200,anchor=tk.CENTER)

        self.Table_view.grid(padx=10)
        
    # deleting expense
    def delete_expense(self):
        selected_value=self.Table_view.selection()
        
        if not selected_value:
             messagebox.showwarning("No Selection", "Please select an expense to delete.")
             return

        db_data = self.Table_view.item(selected_value[0],"values")[0]
        
        if messagebox.askyesno("Confirm Delete",f"Are you sure you want to delete ID {db_data} ?"):
            try:
                sql="Delete from expenses where ID=%s"
                self.cursor.execute(sql,(db_data,))
                self.my_db.commit()
                self.view_expenses()
                self.calculate_current_balance()
            except mysql.connector.Error as e:
                messagebox.showerror("Error",f"An error occurred while deleting: {e}")
            except Exception as e:
                messagebox.showerror("Error",f"An unexpected error occurred: {e}")

    # creating search bar:-
    def search_expense_by_id(self):
        if not self.cursor:
            messagebox.showerror("Connection Error", "Database not connected.")
            return

        search_id = self.search_entry.get().strip()

        if not search_id:
            messagebox.showwarning("Input Required", "Please enter an Expense ID to search.")
            self.view_expenses() # Display all if search field is empty
            return
            
        try:
            # Clear the table before displaying new results
            for row in self.Table_view.get_children():
                self.Table_view.delete(row)
                
            # Use LIKE for flexibility, though exact match is better for ID
            sql = "SELECT id, date, amount, category, note FROM Expenses WHERE ID = %s"
            self.cursor.execute(sql, (search_id,))
            
            data = self.cursor.fetchall()
            
            if data:
                for record in data:
                    self.Table_view.insert('', "end", values=record)
                print(f"Successfully loaded 1 expense (ID: {search_id}).")
            else:
                messagebox.showinfo("Not Found", f"No expense found with ID: {search_id}")
                
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", f"Error searching ID: {e}")
        except ValueError:
             messagebox.showerror("Input Error", "ID must be a number.")


    # view expense ---------------------->
    def view_expenses(self):
        if not self.cursor:
            return
            
        for row in self.Table_view.get_children():
            self.Table_view.delete(row)
            
        self.cursor.execute("Select id,date,amount,category,note from expenses order by date DESC")
        data=self.cursor.fetchall()
            
        for record in data:
            self.Table_view.insert('',"end",values=record)
        print(f"Successfully loaded {len(data)} expenses into the table.")
    
    # budget----------------------------------------->
    def calculate_total_expenses(self):
        # Queries the database to get the sum of all expense amounts.
        if not self.cursor:
            return 0.00
            
        self.cursor.execute("select sum(amount) from expenses")
        total_sum = self.cursor.fetchone()[0]
        
        # Ensure Decimal type is converted to float for arithmetic compatibility
        if total_sum is not None:
            return float(total_sum) 
        else:
            return 0.00
    
    def calculate_current_balance(self):
    # Calculates the current balance (Initial Budget - Total Expenses) and updates the display.
        total_expenses = self.calculate_total_expenses()
        self.current_balance = self.initial_budget_base - total_expenses
        
        self.budget_display()
    
    def set_budget(self):
    # Reads salary input and UPDATES the current budget base by adding the new amount.
        try:
            new_income = float(self.salary_entry.get())
            self.initial_budget_base += new_income
            self.salary_entry.delete(0, tk.END)
            self.calculate_current_balance()
            
            messagebox.showinfo("New Budget Added", f"Rs{new_income:,.2f} added to your base budget. New total base: Rs{self.initial_budget_base:,.2f}")
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for Salary/Income.")
        finally:
            print("Set budget button clicked")

    def budget_display(self):
        # Displays the current calculated balance
        formatted_budget = f"Total Budget: Rs{self.current_balance:,.2f}" 
        self.budget_display_var.set(formatted_budget)
        

# main
root=tk.Tk()
expense_tracker=ExpenseTracker(root)
root.mainloop()