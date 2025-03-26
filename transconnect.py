# Import required Python libraries
import time
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk  # For modern styling (pip install ttkbootstrap)

# Create in-memory storage using dictionaries and lists
# users: stores user information like name, email, password, and their bookings
# bookings: stores all booking information across the system
users: Dict[str, Dict] = {}
bookings: List[Dict] = []

# Define available transportation routes in Marinduque
# Each route has: name, GPS coordinates for start/end points, available seats, and schedule
ROUTES = {
    1: {
        "name": "Boac to Mogpog",
        "start_gps": "13.4462° N, 121.8354° E",  # Boac coordinates
        "end_gps": "13.4871° N, 121.8636° E",    # Mogpog coordinates
        "seats": 15,
        "schedule": "7:00 AM"
    },
    2: {
        "name": "Mogpog to Santa Cruz",
        "start_gps": "13.4871° N, 121.8636° E",  # Mogpog coordinates
        "end_gps": "13.4276° N, 122.0087° E",    # Santa Cruz coordinates
        "seats": 15,
        "schedule": "9:00 AM"
    }
}

class TransConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TransConnect")
        self.root.geometry("800x600")
        self.current_user = None
        
        # Configure style
        style = ttk.Style()
        style.theme_use('darkly')
        
        self.setup_main_frame()
        self.show_login_frame()
    
    def setup_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(
            self.main_frame,
            text="TransConnect",
            font=("Helvetica", 24, "bold")
        )
        header.pack(pady=20)
    
    def show_login_frame(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Login frame
        login_frame = ttk.Frame(self.main_frame)
        login_frame.pack(pady=20)
        
        # Email field
        ttk.Label(login_frame, text="Email:").grid(row=0, column=0, pady=5)
        email_entry = ttk.Entry(login_frame, width=30)
        email_entry.grid(row=0, column=1, pady=5)
        
        # Password field
        ttk.Label(login_frame, text="Password:").grid(row=1, column=0, pady=5)
        password_entry = ttk.Entry(login_frame, width=30, show="*")
        password_entry.grid(row=1, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Login",
            command=lambda: self.handle_login(email_entry.get(), password_entry.get())
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Register",
            command=self.show_register_frame
        ).pack(side=tk.LEFT, padx=5)
    
    def show_register_frame(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Register frame
        register_frame = ttk.Frame(self.main_frame)
        register_frame.pack(pady=20)
        
        # Registration fields
        ttk.Label(register_frame, text="Name:").grid(row=0, column=0, pady=5)
        name_entry = ttk.Entry(register_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(register_frame, text="Email:").grid(row=1, column=0, pady=5)
        email_entry = ttk.Entry(register_frame, width=30)
        email_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(register_frame, text="Password:").grid(row=2, column=0, pady=5)
        password_entry = ttk.Entry(register_frame, width=30, show="*")
        password_entry.grid(row=2, column=1, pady=5)
        
        # Buttons
        button_frame = ttk.Frame(register_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame,
            text="Register",
            command=lambda: self.handle_register(
                name_entry.get(),
                email_entry.get(),
                password_entry.get()
            )
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Back to Login",
            command=self.show_login_frame
        ).pack(side=tk.LEFT, padx=5)

    def show_user_dashboard(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Dashboard frame
        dashboard_frame = ttk.Frame(self.main_frame)
        dashboard_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Welcome message
        ttk.Label(
            dashboard_frame,
            text=f"Welcome, {users[self.current_user]['name']}!",
            font=("Helvetica", 16)
        ).pack(pady=10)
        
        # Dashboard buttons
        ttk.Button(
            dashboard_frame,
            text="View Routes",
            command=self.show_routes
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            dashboard_frame,
            text="Book a Seat",
            command=self.show_booking_form
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            dashboard_frame,
            text="View My Bookings",
            command=self.show_my_bookings
        ).pack(pady=5, fill=tk.X)
        
        ttk.Button(
            dashboard_frame,
            text="Logout",
            command=self.logout
        ).pack(pady=5, fill=tk.X)

    def handle_register(self, name, email, password):
        # Input validation
        if not name or not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Check if email already exists
        if email in users:
            messagebox.showerror("Error", "Email already registered!")
            return
        
        # Register new user
        users[email] = {
            "name": name,
            "password": password,
            "bookings": []
        }
        
        messagebox.showinfo("Success", "Registration successful! Please login.")
        self.show_login_frame()

    def handle_login(self, email, password):
        # Input validation
        if not email or not password:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        # Check if user exists and password matches
        if email in users and users[email]["password"] == password:
            self.current_user = email
            self.show_user_dashboard()
        else:
            messagebox.showerror("Error", "Invalid email or password!")

    def show_routes(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        routes_frame = ttk.Frame(self.main_frame)
        routes_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Display routes
        for route_id, route_info in ROUTES.items():
            route_frame = ttk.Frame(routes_frame)
            route_frame.pack(pady=10, fill=tk.X)
            
            ttk.Label(
                route_frame,
                text=f"Route {route_id}: {route_info['name']}",
                font=("Helvetica", 12, "bold")
            ).pack(anchor="w")
            
            ttk.Label(
                route_frame,
                text=f"Schedule: {route_info['schedule']} | Available Seats: {route_info['seats']}"
            ).pack(anchor="w")
        
        # Back button
        ttk.Button(
            routes_frame,
            text="Back to Dashboard",
            command=self.show_user_dashboard
        ).pack(pady=20)

    def show_booking_form(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        booking_frame = ttk.Frame(self.main_frame)
        booking_frame.pack(pady=20)
        
        ttk.Label(booking_frame, text="Select Route:").pack(pady=5)
        route_var = tk.StringVar()
        route_combo = ttk.Combobox(booking_frame, textvariable=route_var)
        route_combo['values'] = [f"{r['name']}" for r in ROUTES.values()]
        route_combo.pack(pady=5)
        
        ttk.Button(
            booking_frame,
            text="Book Seat",
            command=lambda: self.handle_booking(route_var.get())
        ).pack(pady=20)
        
        ttk.Button(
            booking_frame,
            text="Back to Dashboard",
            command=self.show_user_dashboard
        ).pack()

    def show_my_bookings(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        bookings_frame = ttk.Frame(self.main_frame)
        bookings_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        if not users[self.current_user]['bookings']:
            ttk.Label(
                bookings_frame,
                text="No bookings found.",
                font=("Helvetica", 12)
            ).pack(pady=20)
        else:
            for booking in users[self.current_user]['bookings']:
                booking_frame = ttk.Frame(bookings_frame)
                booking_frame.pack(pady=10, fill=tk.X)
                
                ttk.Label(
                    booking_frame,
                    text=f"Route: {booking['route_name']} | Date: {booking['date']}"
                ).pack(anchor="w")
        
        ttk.Button(
            bookings_frame,
            text="Back to Dashboard",
            command=self.show_user_dashboard
        ).pack(pady=20)

    def handle_booking(self, route_name):
        if not route_name:
            messagebox.showerror("Error", "Please select a route!")
            return
        
        # Find route_id from route_name
        route_id = None
        for rid, route in ROUTES.items():
            if route['name'] == route_name:
                route_id = rid
                break
        
        if route_id and ROUTES[route_id]['seats'] > 0:
            ROUTES[route_id]['seats'] -= 1
            booking = {
                'route_name': route_name,
                'date': time.strftime('%Y-%m-%d'),
                'route_id': route_id
            }
            users[self.current_user]['bookings'].append(booking)
            messagebox.showinfo("Success", "Booking confirmed!")
            self.show_user_dashboard()
        else:
            messagebox.showerror("Error", "No seats available!")

    def logout(self):
        self.current_user = None
        self.show_login_frame()

# Update the main function to use the GUI
def main():
    root = ttk.Window()
    app = TransConnectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
