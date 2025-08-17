import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.ttk import Treeview, Combobox
from tkcalendar import DateEntry
from datetime import time
from decimal import Decimal
from BLL import MRCBusinessLogic

class MRCGUIApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚢 Marine Rental Company Management System")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        self.colors = {
            'bg_primary': '#2c3e50',
            'bg_light': '#ecf0f1',
            'accent': '#3498db',
            'accent_hover': '#2980b9',
            'text_primary': '#2c3e50',
            'text_secondary': '#7f8c8d',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'card_bg': '#ffffff',
            'container_bg': '#f8f9fa',
            'content_bg': '#ffffff',
            'input_bg': '#ffffff',
            'input_border': '#e1e5e9',
            'text_muted': '#6c757d',
            'shadow': '#00000010',
            'border_light': '#dee2e6',
            'table_header': '#495057',
            'table_stripe': '#f8f9fa'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Business logic instance
        self.mrc_bll = MRCBusinessLogic()
        self.logged_in = False
        
        # Style configuration
        self.setup_styles()
        self.setup_treeview_style()
        
        # Initialize login screen
        self.show_login_screen()

    def setup_styles(self):
        """Configure ttk styles for better appearance"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # CONTAINER STYLING
        style.configure('Container.TFrame',
                    background=self.colors['container_bg'])
        
        # CARD STYLING
        style.configure('Card.TFrame',
                    background=self.colors['card_bg'],
                    relief='solid',
                    borderwidth=1)
        
        # CONTENT STYLING
        style.configure('Content.TFrame',
                    background=self.colors['bg_light'])
        
        # TITLE STYLING
        style.configure('Title.TLabel', 
                    font=('Segoe UI', 20, 'bold'))
        
        # HEADER STYLING  
        style.configure('Header.TLabel', 
                    font=('Segoe UI', 14, 'bold'))
        
        # SUBHEADER STYLING
        style.configure('Subheader.TLabel',
                    font=('Segoe UI', 12))
        
        # FORM LABEL STYLING
        style.configure('Form.TLabel',
                    font=('Segoe UI', 10),
                    background=self.colors['card_bg'],
                    foreground=self.colors['text_primary'])
        
        # ENTRY STYLING
        style.configure('Login.TEntry',
                    fieldbackground=self.colors['input_bg'],
                    borderwidth=1,
                    relief='solid',
                    padding=(8, 6),
                    font=('Segoe UI', 10))
        
        style.map('Login.TEntry',
                focuscolor=[('!focus', self.colors['input_border']),
                            ('focus', self.colors['accent'])])
        
        # LABELFRAME STYLING
        style.configure('Modern.TLabelframe',
                    background=self.colors['card_bg'],
                    borderwidth=1,
                    relief='solid')
        
        style.configure('Modern.TLabelframe.Label',
                    font=('Segoe UI', 11, 'bold'),
                    background=self.colors['card_bg'],
                    foreground=self.colors['text_primary'])
        
        # BUTTON STYLING - Primary
        style.configure('Primary.TButton', 
                    font=('Segoe UI', 10, 'bold'),
                    background=self.colors['accent'],
                    foreground='white',
                    borderwidth=0,
                    relief='flat')
        
        style.map('Primary.TButton',
                background=[('active', self.colors['accent_hover']),
                            ('pressed', self.colors['accent_hover'])])
        
        # SUCCESS BUTTON STYLING
        style.configure('Success.TButton',
                    font=('Segoe UI', 10, 'bold'),
                    background=self.colors['success'],
                    foreground='white',
                    borderwidth=0,
                    relief='flat')
        style.map('Success.TButton',
                background=[('active', '#219a52'),
                            ('pressed', '#219a52')])
        
        # DANGER BUTTON STYLING
        style.configure('Danger.TButton',
                    font=('Segoe UI', 10, 'bold'),
                    background=self.colors['danger'],
                    foreground='white',
                    borderwidth=0,
                    relief='flat')
        style.map('Danger.TButton',
                background=[('active', '#c0392b'),
                            ('pressed', '#c0392b')])
        
        # SECONDARY BUTTON STYLING
        style.configure('Secondary.TButton',
                    font=('Segoe UI', 10),
                    background=self.colors['text_secondary'],
                    foreground='white',
                    borderwidth=0,
                    relief='flat')
        style.map('Secondary.TButton',
                background=[('active', '#95a5a6'),
                            ('pressed', '#95a5a6')])
        
    def setup_treeview_style(self):
        """Custom styling for data tables with modern colors"""
        style = ttk.Style()
        
        # Configure treeview colors
        style.configure("Custom.Treeview",
                    background=self.colors['content_bg'],
                    foreground=self.colors['text_primary'],
                    rowheight=28,
                    fieldbackground=self.colors['content_bg'],
                    borderwidth=1,
                    relief='solid')
        
        style.configure("Custom.Treeview.Heading",
                    font=('Segoe UI', 10, 'bold'),
                    background=self.colors['table_header'],
                    foreground='white',
                    relief='flat',
                    borderwidth=1)
        
        # Alternating row colors and selection
        style.map("Custom.Treeview",
                background=[('selected', self.colors['accent']),
                            ('!selected', self.colors['content_bg'])],
                foreground=[('selected', 'white')])

    def show_login_screen(self):
        """Display the login form with improved UI"""
        self.clear_window()
        
        # Container frame
        container_frame = ttk.Frame(self.root)
        container_frame.grid(row=0, column=0, sticky="nsew")
        container_frame.configure(style='Container.TFrame')
        
        # Main login card
        main_frame = ttk.Frame(container_frame, padding="40", relief="solid", borderwidth=1)
        main_frame.grid(row=0, column=0, sticky="", padx=60, pady=60)
        main_frame.configure(style='Card.TFrame')
        
        # Title
        title_label = ttk.Label(main_frame, text="Marine Rental Company", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 8))
        
        subtitle_label = ttk.Label(main_frame, text="Database Login", style='Header.TLabel')
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30))
        
        # Login form
        ttk.Label(main_frame, text="Host:", style='Form.TLabel').grid(row=2, column=0, sticky="w", pady=(8, 8))
        self.host_entry = ttk.Entry(main_frame, width=20, style='Login.TEntry')
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=2, column=1, sticky="ew", pady=(8, 8), padx=(15, 0))
        
        ttk.Label(main_frame, text="Username:", style='Form.TLabel').grid(row=3, column=0, sticky="w", pady=(8, 8))
        self.username_entry = ttk.Entry(main_frame, width=20, style='Login.TEntry')
        self.username_entry.grid(row=3, column=1, sticky="ew", pady=(8, 8), padx=(15, 0))
        
        ttk.Label(main_frame, text="Password:", style='Form.TLabel').grid(row=4, column=0, sticky="w", pady=(8, 8))
        self.password_entry = ttk.Entry(main_frame, width=20, show="*", style='Login.TEntry')
        self.password_entry.grid(row=4, column=1, sticky="ew", pady=(8, 8), padx=(15, 0))
        
        ttk.Label(main_frame, text="Database:", style='Form.TLabel').grid(row=5, column=0, sticky="w", pady=(8, 8))
        self.database_entry = ttk.Entry(main_frame, width=20, style='Login.TEntry')
        self.database_entry.insert(0, "mrc")
        self.database_entry.grid(row=5, column=1, sticky="ew", pady=(8, 8), padx=(15, 0))
        
        # Login button
        login_btn = ttk.Button(main_frame, text="🔐 Login", command=self.login, style='Primary.TButton')
        login_btn.grid(row=6, column=0, columnspan=2, pady=(25, 0), sticky="ew")
        
        # Configure grid weights for responsive design
        main_frame.columnconfigure(1, weight=1)
        container_frame.columnconfigure(0, weight=1)
        container_frame.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def login(self):
        """Handle login attempt"""
        host = self.host_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        database = self.database_entry.get().strip()
        
        if not all([username, password, database]):
            messagebox.showerror("Error", "Please fill in all required fields")
            return
        
        # Database connection
        try:
            if self.mrc_bll.initialize_database_connection(username, password, database, host):
                self.logged_in = True
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Failed to connect to database. Please check your credentials.")
        except Exception as e:
            messagebox.showerror("Error", f"Connection error: {str(e)}")
    
    def show_main_screen(self):
        """Display the main application interface"""
        self.clear_window()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title_label = ttk.Label(main_frame, text="Marine Rental Company Management", style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Button frame
        button_frame = ttk.LabelFrame(main_frame, text="Operations", padding="10")
        button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        
        # Navigation buttons
        buttons = [
            ("📋 View All Trips", self.view_all_trips),
            ("💰 View Revenue by Vessel", self.view_revenue_by_vessel),
            ("👥 Manage Passengers", self.manage_passengers),
            ("🚢 Manage Vessels", self.manage_vessels),
            ("➕ Add New Trip", self.add_trip),
            ("🚪 Logout", self.logout)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(button_frame, text=text, command=command, style='Primary.TButton')
            btn.grid(row=i//3, column=i%3, padx=5, pady=5, sticky="ew")
        
        # Configure button frame columns
        for i in range(3):
            button_frame.columnconfigure(i, weight=1)
        
        # Content frame
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.grid(row=2, column=0, columnspan=3, sticky="nsew")
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Show initial content
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Display welcome message in content area"""
        self.clear_content_frame()
        
        welcome_label = ttk.Label(self.content_frame, 
                                text="🌊 Welcome to the Marine Rental Company Management System! 🌊\n\nSelect an operation from the buttons above to get started.",
                                font=('Segoe UI', 12), 
                                justify="center")
        welcome_label.grid(row=0, column=0, pady=50)
        
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(0, weight=1)
    
    def clear_window(self):
        """Clear all widgets from the main window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_content_frame(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def view_all_trips(self):
        """Display all trips in a table format"""
        self.clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="All Trips", style='Header.TLabel')
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(self.content_frame, text="🔄 Refresh", command=self.view_all_trips)
        refresh_btn.grid(row=0, column=1, sticky="e", pady=(0, 10))
        
        try:
            trips_data = self.mrc_bll.get_all_trips_formatted()
            
            if isinstance(trips_data, str) or not trips_data:
                no_data_label = ttk.Label(self.content_frame, text="No trips found")
                no_data_label.grid(row=1, column=0, columnspan=2, pady=20)
                return
            
            # Create treeview for trips
            columns = ('date_time', 'vessel', 'passenger', 'address', 'phone', 'cost')
            tree = Treeview(self.content_frame, columns=columns, show='headings', height=15, style="Custom.Treeview")
            
            # Define headings
            tree.heading('date_time', text='Date & Time')
            tree.heading('vessel', text='Vessel')
            tree.heading('passenger', text='Passenger')
            tree.heading('address', text='Address')
            tree.heading('phone', text='Phone')
            tree.heading('cost', text='Total Cost')
            
            # Configure column widths
            tree.column('date_time', width=150)
            tree.column('vessel', width=120)
            tree.column('passenger', width=120)
            tree.column('address', width=200)
            tree.column('phone', width=120)
            tree.column('cost', width=100)
            
            # Add data
            for trip in trips_data:
                # Format cost properly
                cost = trip['total_cost']
                if isinstance(cost, Decimal):
                    cost_str = f"${cost:.2f}"
                else:
                    cost_str = str(cost)
                
                tree.insert('', tk.END, values=(
                    trip['date_time'],
                    trip['vessel_name'],
                    trip['passenger_name'],
                    trip['passenger_address'],
                    trip['passenger_phone'],
                    cost_str
                ))
            
            # Add scrollbars
            v_scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
            h_scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.HORIZONTAL, command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Grid layout
            tree.grid(row=1, column=0, columnspan=2, sticky="nsew")
            v_scrollbar.grid(row=1, column=2, sticky="ns")
            h_scrollbar.grid(row=2, column=0, columnspan=2, sticky="ew")
            
        except Exception as e:
            error_label = ttk.Label(self.content_frame, text=f"Error loading trips: {str(e)}")
            error_label.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
    
    def view_revenue_by_vessel(self):
        """Display revenue by vessel"""
        self.clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Total Revenue by Vessel", style='Header.TLabel')
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Refresh button
        refresh_btn = ttk.Button(self.content_frame, text="🔄 Refresh", command=self.view_revenue_by_vessel)
        refresh_btn.grid(row=0, column=1, sticky="e", pady=(0, 10))
        
        try:
            revenue_data = self.mrc_bll.get_total_revenue_by_vessel()
            
            if isinstance(revenue_data, str) or not revenue_data:
                no_data_label = ttk.Label(self.content_frame, text="No revenue data found")
                no_data_label.grid(row=1, column=0, columnspan=2, pady=20)
                return
            
            # Create treeview for revenue
            columns = ('vessel_name', 'revenue')
            tree = Treeview(self.content_frame, columns=columns, show='headings', height=10, style="Custom.Treeview")
            
            # Define headings
            tree.heading('vessel_name', text='Vessel Name')
            tree.heading('revenue', text='Total Revenue')
            
            # Configure column widths
            tree.column('vessel_name', width=300)
            tree.column('revenue', width=200)
            
            # Add data
            total_revenue = 0
            for item in revenue_data:
                revenue = item['revenue']
                if isinstance(revenue, Decimal):
                    revenue_str = f"${revenue:.2f}"
                    total_revenue += float(revenue)
                else:
                    revenue_str = str(revenue)
                    try:
                        total_revenue += float(str(revenue).replace('$', '').replace(',', ''))
                    except:
                        pass
                
                tree.insert('', tk.END, values=(
                    item['vessel_name'],
                    revenue_str
                ))
            
            # Add total row
            tree.insert('', tk.END, values=("TOTAL", f"${total_revenue:,.2f}"))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            
            # Grid layout
            tree.grid(row=1, column=0, columnspan=2, sticky="nsew")
            scrollbar.grid(row=1, column=2, sticky="ns")
            
        except Exception as e:
            error_label = ttk.Label(self.content_frame, text=f"Error loading revenue data: {str(e)}")
            error_label.grid(row=1, column=0, columnspan=2, pady=20)
        
        # Configure grid weights
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(1, weight=1)
    
    def manage_passengers(self):
        """Display passenger management interface"""
        self.clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Passenger Management", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Buttons
        add_btn = ttk.Button(self.content_frame, text="➕ Add Passenger", command=self.add_passenger, style='Success.TButton')
        add_btn.grid(row=1, column=0, padx=5, pady=5)
        
        delete_btn = ttk.Button(self.content_frame, text="🗑️ Delete Passenger", command=self.delete_passenger, style='Danger.TButton')
        delete_btn.grid(row=1, column=1, padx=5, pady=5)
        
        refresh_btn = ttk.Button(self.content_frame, text="🔄 Refresh", command=self.manage_passengers)
        refresh_btn.grid(row=1, column=2, padx=5, pady=5)
        
        try:
            passengers = self.mrc_bll.get_all_passengers_list()
            
            if not passengers:
                no_data_label = ttk.Label(self.content_frame, text="No passengers found")
                no_data_label.grid(row=2, column=0, columnspan=3, pady=20)
                return
            
            # Create treeview for passengers
            columns = ('id', 'first_name', 'last_name', 'street', 'city', 'state', 'zip', 'phone', 'seasick')
            self.passenger_tree = Treeview(self.content_frame, columns=columns, show='headings', height=12, style="Custom.Treeview")
            
            # Define headings
            headings = ['ID', 'First Name', 'Last Name', 'Street', 'City', 'State', 'ZIP', 'Phone', 'Gets Seasick']
            for col, heading in zip(columns, headings):
                self.passenger_tree.heading(col, text=heading)
                self.passenger_tree.column(col, width=100)
            
            # Add data
            for passenger in passengers:
                self.passenger_tree.insert('', tk.END, values=(
                    passenger.passenger_id,
                    passenger.first_name,
                    passenger.last_name,
                    passenger.street or '',
                    passenger.city or '',
                    passenger.state or '',
                    passenger.zip_code or '',
                    passenger.phone or '',
                    'Yes' if passenger.gets_seasick else 'No'
                ))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.passenger_tree.yview)
            self.passenger_tree.configure(yscrollcommand=scrollbar.set)
            
            # Grid layout
            self.passenger_tree.grid(row=2, column=0, columnspan=3, sticky="nsew")
            scrollbar.grid(row=2, column=3, sticky="ns")
            
        except Exception as e:
            error_label = ttk.Label(self.content_frame, text=f"Error loading passengers: {str(e)}")
            error_label.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Configure grid weights
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(2, weight=1)
    
    def add_passenger(self):
        """Add a new passenger through BLL"""
        dialog = PassengerDialog(self.root, "Add Passenger", self.colors)

        if dialog.result:
            first_name, last_name, phone = dialog.result
            result = self.mrc_bll.add_new_passenger(first_name, last_name, phone)
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.manage_passengers()
            else:
                messagebox.showerror("Error", result["message"])
        else:
            messagebox.showwarning("Warning", "No passenger details added")
    
    def delete_passenger(self):
        """Delete selected passenger through BLL"""
        if not hasattr(self, 'passenger_tree'):
            messagebox.showwarning("Warning", "No passenger list available")
            return
        
        selection = self.passenger_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a passenger to delete")
            return
        
        item = self.passenger_tree.item(selection[0])
        passenger_id = item['values'][0]
        passenger_name = f"{item['values'][1]} {item['values'][2]}"
        
        confirmation_message = (f"⚠️ Are you sure you want to delete this passenger?\n\n"
                            f"Name: {passenger_name}\n"
                            f"ID: {passenger_id}\n\n"
                            f"⚠️ WARNING: This action cannot be undone!")
        
        if messagebox.askyesno("Confirm Delete", confirmation_message):
            
            result = self.mrc_bll.delete_passenger_by_id(passenger_id)
            
            if result["success"]:
                messagebox.showinfo("Success", f"✅ {result['message']}")
                self.manage_passengers()
            else:
                messagebox.showerror("Delete Failed", f"❌ {result['message']}")
  
    def add_vessel(self):
        """Add a new vessel through BLL"""
        dialog = VesselDialog(self.root, "Add Vessel", self.colors)
        if dialog.result:
            vessel_name, cost_per_hour = dialog.result
            
            result = self.mrc_bll.add_new_vessel(vessel_name, cost_per_hour)
            
            if result["success"]:
                messagebox.showinfo("Success", result["message"])
                self.manage_vessels()
            else:
                messagebox.showerror("Error", result["message"])

    def manage_vessels(self):
        """Display vessel management interface"""
        self.clear_content_frame()
        
        # Title
        title_label = ttk.Label(self.content_frame, text="Vessel Management", style='Header.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Buttons
        add_btn = ttk.Button(self.content_frame, text="➕ Add Vessel", command=self.add_vessel, style='Success.TButton')
        add_btn.grid(row=1, column=0, padx=5, pady=5)
        
        delete_btn = ttk.Button(self.content_frame, text="🗑️ Delete Vessel", command=self.delete_vessel, style='Danger.TButton')
        delete_btn.grid(row=1, column=1, padx=5, pady=5)
        
        refresh_btn = ttk.Button(self.content_frame, text="🔄 Refresh", command=self.manage_vessels)
        refresh_btn.grid(row=1, column=2, padx=5, pady=5)
        
        try:
            vessels = self.mrc_bll.get_all_vessels_list()
            
            if not vessels:
                no_data_label = ttk.Label(self.content_frame, text="No vessels found")
                no_data_label.grid(row=2, column=0, columnspan=3, pady=20)
                return
            
            # Create treeview for vessels
            columns = ('id', 'name', 'cost_per_hour')
            self.vessel_tree = Treeview(self.content_frame, columns=columns, show='headings', height=12, style="Custom.Treeview")
            
            # Define headings
            self.vessel_tree.heading('id', text='ID')
            self.vessel_tree.heading('name', text='Vessel Name')
            self.vessel_tree.heading('cost_per_hour', text='Cost per Hour')
            
            # Configure column widths
            self.vessel_tree.column('id', width=80)
            self.vessel_tree.column('name', width=200)
            self.vessel_tree.column('cost_per_hour', width=150)
            
            # Add data
            for vessel in vessels:
                cost_str = f"${vessel.cost_per_hour:.2f}" if isinstance(vessel.cost_per_hour, (int, float, Decimal)) else str(vessel.cost_per_hour)
                self.vessel_tree.insert('', tk.END, values=(
                    vessel.vessel_id,
                    vessel.vessel_name,
                    cost_str
                ))
            
            # Add scrollbar
            scrollbar = ttk.Scrollbar(self.content_frame, orient=tk.VERTICAL, command=self.vessel_tree.yview)
            self.vessel_tree.configure(yscrollcommand=scrollbar.set)
            
            # Grid layout
            self.vessel_tree.grid(row=2, column=0, columnspan=3, sticky="nsew")
            scrollbar.grid(row=2, column=3, sticky="ns")
            
        except Exception as e:
            error_label = ttk.Label(self.content_frame, text=f"Error loading vessels: {str(e)}")
            error_label.grid(row=2, column=0, columnspan=3, pady=20)
        
        # Configure grid weights
        self.content_frame.columnconfigure(0, weight=1)
        self.content_frame.rowconfigure(2, weight=1)

    def delete_vessel(self):
        """Delete selected vessel through BLL"""
        if not hasattr(self, 'vessel_tree'):
            messagebox.showwarning("Warning", "No vessel list available")
            return
        
        selection = self.vessel_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a vessel to delete")
            return
        
        item = self.vessel_tree.item(selection[0])
        vessel_id = item['values'][0]
        vessel_name = item['values'][1]
        
        confirmation_message = (f"⚠️ Are you sure you want to delete this vessel?\n\n"
                            f"Name: {vessel_name}\n"
                            f"ID: {vessel_id}\n\n"
                            f"⚠️ WARNING: This action cannot be undone!")
        
        if messagebox.askyesno("Confirm Delete", confirmation_message):
            result = self.mrc_bll.delete_vessel_by_id(vessel_id)
            
            if result["success"]:
                messagebox.showinfo("Success", f"✅ {result['message']}")
                self.manage_vessels()  # Refresh the view
            else:
                messagebox.showerror("Delete Failed", f"❌ {result['message']}")
    
    def add_trip(self):
        """Add a new trip with overlap checking"""
        dialog = TripDialog(self.root, self.mrc_bll, self.colors)
        if dialog.result:
            vessel_name, passenger_name, trip_date, departure_time, length_hours, total_passengers = dialog.result
            
            try:
                # Parse passenger name
                passenger_parts = passenger_name.split(' ', 1)
                if len(passenger_parts) != 2:
                    messagebox.showerror("Error", "Invalid passenger name format")
                    return
                
                first_name, last_name = passenger_parts
                
                booking_check = self.mrc_bll.check_double_booking(
                    vessel_name, first_name, last_name,
                    trip_date, departure_time, length_hours
                )
                
                if booking_check["conflict"]:
                    messagebox.showwarning("Double Booking", 
                                         f"Booking conflict: {booking_check['message']}")
                    return
                
                # Add the trip
                result = self.mrc_bll.add_new_trip_existing_entities(
                    vessel_name, first_name, last_name,
                    trip_date, departure_time, length_hours, total_passengers
                )
                
                if "successfully" in result.lower():
                    messagebox.showinfo("Success", result)
                else:
                    messagebox.showerror("Error", result)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error adding trip: {str(e)}")
    
    def logout(self):
        """Logout and return to login screen"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            try:
                self.mrc_bll.close_connection()
            except:
                pass
            self.logged_in = False
            self.show_login_screen()
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

class PassengerDialog:
    def __init__(self, parent, title, colors):
        self.result = None
        self.colors = colors

        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.configure(bg=self.colors['text_secondary'])
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Container frame
        main_frame = tk.Frame(self.dialog, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form frame
        form_frame = tk.Frame(main_frame, bg='white', relief='raised', borderwidth=1)
        form_frame.pack(padx=10, pady=10)

        tk.Label(form_frame, text="First Name:", bg='white', fg='black', font=('Segoe UI', 10)).grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.first_name_entry = tk.Entry(form_frame, bg='white', fg='black', font=('Segoe UI', 10))
        self.first_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Last Name:", bg='white', fg='black', font=('Segoe UI', 10)).grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.last_name_entry = tk.Entry(form_frame, bg='white', fg='black', font=('Segoe UI', 10))
        self.last_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Phone:", bg='white', fg='black', font=('Segoe UI', 10)).grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.phone_entry = tk.Entry(form_frame, bg='white', fg='black', font=('Segoe UI', 10))
        self.phone_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons frame
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_light'])
        button_frame.pack(pady=10)

        ok_btn = ttk.Button(button_frame, text="✅ OK", command=self.ok_clicked, style='Success.TButton')
        ok_btn.grid(row=0, column=0, padx=5)

        cancel_btn = ttk.Button(button_frame, text="❌ Cancel", command=self.cancel_clicked, style='Danger.TButton')
        cancel_btn.grid(row=0, column=1, padx=5)

        self.dialog.bind('<Return>', lambda event: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda event: self.cancel_clicked())
        self.first_name_entry.focus()

        parent.wait_window(self.dialog)

    def ok_clicked(self):
        first_name = self.first_name_entry.get().strip()
        last_name = self.last_name_entry.get().strip()
        phone = self.phone_entry.get().strip()

        if not all([first_name, last_name, phone]):
            messagebox.showerror("Error", "All fields are required")
            return

        self.result = (first_name, last_name, phone)
        self.dialog.destroy()

    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

class VesselDialog:
    def __init__(self, parent, title, colors):
        self.result = None
        self.colors = colors
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"🚢 {title}")
        self.dialog.configure(bg=self.colors['text_secondary'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(padx="10", pady="10")
        
        # Form fields
        ttk.Label(main_frame, text="Vessel Name:", font=('Segoe UI', 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.vessel_name_entry = ttk.Entry(main_frame, width=20, font=('Segoe UI', 10))
        self.vessel_name_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Cost per Hour ($):", font=('Segoe UI', 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.cost_entry = ttk.Entry(main_frame, width=20, font=('Segoe UI', 10))
        self.cost_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Add placeholder text for cost
        self.cost_entry.insert(0, "0.00")
        self.cost_entry.bind('<FocusIn>', self.on_cost_focus_in)
        self.cost_entry.bind('<FocusOut>', self.on_cost_focus_out)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ok_btn = ttk.Button(button_frame, text="✅ OK", command=self.ok_clicked, style='Success.TButton')
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancel", command=self.cancel_clicked, style='Danger.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Focus on first entry and bind Enter key
        self.vessel_name_entry.focus()
        self.dialog.bind('<Return>', lambda event: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda event: self.cancel_clicked())

        parent.wait_window(self.dialog)
    
    def on_cost_focus_in(self, event):
        """Clear placeholder text when user clicks on cost field"""
        if self.cost_entry.get() == "0.00":
            self.cost_entry.delete(0, tk.END)
    
    def on_cost_focus_out(self, event):
        """Restore placeholder if field is empty"""
        if not self.cost_entry.get().strip():
            self.cost_entry.insert(0, "0.00")
    
    def ok_clicked(self):
        vessel_name = self.vessel_name_entry.get().strip()
        cost_str = self.cost_entry.get().strip()
        
        # Validation
        if not vessel_name:
            messagebox.showerror("Error", "Vessel name is required")
            return
        
        if not cost_str or cost_str == "0.00":
            messagebox.showerror("Error", "Cost per hour is required")
            return
        
        try:
            cost_per_hour = float(cost_str)
            if cost_per_hour <= 0:
                messagebox.showerror("Error", "Cost per hour must be greater than 0")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for cost per hour")
            return
        
        # Format to 2 decimal places
        cost_per_hour = round(cost_per_hour, 2)
        
        self.result = (vessel_name, cost_per_hour)
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()

class TripDialog:
    def __init__(self, parent, mrc_bll, colors):
        self.result = None
        self.mrc_bll = mrc_bll

        self.colors = colors
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("🛥️ Add Trip")
        self.dialog.geometry("450x400")
        self.dialog.configure(bg=self.colors['bg_primary'])
        self.dialog.resizable(False, False)
        self.dialog.grab_set()
        
        # Add a subtle border
        self.dialog.configure(relief='raised', borderwidth=2)
        
        # Center the dialog
        self.dialog.transient(parent)
        
        # Create form
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Get vessels and passengers for dropdowns
        self.load_data()

        # Configure styles for consistent white backgrounds
        style = ttk.Style()

        # More comprehensive combobox styling
        style.configure('White.TCombobox',
                        fieldbackground='white',
                        background='white',
                        foreground='black',
                        selectbackground='#3498db',
                        selectforeground='white',
                        insertcolor='black',
                        borderwidth=1,
                        relief='solid')

        # Map different states for combobox
        style.map('White.TCombobox',
                fieldbackground=[('readonly', 'white'),
                                ('focus', 'white'),
                                ('!focus', 'white')],
                background=[('readonly', 'white'),
                            ('focus', 'white'),
                            ('!focus', 'white')],
                selectbackground=[('focus', '#3498db')])

        # Entry styling
        style.configure('White.TEntry',
                        fieldbackground='white',
                        background='white',
                        foreground='black',
                        insertcolor='black',
                        borderwidth=1,
                        relief='solid')

        style.map('White.TEntry',
                fieldbackground=[('focus', 'white'),
                                ('!focus', 'white')])
        
        # Vessel selection
        ttk.Label(main_frame, text="Vessel:", font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        self.vessel_combo = Combobox(main_frame, style='White.TCombobox', values=self.vessel_names, state="readonly", width=25, font=('Segoe UI', 10))
        self.vessel_combo.grid(row=0, column=1, pady=5, padx=(10, 0), sticky="w")
        
        # Passenger selection
        ttk.Label(main_frame, text="Passenger:", font=('Segoe UI', 10, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        self.passenger_combo = Combobox(main_frame, style='White.TCombobox', values=self.passenger_names, state="readonly", width=25, font=('Segoe UI', 10))
        self.passenger_combo.grid(row=1, column=1, pady=5, padx=(10, 0), sticky="w")
        
        # Date selection
        ttk.Label(main_frame, text="Trip Date:", font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky="w", pady=5)
        self.date_picker = DateEntry(main_frame, width=12, background='#3498db',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                   font=('Segoe UI', 10))
        self.date_picker.grid(row=2, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Time selection
        ttk.Label(main_frame, text="Departure Time:", font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky="w", pady=5)
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=3, column=1, sticky="w", pady=5, padx=(10, 0))
        
        self.hour_combo = Combobox(time_frame, style='White.TCombobox', values=[f"{i:02d}" for i in range(24)], 
                                 state="readonly", width=5, font=('Segoe UI', 10))
        self.hour_combo.pack(side=tk.LEFT)
        self.hour_combo.set("09")
        
        ttk.Label(time_frame, text=":", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT, padx=5)
        
        self.minute_combo = Combobox(time_frame, style='White.TCombobox', values=[f"{i:02d}" for i in range(0, 60, 15)], 
                                   state="readonly", width=5, font=('Segoe UI', 10))
        self.minute_combo.pack(side=tk.LEFT)
        self.minute_combo.set("00")
        
        ttk.Label(time_frame, text="(24-hour format)", font=('Segoe UI', 8), foreground='gray').pack(side=tk.LEFT, padx=(10, 0))
        
        # Trip length
        ttk.Label(main_frame, text="Length (hours):", font=('Segoe UI', 10, 'bold')).grid(row=4, column=0, sticky="w", pady=5)
        length_frame = ttk.Frame(main_frame)
        length_frame.grid(row=4, column=1, sticky="w", pady=5, padx=(10, 0))
        
        self.length_entry = ttk.Entry(length_frame, style='White.TEntry', width=8, font=('Segoe UI', 10))
        self.length_entry.pack(side=tk.LEFT)
        self.length_entry.insert(0, "2.0")
        
        ttk.Label(length_frame, text="hours", font=('Segoe UI', 9), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Total passengers
        ttk.Label(main_frame, text="Total Passengers:", font=('Segoe UI', 10, 'bold')).grid(row=5, column=0, sticky="w", pady=5)
        passengers_frame = ttk.Frame(main_frame)
        passengers_frame.grid(row=5, column=1, sticky="w", pady=5, padx=(10, 0))
        
        self.passengers_entry = ttk.Entry(passengers_frame, style='White.TEntry', width=8, font=('Segoe UI', 10))
        self.passengers_entry.pack(side=tk.LEFT)
        self.passengers_entry.insert(0, "1")
        
        ttk.Label(passengers_frame, text="people", font=('Segoe UI', 9), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Info label
        info_label = ttk.Label(main_frame, 
                              text="💡 The system will check for booking conflicts automatically",
                              font=('Segoe UI', 9), 
                              foreground='#7f8c8d')
        info_label.grid(row=6, column=0, columnspan=2, pady=(15, 5))
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ok_btn = ttk.Button(button_frame, text="🚀 Add Trip", command=self.ok_clicked, style='Success.TButton')
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = ttk.Button(button_frame, text="❌ Cancel", command=self.cancel_clicked, style='Danger.TButton')
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Focus on vessel combo and bind keys
        self.vessel_combo.focus()
        self.dialog.bind('<Return>', lambda event: self.ok_clicked())
        self.dialog.bind('<Escape>', lambda event: self.cancel_clicked())
        
        # Bind focus events
        self.length_entry.bind('<FocusIn>', self.on_length_focus_in)
        self.passengers_entry.bind('<FocusIn>', self.on_passengers_focus_in)

        parent.wait_window(self.dialog)
    
    def load_data(self):
        """Load vessels and passengers for dropdowns using BLL"""
        try:
            vessels = self.mrc_bll.get_all_vessels_list()
            self.vessel_names = [v.vessel_name for v in vessels] if vessels else []

            passengers = self.mrc_bll.get_all_passengers_list()
            self.passenger_names = [f"{p.first_name} {p.last_name}" for p in passengers] if passengers else []

            if not self.vessel_names:
                self.vessel_names = ["No vessels available - Add vessels first"]
            if not self.passenger_names:
                self.passenger_names = ["No passengers available - Add passengers first"]
        except Exception as e:
            print(f"Error loading data: {e}")
            self.vessel_names = ["Error loading vessels"]
            self.passenger_names = ["Error loading passengers"]

    
    def on_length_focus_in(self, event):
        """Select all text when length field is focused"""
        self.length_entry.select_range(0, tk.END)
    
    def on_passengers_focus_in(self, event):
        """Select all text when passengers field is focused"""
        self.passengers_entry.select_range(0, tk.END)
    
    def ok_clicked(self):
        vessel_name = self.vessel_combo.get()
        passenger_name = self.passenger_combo.get()
        trip_date = self.date_picker.get_date()
        
        hour = self.hour_combo.get()
        minute = self.minute_combo.get()
        length_str = self.length_entry.get().strip()
        passengers_str = self.passengers_entry.get().strip()
        
        # Validation
        if not vessel_name or vessel_name.startswith("No vessels") or vessel_name.startswith("Error"):
            messagebox.showerror("Error", "Please select a valid vessel")
            return
        
        if not passenger_name or passenger_name.startswith("No passengers") or passenger_name.startswith("Error"):
            messagebox.showerror("Error", "Please select a valid passenger")
            return
        
        if not all([hour, minute, length_str, passengers_str]):
            messagebox.showerror("Error", "All fields are required")
            return
        
        try:
            departure_time = time(int(hour), int(minute))
        except ValueError:
            messagebox.showerror("Error", "Invalid time format")
            return
        
        try:
            length_hours = float(length_str)
            if length_hours <= 0 or length_hours > 24:
                messagebox.showerror("Error", "Trip length must be between 0.1 and 24 hours")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for trip length")
            return
        
        try:
            total_passengers = int(passengers_str)
            if total_passengers <= 0 or total_passengers > 50:
                messagebox.showerror("Error", "Number of passengers must be between 1 and 50")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number for passengers")
            return
        
        # Check if date is not in the past
        from datetime import date as date_class
        if trip_date < date_class.today():
            if not messagebox.askyesno("Past Date Warning", 
                                     "The selected date is in the past. Do you want to continue?"):
                return
        
        self.result = (vessel_name, passenger_name, trip_date, departure_time, length_hours, total_passengers)
        self.dialog.destroy()
    
    def cancel_clicked(self):
        self.result = None
        self.dialog.destroy()