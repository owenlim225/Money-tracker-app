import tkinter as tk
import db
from calc import Calculator
from currency_conv import CurrencyConverter
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

# For Installing lib
# pip install pysqlite3 

class StartUp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("500x200")
        self.overrideredirect(True)

        # Center StartUp Window
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry("+{}+{}".format(x, y))

        # Call methods
        self.create_widgets()
        self.loading(0)

    def create_widgets(self):
        # Frame
        self.frame_parent = tk.Frame(
            self,
            width=500,
            height=200,
            bd=10,
            relief=tk.GROOVE,
            bg="#102C57"
        )
        
        self.frame_child = tk.Frame(
            self.frame_parent,
            width=480,
            height=180,
            bd=5,
            relief=tk.GROOVE,
            bg="#EADBC8"
        )
        
      # Lbl
        lbl_title = tk.Label(
            self.frame_child,
            text="Pera Ko",
            font=("kuashan script", 40, "bold"),
            bg="#EADBC8"
        )

        self.lbl_loading = tk.Label(
            self.frame_child,
            text="0 %",
            font=("kuashan script", 18, "bold"),
            bg="#EADBC8"
        )
        
        # Widget Pos
        # Frame
        self.frame_parent.pack()
        self.frame_child.place(x=5, y=5)
        
        # Lbl        
        lbl_title.place(x=130, y=50)
        self.lbl_loading.place(x=200, y=120)
        
    # Loading Progress Counter
    def loading(self, progress):
        if progress <= 100:
            self.lbl_loading.config(text=f"{progress} %")
            progress += 1
            self.after(2, self.loading, progress)
        else:
            self.destroy()
            window = MyApp()
            window.mainloop()


class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600+0+0")
        self.title("Pera ko")
        self.resizable(False, False)

        # Check if Database exist, if not, create database file where the py file is located.
        db.create_database()
        
        # Call Methods
        self.create_widgets()
        self.load_entries()
        self.update_total_balance()
        
    def create_widgets(self):
        # Frames
        self.top_frame = tk.Frame(self, width=900, height=130, bg="#102C57")
        self.mid_frame = tk.Frame(self, width=900, height=400, bg="#EADBC8")
        self.chart_frame = tk.Frame(self, width=900, height=470, bg="#EADBC8")
        self.bot_frame = tk.Frame(self, width=900, height=70, bg="#102C57")
        
        self.menu_frame = tk.Frame(self, width=300, height=600, bg="#102C57", bd=4, relief=tk.GROOVE)
        
        # Frames pos
        self.top_frame.place(x=0, y=0)
        self.mid_frame.place(x=0, y=130)
        self.bot_frame.place(x=0, y=530)

        # Date
        self.current_date = tk.StringVar()
        self.current_date.set(datetime.now().strftime("%B %d, %Y"))

        self.lbl_date = tk.Label(
            self.top_frame,
            textvariable=self.current_date,
            font=("katibeh", 20, "bold"),
            bg="#102C57",
            fg="#fff"
        )
        
        # Lable for expense/income/balance
        self.lbl_expenses = tk.Label(
            self.top_frame,
            text="Expenses",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff"
        )
        
        self.lbl_income = tk.Label(
            self.top_frame,
            text="Income",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff"
        )
        
        self.lbl_balance = tk.Label(
            self.top_frame,
            text="Balance",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff"
        )

        self.lbl_expenses_amount = tk.Label(
            self.top_frame,
            text="₱0",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#FF0000"
        )
        
        self.lbl_income_amount = tk.Label(
            self.top_frame, text="₱0",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#90EE90"
        )
        
        self.lbl_amount_amount = tk.Label(
            self.top_frame, text="₱0",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff"
        )

        # Menu Btn
        btn_menu = tk.Button(
            self.top_frame,
            text="≡",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff",
            width=3,
            cursor="hand2",
            command=self.menu_sidebar
        )

        # Date Next/Previous Btn
        self.btn_date_next = tk.Button(
            self.top_frame,
            text=">",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff",
            width=3,
            cursor="hand2",
            command=self.next_date
        )
        
        self.btn_date_previous = tk.Button(
            self.top_frame,
            text="<",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff",
            width=3,
            cursor="hand2",
            command=self.previous_date
        )

        # Top Frame Widgets pos
        self.lbl_date.place(x=160, y=50)
        self.lbl_expenses.place(x=440, y=30)
        self.lbl_income.place(x=580, y=30)
        self.lbl_balance.place(x=730, y=30)

        self.lbl_expenses_amount.place(x=440, y=60)
        self.lbl_income_amount.place(x=580, y=60)
        self.lbl_amount_amount.place(x=730, y=60)

        btn_menu.place(x=10, y=10)

        self.btn_date_next.place(x=360, y=50)
        self.btn_date_previous.place(x=100, y=50)

        # Mid Frame widgets
        # TreeView
        self.tv_tree_view = ttk.Treeview(
            self.mid_frame,
            columns=(1, 2, 3),
            show="headings",
            height=12,
            style="Custom.Treeview"
        )
        
        self.tv_tree_view.column(1, anchor="center", stretch="No", width=200)
        self.tv_tree_view.column(2, anchor="center", stretch="No", width=340)
        self.tv_tree_view.column(3, anchor="center", stretch="No", width=340)
        self.tv_tree_view.heading(1, text="ID")
        self.tv_tree_view.heading(2, text="Name")
        self.tv_tree_view.heading(3, text="Amount")

        # TreeView pos
        self.tv_tree_view.pack(side="left")

        # Config TreeView Style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview.Heading", font=("katibeh", 18))
        style.configure("Custom.Treeview", font=("katibeh", 16), background="#EADBC8", fieldbackground="#EADBC8")
        style.configure("Custom.Treeview", rowheight=30)

        # Disable TreeView Heading Resizing and selection
        self.tv_tree_view.bind('<B1-Motion>', lambda event: 'break')
        self.tv_tree_view.bind("<ButtonRelease-1>", lambda event: self.tv_tree_view.selection_remove(self.tv_tree_view.selection()))

        # TreeView Vertical ScrollBar
        scrollbar = ttk.Scrollbar(
            self.mid_frame,
            orient="vertical",
            command=self.tv_tree_view.yview
        )
        
        scrollbar.pack(side="right", fill="y")

        # Edit Btn
        btn_edit = tk.Button(
            self.mid_frame,
            text="📝",
            font=("katibeh", 20),
            cursor="hand2",
            command=self.edit_entries_window
        )
        
        btn_edit.place(x=810, y=330)

        # Bot Frame
        btn_records = tk.Button(
            self.bot_frame,
            text="🧾",
            font=("katibeh", 26),
            width=3,
            bg="#FEFAF6",
            cursor="hand2",
            command=self.show_records
        )
        
        self.btn_add = tk.Button(
            self.bot_frame,
            text="+",
            font=("katibeh", 28),
            width=3,
            bg="#FEFAF6",
            cursor="hand2",
            command=self.add_entry_win
        )
        
        btn_chart = tk.Button(
            self.bot_frame,
            text="📊",
            font=("katibeh", 26),
            width=3,
            bg="#FEFAF6",
            cursor="hand2",
            command=self.show_chart
        )

        btn_records.place(x=280, y=0)
        self.btn_add.place(x=400, y=0)
        btn_chart.place(x=520, y=0)
        
        # Chart Widgets
        months = [
            'January',
            'February',
            'March',
            'April',
            'May',
            'June',
            'July',
            'August',
            'September',
            'October',
            'November',
            'December'
        ]
        
        year = []
        
        current_month_number = datetime.now().month
        current_month_name = datetime.now().strftime('%B')
        current_year = datetime.now().year
        current_year_str = str(current_year)
        
        year.append(current_year_str) if current_year_str not in year else None

            
        self.chart_month = ttk.Combobox(
            self.chart_frame,
            values=months,
            font=("katibeh", 16),
            width=16,
            state="readonly"
        )
        self.chart_month.set(current_month_name)
        
        self.chart_year = ttk.Combobox(
            self.chart_frame,
            values=year,
            font=("katibeh", 16),
            width=12,
            state="readonly"
        )
        self.chart_year.set(current_year_str)
        
        # Chart Frame Widgets pos
        self.chart_month.place(x=20, y=20)
        self.chart_year.place(x=250, y=20)
                
        # Menu Sidebar widgets
        btn_sidebar_menu_back = tk.Button(
            self.menu_frame,
            text="<",
            font=("katibeh", 14, "bold"),
            bg="#102C57",
            fg="#fff",
            cursor="hand2",
            width=3,
            command=lambda: self.menu_frame.place_forget()
        )
        
        lbl_sidebar_title = tk.Label(
            self.menu_frame,
            text="Pera Ko",
            font=("katibeh", 30, "bold"),
            bg="#102C57",
            fg="#fff",
        )
        
        self.menu_sidebar_child_frame = tk.Frame(
            self.menu_frame,
            bg="#EADBC8",
            width=260,
            height=380,
            bd=3,
            relief=tk.GROOVE
        )
        
        # Widgets Inside menu sidebar child Frame
        btn_calculator = tk.Button(
            self.menu_sidebar_child_frame,
            text="Calculator",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat",
            command=self.open_calculator
        )
        
        btn_currency = tk.Button(
            self.menu_sidebar_child_frame,
            text="Currency Converter",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat",
            command=self.open_currency_converter
        )
        
        
        btn_project_team = tk.Button(
            self.menu_sidebar_child_frame,
            text="Project Team",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat"
        )
        
        btn_clear_data = tk.Button(
            self.menu_sidebar_child_frame,
            text="Clear Data",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat",
            command=self.clear_data
        )
        
        btn_about = tk.Button(
            self.menu_sidebar_child_frame,
            text="About",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat"
        )
        
        btn_exit = tk.Button(
            self.menu_sidebar_child_frame,
            text="Exit",
            font=("katibeh", 18, "bold"),
            cursor="hand2",
            width=15,
            bg="#EADBC8",
            borderwidth=0,
            anchor="w",
            relief="flat",
            command= self.destroy
        )
        
        # Create Bindings For top, mid, bot frame and widgets to close menu sidebar after off focus
        self.top_frame.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.mid_frame.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.chart_frame.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.bot_frame.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.tv_tree_view.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.btn_date_next.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        btn_records.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        self.btn_add.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        btn_chart.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        scrollbar.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        btn_edit.bind('<Button-1>', self.menu_sidebar_outside_frame_click)
        
        # Menu Parent Frame Widgets pos
        btn_sidebar_menu_back.place(x=10, y=10)
        lbl_sidebar_title.place(x=70, y=60)
        self.menu_sidebar_child_frame.place(x=20, y=120)
        
        # Menu Child Frame Widgets pos
        btn_calculator.place(x=10, y=10)
        btn_currency.place(x=10, y=50)
        btn_project_team.place(x=10, y=90)
        btn_clear_data.place(x=10, y=130)
        btn_about.place(x=10, y=170)
        btn_exit.place(x=10, y=210)
        
        
        # Enable Disable Widgets
        # Disable Next button if Date is Current
        today = datetime.now().strftime("%B %d, %Y")
        if self.current_date.get() == today:
            self.btn_date_next.config(state="disabled")
            
    # Show Records or Charts in main window
    def show_records(self):
        self.mid_frame.place(x=0, y=130)
        self.top_frame.config(height=130)
        self.lbl_date.place(x=160, y=50)
        self.lbl_expenses.place(x=440, y=30)
        self.lbl_income.place(x=580, y=30)
        self.lbl_balance.place(x=730, y=30)

        self.lbl_expenses_amount.place(x=440, y=60)
        self.lbl_income_amount.place(x=580, y=60)
        self.lbl_amount_amount.place(x=730, y=60)

        self.btn_date_next.place(x=360, y=50)
        self.btn_date_previous.place(x=100, y=50)
        
        self.btn_add.config(state="normal")
        
        self.chart_frame.place_forget()
        
    
    def show_chart(self):
        # Remove Widgets in Top Frame
        widgets = [
            self.mid_frame,
            self.lbl_date,
            self.lbl_expenses,
            self.lbl_income,
            self.lbl_balance,
            self.lbl_expenses_amount,
            self.lbl_income_amount,
            self.lbl_amount_amount,
            self.btn_date_next,
            self.btn_date_previous
        ]        
        for widget in widgets:
            widget.place_forget()
        
        self.btn_add.config(state="disabled")
        self.top_frame.config(height=60)
        
        # Widgets pos
        self.chart_frame.place(x=0, y=60)
        
    # App Window PopUps
    def add_entry_win(self):
        self.add_window = tk.Toplevel(self)
        self.add_window.title("Add Items")
        self.add_window.geometry("400x300")
        self.add_window.config(bg="#102C57")
        self.add_window.resizable(False, False)
        self.add_window.grab_set()

        # Frames
        frame = tk.Frame(
            self.add_window,
            bg="#EADBC8",
            width=340,
            height=230
            )
        
        frame.place(x=30, y=30)

        # Lbl
        ttk.Label(frame, text="Category:", font=("katibeh", 16, "bold"), background="#EADBC8").place(x=10, y=20)
        ttk.Label(frame, text="Name:", font=("katibeh", 16, "bold"), background="#EADBC8").place(x=10, y=60)
        ttk.Label(frame, text="Amount:", font=("katibeh", 16, "bold"), background="#EADBC8").place(x=10, y=100)

        # Category ComboBox
        self.ent_category = ttk.Combobox(
            frame,
            values=["Income", "Expense"],
            font=("katibeh", 16),
            width=12,
            state="readonly"
        )
        
        self.ent_category.set("Expense")
        self.ent_category['validate'] = 'key'
        self.ent_category['validatecommand'] = (self.register(lambda text: text.isdigit() and text.isalpha() or text == ""), '%S')
        
        # Entry
        self.ent_name = ttk.Entry(
            frame,
            font=("katibeh", 16),
            width=16
            )
        
        self.ent_amount = ttk.Entry(
            frame,
            font=("katibeh", 16),
            width=14
            )
        
        self.ent_name.config(validate="key", validatecommand=(self.ent_name.register(lambda char: char.isalpha() or char == " "), "%S"))
        self.ent_amount.config(validate="key", validatecommand=(self.ent_amount.register(lambda char: char.isdigit() or char == ""), '%S'))

        self.ent_category.place(x=130, y=20)
        self.ent_name.place(x=90, y=60)
        self.ent_amount.place(x=110, y=100)

        # Add Button
        btn_add = tk.Button(
            frame,
            text="Add",
            font=("katibeh", 16),
            width=9,
            cursor="hand2",
            command=self.add_to_db
            )
        
        # Cance Add Button
        btn_cancel_add = tk.Button(
            frame,
            text="Cancel",
            font=("katibeh", 16),
            width=9,
            cursor="hand2",
            command=self.add_window.destroy
            )
        
        btn_add.place(x=40, y=170)
        btn_cancel_add.place(x=170, y=170)
      
    def edit_entries_window(self):
        self.edit_entries_win = tk.Toplevel()
        self.edit_entries_win.title("Options")
        self.edit_entries_win.geometry("400x400")
        self.edit_entries_win.resizable(False, False)
        self.edit_entries_win.grab_set()

        # Frames
        frame1 = tk.Frame(self.edit_entries_win, height=100, width=400, bg="#102C57")
        frame2 = tk.Frame(self.edit_entries_win, height=300, width=400, bg="#EADBC8")
        self.update_frame = tk.Frame(frame2, height=280, width=380, bg="#102C57", bd=3, relief=tk.GROOVE)
        self.remove_frame = tk.Frame(frame2, height=280, width=380, bg="#102C57", bd=3, relief=tk.GROOVE)

        # Frame pos
        frame1.place(x=0, y=0)
        frame2.place(x=0, y=100)

        # Frame 1 Widgets
        # Btn
        btn_update = tk.Button(
            frame1,
            text="Update",
            font=("katibeh", 16),
            cursor="hand2",
            command=self.update_window
            )
        
        btn_remove = tk.Button(
            frame1,
            text="Remove",
            font=("katibeh", 16),
            cursor="hand2",
            command=self.remove_window
            )

        # Btn Pos
        btn_update.place(x=100, y=30)
        btn_remove.place(x=200, y=30)

        # Update Frame Widgets
        # Label Update Frame
        lbl_update_id = tk.Label(
            self.update_frame,
            text="ID:",
            font=("katibeh", 18),
            bg="#102C57",
            fg="#fff"
            )
        
        lbl_update_name = tk.Label(
            self.update_frame,
            text="Name:",
            font=("katibeh", 18),
            bg="#102C57",
            fg="#fff"
            )
        
        lbl_update_category = tk.Label(
            self.update_frame,
            text="Category:",
            font=("katibeh", 18),
            bg="#102C57",
            fg="#fff"
            )
        
        lbl_update_amount = tk.Label(
            self.update_frame,
            text="Amount:",
            font=("katibeh", 18),
            bg="#102C57",
            fg="#fff"
            )

        # Label Update Frame pos
        lbl_update_id.place(x=50, y=20)
        lbl_update_name.place(x=50, y=50)
        lbl_update_category.place(x=50, y=80)
        lbl_update_amount.place(x=50, y=110)

        # Ent Update Frame
        self.ent_update_id = tk.Entry(
            self.update_frame,
            font=("katibeh", 14),
            width=23
            )
        
        self.ent_update_name = tk.Entry(
            self.update_frame,
            font=("katibeh", 14)
            )
        
        self.ent_update_id.config(validate="key", validatecommand=(self.ent_update_id.register(lambda char: char.isdigit() or char == ""), "%S")) 
        self.ent_update_name.config(validate="key", validatecommand=(self.ent_update_id.register(lambda char: char.isalpha() or char == ""), "%S"))

        # ComboBox Entry Update Frame
        self.ent_update_category = ttk.Combobox(
            self.update_frame,
            values=["Income", "Expense"],
            font=("katibeh", 14),
            width=15,
            state="readonly"
            )
        
        self.ent_update_category.set("Expense")
        self.ent_update_category.config(validate="key", validatecommand=(self.ent_update_category.register(lambda char: char.isdigit() and char.isalpha() or char == ""), "%S"))

        self.ent_update_amount = tk.Entry(
            self.update_frame,
            font=("katibeh", 14),
            width=18
            )
        
        self.ent_update_amount.config(validate="key", validatecommand=(self.ent_update_amount.register(lambda char: char.isdigit() or char == ""), "%S"))

        # Ent Update Frame pos
        self.ent_update_id.place(x=100, y=22)
        self.ent_update_name.place(x=130, y=53)
        self.ent_update_category.place(x=170, y=83)
        self.ent_update_amount.place(x=150, y=114)

        # Btn Update Frame
        btn_update_frame = tk.Button(
            self.update_frame,
            text="Update",
            font=("katibeh", 16),
            width=10,
            cursor="hand2", 
            command=self.update_data_to_db
            )
        
        btn_update_cancel_frame = tk.Button(
            self.update_frame,
            text="Cancel",
            font=("katibeh", 16),
            width=8,
            cursor="hand2",
            command=self.edit_entries_win.destroy
            )

        # Btn Update Frame pos
        btn_update_frame.place(x=120, y=170)
        btn_update_cancel_frame.place(x=130, y=220)

        # Remove Frame Widgets
        # Lbl Remove Frame
        lbl_remove_id = tk.Label(
            self.remove_frame,
            text="ID:",
            font=("katibeh", 18),
            bg="#102C57",
            fg="#fff"
            )

        # Lbl Remove Frame pos
        lbl_remove_id.place(x=50, y=80)

        # Ent Remove Frame
        self.ent_remove_id = tk.Entry(
            self.remove_frame,
            font=("katibeh", 14),
            width=18
            )
        
        self.ent_remove_id.config(validate="key", validatecommand=(self.ent_remove_id.register(lambda char: char.isdigit() or char == ""), "%S"))

        # Ent Remove Frame pos
        self.ent_remove_id.place(x=120, y=83)

        # Btn Remove Frame
        btn_remove_frame = tk.Button(
            self.remove_frame,
            text="Remove",
            font=("katibeh", 16),
            width=10,
            cursor="hand2",
            command=self.remove_data_from_db
            )
        
        btn_remove_cancel_frame = tk.Button(
            self.remove_frame,
            text="Cancel",
            font=("katibeh", 16),
            width=8,
            cursor="hand2",
            command=self.edit_entries_win.destroy
            )

        # Btn Remove Frame pos
        btn_remove_frame.place(x=120, y=170)
        btn_remove_cancel_frame.place(x=130, y=220)

    # App Functions Sections
    # Date Functions
    def previous_date(self):
        # Get current date displayed and minus one day to get previous date
        current = datetime.strptime(self.current_date.get(), "%B %d, %Y")
        new_date = current - timedelta(days=1)
        self.current_date.set(new_date.strftime("%B %d, %Y"))
        
        # Enable the "Next" button if it was disabled before
        self.btn_date_next.config(state="normal")
        self.load_entries()
        self.update_amount_label()

    def next_date(self):
        # Get current date displayed and add one day to get next date
        current = datetime.strptime(self.current_date.get(), "%B %d, %Y")
        new_date = current + timedelta(days=1)
        self.current_date.set(new_date.strftime("%B %d, %Y"))
        
        # Check if the current date is today, if yes, disable the "Next" button
        today = datetime.now().strftime("%B %d, %Y")
        if self.current_date.get() == today:
            self.btn_date_next.config(state="disabled")
        self.load_entries()
        self.update_amount_label()

    def load_entries(self):
        # Get current date
        current_date = self.current_date.get()

        # Load entries from the database for the current date
        self.entries = db.load_entries(current_date)

        # Clear existing entries in the Treeview
        for record in self.tv_tree_view.get_children():
            self.tv_tree_view.delete(record)

        # Insert loaded entries into the Treeview
        if self.entries:
            for entry in self.entries:
                # Extract entry details
                category = entry[2]
                amount = entry[4]

                # Format amount based on category
                if category == "Expense":
                    formatted_amount = "-₱{:.2f}".format(abs(amount))  # Display negative amount
                    text_color = "#FF0000"  # Red for expenses
                elif category == "Income":
                    formatted_amount = "+₱{:.2f}".format(abs(amount))  # Display positive amount
                    text_color = "#006400"  # Green for income
                else:
                    formatted_amount = "₱{:.2f}".format(amount)  # Default format
                    text_color = "#000000"  # Default color

                # Insert the entry into the Treeview with appropriate color and tag
                formatted_entry = (entry[1], entry[3], formatted_amount)  # Update amount in entry
                self.tv_tree_view.insert('', 'end', values=formatted_entry, tags=(category,))
                # Apply the color to the entire row
                self.tv_tree_view.tag_configure(category, foreground=text_color)

        self.update_amount_label()
    
    # Update Income/Expense Amount label
    def update_amount_label(self):
        total_expenses = 0
        total_income = 0
        if self.entries:
            for entry in self.entries:
                category = entry[2]
                amount = entry[4]

                if category == "Expense":
                    total_expenses += amount
                elif category == "Income":
                    total_income += amount

            # Update the expenses and income labels with the calculated totals
            self.lbl_expenses_amount.config(text="₱{:.2f}".format(total_expenses))
            self.lbl_income_amount.config(text="₱{:.2f}".format(total_income))
            self.update_total_balance()

        else:
            self.lbl_expenses_amount.config(text="₱{:.2f}".format(total_expenses))
            self.lbl_income_amount.config(text="₱{:.2f}".format(total_income))

    # Update Total Balance Displayed
    def update_total_balance(self):
        total_balance = db.total_amount()
        if total_balance is not None:  # Check if total_balance is not None
            self.lbl_amount_amount.config(text="₱{:.2f}".format(total_balance))
        else:
            self.lbl_amount_amount.config(text="₱0.00")

    # Show Sidebar
    def menu_sidebar(self):
        self.menu_frame.place(x=0, y=0)
    
    # Close Menu Sidebar
    def close_menu_sidebar(self, event=None):
        self.menu_frame.place_forget()
    
    # Check if mouse click detected outside the menu sidebar frame
    def menu_sidebar_outside_frame_click(self, event):
        if event.widget != self.menu_frame:
            self.close_menu_sidebar()
        
    # App Window PopUp Functions
    # Add data to Database
    def add_to_db(self):
        date = self.current_date.get()
        category = self.ent_category.get()
        name = self.ent_name.get()         
        amount = self.ent_amount.get() 

        if date and category and amount:
            try:
                amount = float(amount)               
                db.add_data_to_table(date, category, name, amount)
                
                self.add_window.destroy()
                self.load_entries()
                self.update_total_balance()
                
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid amount")
        else:
            messagebox.showerror("Error", "Please fill in all fields")

    # Update Data to Database
    def update_data_to_db(self):
        current_date = self.current_date.get()
        id = self.ent_update_id.get()
        name = self.ent_update_name.get()
        category = self.ent_update_category.get()
        amount = self.ent_update_amount.get()
        
        if id and name and category and amount:
            try:
                amount = float(amount)
                id_not_exist = db.update_data_in_table(id, name, category, amount, current_date)
                
                if id_not_exist:
                    messagebox.showerror("Error", "Oopss, ID Does not Exist in Current Date")
                else:
                    self.edit_entries_win.destroy()
                    self.load_entries()
                    self.update_total_balance()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid values")
        else:
            messagebox.showerror("Error", "Please fill in all fields")
            
    # Delete Data       
    def remove_data_from_db(self):
        current_date = self.current_date.get()
        id = self.ent_remove_id.get()
        
        id_not_exist = db.delete_data_in_table(id, current_date)
        
        if id:
            if id_not_exist:
                messagebox.showerror("Error", "Oops, ID Does Not Exist In Current Date")
            else:
                self.edit_entries_win.destroy()
                self.load_entries()
                self.update_total_balance()
        else:
            messagebox.showerror("Error", "Please fill in all fields")   
                           
    # Update Entry Window Enable/Disable Displayed Widgets
    def update_window(self):
        self.remove_frame.place_forget()
        self.update_frame.place(x=10, y=10)
        
    # Load datas to update in Update entry window
    def load_data_to_ent_in_update_window(self):
        pass
    
    # Remove Entry Window Enable/Disable Displayed Widgets
    def remove_window(self):
        self.update_frame.place_forget()
        self.remove_frame.place(x=10, y=10)
        
    def clear_data(self):
        result = messagebox.askyesno("Clear Data", "Do you want to Delete All Data? Data cannot be recovered after deletion")
        
        if result:
            db.delete_all_data_in_table()
            self.load_entries()
            self.update_total_balance()
            self.menu_frame.place_forget()
            messagebox.showinfo("Success", "Successfully Cleared Data")
    
    def open_calculator(self):
        Calculator(self)
    
    def open_currency_converter(self):
        CurrencyConverter(self)
                                 
# Call StartUp
# app = StartUp()
# app.mainloop()

# Call Main Window
win = MyApp()
win.mainloop()
