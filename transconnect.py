# Import required Python libraries
import time
from typing import Dict, List
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk  # For modern styling (pip install ttkbootstrap)
import folium
from geopy.geocoders import Nominatim
from geopy.location import Location
from geopy import distance
import webbrowser
import os

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
        "start_gps": "13.4488, 121.8386",  # Boac town proper
        "end_gps": "13.4819, 121.8637",    # Mogpog town proper
        "seats": 15,
        "schedule": "7:00 AM"
    },
    2: {
        "name": "Mogpog to Santa Cruz", 
        "start_gps": "13.4819, 121.8637",  # Mogpog town proper
        "end_gps": "13.4280, 122.0094",    # Santa Cruz town proper
        "seats": 15,
        "schedule": "9:00 AM"
    },
    3: {
        "name": "Santa Cruz to Torrijos",
        "start_gps": "13.4280, 122.0094",  # Santa Cruz town proper
        "end_gps": "13.3127, 122.0871",    # Torrijos town proper
        "seats": 15,
        "schedule": "11:00 AM"
    },
    4: {
        "name": "Torrijos to Buenavista",
        "start_gps": "13.3127, 122.0871",  # Torrijos town proper
        "end_gps": "13.2574, 121.9226",    # Buenavista town proper
        "seats": 15,
        "schedule": "1:00 PM"
    },
    5: {
        "name": "Buenavista to Gasan",
        "start_gps": "13.2574, 121.9226",  # Buenavista town proper
        "end_gps": "13.3197, 121.8685",    # Gasan town proper
        "seats": 15,
        "schedule": "3:00 PM"
    },
    6: {
        "name": "Gasan to Boac",
        "start_gps": "13.3197, 121.8685",  # Gasan town proper
        "end_gps": "13.4488, 121.8386",    # Boac town proper
        "seats": 15,
        "schedule": "3:00 PM"
    }
}

def get_current_location():
    """Get the current location using geopy's Nominatim service"""
    try:
        geolocator = Nominatim(user_agent="transconnect")
        # For demo purposes, we'll use Marinduque's center coordinates
        # In a real app, you'd use device GPS or IP-based location
        location = geolocator.reverse("13.4013° N, 121.9694° E")
        return location
    except Exception as e:
        print(f"Error getting location: {e}")
        return None

class TransConnectApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TransConnect")
        self.root.geometry("1024x768")  # Larger window
        self.current_user = None
        
        # Configure style with a modern theme and custom colors
        style = ttk.Style()
        style.theme_use('darkly')
        
        # Configure custom styles
        style.configure('Header.TLabel', font=("Helvetica", 32, "bold"), foreground='#2196F3')
        style.configure('SubHeader.TLabel', font=("Helvetica", 14), foreground='#757575')
        style.configure('Card.TFrame', background='#2A2A2A', relief='raised', borderwidth=1)
        style.configure('Action.TButton', font=("Helvetica", 11), padding=10)
        
        self.setup_main_frame()
        self.show_login_frame()
    
    def setup_main_frame(self):
        # Create main container with gradient background
        self.main_frame = ttk.Frame(self.root, padding="40")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with logo and tagline
        header = ttk.Label(
            self.main_frame,
            text="TransConnect",
            style='Header.TLabel'
        )
        header.pack(pady=(0, 5))
        
        subheader = ttk.Label(
            self.main_frame,
            text="Your Gateway to Seamless Travel in Marinduque",
            style='SubHeader.TLabel'
        )
        subheader.pack(pady=(0, 30))
    
    def show_login_frame(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create card-like container
        login_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        login_frame.pack(pady=20, padx=20, ipadx=40, ipady=30)
        
        # Login header
        ttk.Label(
            login_frame,
            text="Welcome Back",
            font=("Helvetica", 18, "bold"),
            foreground='#2196F3'
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Styled input fields
        ttk.Label(login_frame, text="Email:", font=("Helvetica", 11)).grid(row=1, column=0, pady=10, sticky='e', padx=10)
        email_entry = ttk.Entry(login_frame, width=35, font=("Helvetica", 11))
        email_entry.grid(row=1, column=1, pady=10, padx=10)
        
        ttk.Label(login_frame, text="Password:", font=("Helvetica", 11)).grid(row=2, column=0, pady=10, sticky='e', padx=10)
        password_entry = ttk.Entry(login_frame, width=35, show="•", font=("Helvetica", 11))
        password_entry.grid(row=2, column=1, pady=10, padx=10)
        
        # Styled buttons
        button_frame = ttk.Frame(login_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=25)
        
        login_btn = ttk.Button(
            button_frame,
            text="Login",
            style='Action.TButton',
            command=lambda: self.handle_login(email_entry.get(), password_entry.get())
        )
        login_btn.pack(side=tk.LEFT, padx=10)
        
        register_btn = ttk.Button(
            button_frame,
            text="Create Account",
            style='Action.TButton',
            command=self.show_register_frame
        )
        register_btn.pack(side=tk.LEFT, padx=10)
    
    def show_register_frame(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create modern registration card
        register_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        register_frame.pack(pady=20, padx=40, ipadx=40, ipady=30)
        
        # Registration header
        ttk.Label(
            register_frame,
            text="Create Your Account",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(20, 10))
        
        ttk.Label(
            register_frame,
            text="Join TransConnect today and start your journey",
            font=("Helvetica", 12),
            foreground='#757575'
        ).pack(pady=(0, 30))
        
        # Input container
        input_frame = ttk.Frame(register_frame)
        input_frame.pack(fill=tk.X, padx=20)
        
        # Styled input fields
        fields = [
            ("Full Name", "name_entry"),
            ("Email Address", "email_entry"),
            ("Password", "password_entry", "*")
        ]
        
        entries = {}
        for i, (label, key, *args) in enumerate(fields):
            ttk.Label(
                input_frame,
                text=label,
                font=("Helvetica", 11, "bold"),
                foreground='#424242'
            ).pack(anchor='w', pady=(10, 5))
            
            entry = ttk.Entry(
                input_frame,
                width=40,
                font=("Helvetica", 11),
                show="•" if args else ""
            )
            entry.pack(fill=tk.X, pady=(0, 10))
            entries[key] = entry
        
        # Button container
        button_frame = ttk.Frame(register_frame)
        button_frame.pack(pady=30)
        
        # Styled buttons
        register_btn = ttk.Button(
            button_frame,
            text="Create Account",
            style='Action.TButton',
            command=lambda: self.handle_register(
                entries['name_entry'].get(),
                entries['email_entry'].get(),
                entries['password_entry'].get()
            )
        )
        register_btn.pack(side=tk.LEFT, padx=10)
        
        back_btn = ttk.Button(
            button_frame,
            text="Back to Login",
            style='Action.TButton',
            command=self.show_login_frame
        )
        back_btn.pack(side=tk.LEFT, padx=10)

    def show_user_dashboard(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create modern dashboard layout
        dashboard_frame = ttk.Frame(self.main_frame)
        dashboard_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Welcome section with user info
        welcome_frame = ttk.Frame(dashboard_frame, style='Card.TFrame')
        welcome_frame.pack(fill=tk.X, padx=20, pady=10, ipady=15)
        
        ttk.Label(
            welcome_frame,
            text=f"Welcome back, {users[self.current_user]['name']}",
            font=("Helvetica", 20, "bold"),
            foreground='#2196F3'
        ).pack(pady=(10, 5))
        
        ttk.Label(
            welcome_frame,
            text="Manage your travel arrangements below",
            font=("Helvetica", 12),
            foreground='#757575'
        ).pack()
        
        # Dashboard grid layout
        grid_frame = ttk.Frame(dashboard_frame)
        grid_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        
        # Dashboard cards
        self.create_dashboard_card(
            grid_frame, 0, 0,
            "View Routes",
            "Browse available transportation routes",
            self.show_routes
        )
        
        self.create_dashboard_card(
            grid_frame, 0, 1,
            "Book a Seat",
            "Reserve your spot on a route",
            self.show_booking_form
        )
        
        self.create_dashboard_card(
            grid_frame, 1, 0,
            "My Bookings",
            "Check your travel schedule",
            self.show_my_bookings
        )
        
        self.create_dashboard_card(
            grid_frame, 1, 1,
            "Logout",
            "Sign out of your account",
            self.logout
        )

    def create_dashboard_card(self, parent, row, col, title, description, command):
        card = ttk.Frame(parent, style='Card.TFrame')
        card.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
        
        ttk.Label(
            card,
            text=title,
            font=("Helvetica", 16, "bold"),
            foreground='#2196F3'
        ).pack(pady=(20, 5))
        
        ttk.Label(
            card,
            text=description,
            font=("Helvetica", 11),
            foreground='#757575'
        ).pack(pady=(0, 15))
        
        ttk.Button(
            card,
            text="Open",
            style='Action.TButton',
            command=command
        ).pack(pady=(0, 20))
        
        # Add map button to dashboard
        if title == "View Routes":
            ttk.Button(
                card,
                text="View Map",
                style='Action.TButton',
                command=self.show_location_map
            ).pack(pady=(0, 20))

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
        
        # Create container
        routes_frame = ttk.Frame(self.main_frame)
        routes_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            routes_frame,
            text="Available Routes",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Create canvas and scrollbar for scrolling
        canvas = tk.Canvas(routes_frame)
        scrollbar = ttk.Scrollbar(routes_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_reqwidth())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=(40, 0))
        
        # Display routes in modern cards
        for route_id, route_info in ROUTES.items():
            route_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
            route_card.pack(pady=10, fill=tk.X, ipady=15)
            
            # Route header
            ttk.Label(
                route_card,
                text=f"Route {route_id}",
                font=("Helvetica", 14, "bold"),
                foreground='#2196F3'
            ).pack(anchor="w", padx=20, pady=(10, 5))
            
            ttk.Label(
                route_card,
                text=route_info['name'],
                font=("Helvetica", 12, "bold"),
                foreground='#424242'
            ).pack(anchor="w", padx=20)
            
            # Route details
            details_frame = ttk.Frame(route_card)
            details_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
            
            # Schedule
            schedule_frame = ttk.Frame(details_frame)
            schedule_frame.pack(side=tk.LEFT, padx=(0, 30))
            
            ttk.Label(
                schedule_frame,
                text="Schedule",
                font=("Helvetica", 10),
                foreground='#757575'
            ).pack(anchor="w")
            
            ttk.Label(
                schedule_frame,
                text=route_info['schedule'],
                font=("Helvetica", 12, "bold"),
                foreground='#424242'
            ).pack(anchor="w")
            
            # Available seats
            seats_frame = ttk.Frame(details_frame)
            seats_frame.pack(side=tk.LEFT)
            
            ttk.Label(
                seats_frame,
                text="Available Seats",
                font=("Helvetica", 10),
                foreground='#757575'
            ).pack(anchor="w")
            
            ttk.Label(
                seats_frame,
                text=str(route_info['seats']),
                font=("Helvetica", 12, "bold"),
                foreground='#424242'
            ).pack(anchor="w")
        
        # Back button with unbinding
        def on_back():
            self.root.unbind_all("<MouseWheel>")  # Unbind mousewheel before destroying
            self.show_user_dashboard()
        
        ttk.Button(
            routes_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=on_back
        ).pack(pady=30)
        
        # Configure canvas scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        self.root.bind_all("<MouseWheel>", on_mousewheel)

    def show_booking_form(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create booking container
        booking_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        booking_frame.pack(pady=20, padx=40, ipadx=40, ipady=30)
        
        # Booking header
        ttk.Label(
            booking_frame,
            text="Book Your Trip",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(20, 10))
        
        ttk.Label(
            booking_frame,
            text="Select your preferred route and schedule",
            font=("Helvetica", 12),
            foreground='#757575'
        ).pack(pady=(0, 30))
        
        # Route selection
        ttk.Label(
            booking_frame,
            text="Select Route",
            font=("Helvetica", 11, "bold"),
            foreground='#424242'
        ).pack(anchor='w', padx=20, pady=(10, 5))
        
        route_var = tk.StringVar()
        route_combo = ttk.Combobox(
            booking_frame,
            textvariable=route_var,
            font=("Helvetica", 11),
            width=40
        )
        route_combo['values'] = [f"{r['name']}" for r in ROUTES.values()]
        route_combo.pack(padx=20, pady=(0, 20))
        
        # Button container
        button_frame = ttk.Frame(booking_frame)
        button_frame.pack(pady=30)
        
        # Action buttons
        ttk.Button(
            button_frame,
            text="Confirm Booking",
            style='Action.TButton',
            command=lambda: self.handle_booking(route_var.get())
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=self.show_user_dashboard
        ).pack(side=tk.LEFT, padx=10)

    def show_my_bookings(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create bookings container
        bookings_frame = ttk.Frame(self.main_frame)
        bookings_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            bookings_frame,
            text="My Bookings",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Bookings container
        bookings_container = ttk.Frame(bookings_frame)
        bookings_container.pack(fill=tk.BOTH, expand=True, padx=40)
        
        if not users[self.current_user]['bookings']:
            empty_frame = ttk.Frame(bookings_container, style='Card.TFrame')
            empty_frame.pack(pady=20, ipady=30, fill=tk.X)
            
            ttk.Label(
                empty_frame,
                text="No bookings found",
                font=("Helvetica", 14),
                foreground='#757575'
            ).pack()
            
            ttk.Label(
                empty_frame,
                text="Book your first trip now!",
                font=("Helvetica", 12),
                foreground='#757575'
            ).pack()
        else:
            for booking in users[self.current_user]['bookings']:
                booking_card = ttk.Frame(bookings_container, style='Card.TFrame')
                booking_card.pack(pady=10, fill=tk.X, ipady=15)
                
                ttk.Label(
                    booking_card,
                    text=booking['route_name'],
                    font=("Helvetica", 14, "bold"),
                    foreground='#2196F3'
                ).pack(anchor="w", padx=20, pady=(10, 5))
                
                # Get schedule time from ROUTES using route_id
                schedule_time = ROUTES[booking['route_id']]['schedule']
                
                ttk.Label(
                    booking_card,
                    text=f"Travel Date: {booking['date']} at {schedule_time}",
                    font=("Helvetica", 12),
                    foreground='#424242'
                ).pack(anchor="w", padx=20)
        
        # Back button
        ttk.Button(
            bookings_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=self.show_user_dashboard
        ).pack(pady=30)

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

    def show_location_map(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create map container
        map_frame = ttk.Frame(self.main_frame)
        map_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            map_frame,
            text="Location & Routes Map",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Create a map centered on Marinduque
        m = folium.Map(
            location=[13.4013, 121.9694],
            zoom_start=11
        )
        
        # Add markers and lines for all routes
        for route_id, route in ROUTES.items():
            # Parse start and end coordinates
            start_coords = [float(x.strip('° NSEW')) for x in route['start_gps'].split(',')]
            end_coords = [float(x.strip('° NSEW')) for x in route['end_gps'].split(',')]
            
            # Add markers for start and end points
            folium.Marker(
                start_coords,
                popup=f"Start: {route['name']}",
                icon=folium.Icon(color='green')
            ).add_to(m)
            
            folium.Marker(
                end_coords,
                popup=f"End: {route['name']}",
                icon=folium.Icon(color='blue')
            ).add_to(m)
            
            # Draw line between points
            folium.PolyLine(
                locations=[start_coords, end_coords],
                weight=2,
                color='red',
                popup=f"Route {route_id}: {route['name']}"
            ).add_to(m)
        
        # Save map to HTML file
        map_file = "route_map.html"
        m.save(map_file)
        
        # Create info frame
        info_frame = ttk.Frame(map_frame, style='Card.TFrame')
        info_frame.pack(fill=tk.X, padx=40, pady=20)
        
        # Button to open map in browser
        ttk.Button(
            info_frame,
            text="Open Map in Browser",
            style='Action.TButton',
            command=lambda: webbrowser.open('file://' + os.path.realpath(map_file))
        ).pack(pady=10)
        
        # Back button
        ttk.Button(
            map_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=self.show_user_dashboard
        ).pack(pady=30)

# Update the main function to use the GUI
def main():
    root = ttk.Window()
    app = TransConnectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
