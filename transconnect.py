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
users: Dict[str, Dict] = {
    "admin@gmail.com": {
        "name": "Admin",
        "password": "admin123",
        "is_admin": True,
        "bookings": []
    }
}
bookings: List[Dict] = []

# Define available transportation routes in Marinduque
# Each route has: name, GPS coordinates for start/end points, available seats, and schedule
ROUTES = {
    1: {
        "name": "Boac to Mogpog",
        "start_gps": "13.449078, 121.839003",  # Boac town proper
        "end_gps": "13.473615, 121.860948",    # Mogpog town proper
        "seats": 15,
        "schedule": "7:00 AM"
    },
    2: {
        "name": "Mogpog to Santa Cruz", 
        "start_gps": "13.473615, 121.860948",  # Mogpog town proper
        "end_gps": "13.475758368354766, 122.03110517819835",    # Santa Cruz town proper
        "seats": 15,
        "schedule": "9:00 AM"
    },
    3: {
        "name": "Santa Cruz to Torrijos",
        "start_gps": "13.475758368354766, 122.03110517819835",  # Santa Cruz town proper
        "end_gps": "13.320148, 122.084475",    # Torrijos town proper
        "seats": 15,
        "schedule": "11:00 AM"
    },
    4: {
        "name": "Torrijos to Buenavista",
        "start_gps": "13.320148, 122.084475",  # Torrijos town proper
        "end_gps": "13.473615, 121.860948",    # Buenavista town proper DONE
        "seats": 15,
        "schedule": "1:00 PM"
    },
    5: {
        "name": "Buenavista to Gasan",
        "start_gps": "13.473615, 121.860948",  # Buenavista town proper
        "end_gps": "13.328510, 121.845800",    # Gasan town proper
        "seats": 15,
        "schedule": "3:00 PM"
    },
    6: {
        "name": "Gasan to Boac",
        "start_gps": "13.328510, 121.845800",  # Gasan town proper
        "end_gps": "13.449078, 121.839003",    # Boac town proper
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
        self.root.geometry("1024x768")
        self.current_user = None
        self.is_admin = False
        
        # Configure style with a light theme and custom colors
        style = ttk.Style()
        style.theme_use('litera')  # Using a light theme
        
        # Configure custom styles with white background and modern accents
        style.configure('Header.TLabel', 
                       font=("Helvetica", 32, "bold"), 
                       foreground='#1976D2')  # Darker blue
        style.configure('SubHeader.TLabel', 
                       font=("Helvetica", 14), 
                       foreground='#616161')  # Darker gray
        style.configure('Card.TFrame', 
                       background='#FFFFFF',
                       relief='solid',
                       borderwidth=1)
        style.configure('Action.TButton', 
                       font=("Helvetica", 11),
                       padding=10,
                       background='#1976D2')  # Blue buttons
        
        # Configure the root window background
        self.root.configure(bg='#F5F5F5')  # Light gray background
        
        self.setup_main_frame()
        self.show_login_frame()
    
    def setup_main_frame(self):
        # Create main container with white background
        self.main_frame = ttk.Frame(self.root, padding="40", style='TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure main frame background
        style = ttk.Style()
        style.configure('TFrame', background='#F5F5F5')
        
        # Header with modern styling
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
        # Updated card style with shadows and hover effect
        card = ttk.Frame(parent, style='Card.TFrame')
        card.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
        
        # Add padding and modern styling
        inner_frame = ttk.Frame(card)
        inner_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        ttk.Label(
            inner_frame,
            text=title,
            font=("Helvetica", 16, "bold"),
            foreground='#1976D2'  # Darker blue
        ).pack(pady=(0, 5))
        
        ttk.Label(
            inner_frame,
            text=description,
            font=("Helvetica", 11),
            foreground='#616161'  # Darker gray
        ).pack(pady=(0, 15))
        
        button_text = "Logout" if title == "Logout" else "Open"
        button_style = 'Danger.TButton' if title == "Logout" else 'Action.TButton'
        
        if title == "Logout":
            ttk.Button(
                inner_frame,
                text=button_text,
                style=button_style,
                command=lambda: self.confirm_logout(command)
            ).pack(pady=(0, 0))
        else:
            ttk.Button(
                inner_frame,
                text=button_text,
                style=button_style,
                command=command
            ).pack(pady=(0, 0))

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
            self.is_admin = users[email].get("is_admin", False)  # Check if user is admin
            if self.is_admin:
                self.show_admin_dashboard()
            else:
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
        
        # Update route cards with modern styling
        for route_id, route_info in ROUTES.items():
            route_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
            route_card.pack(pady=10, fill=tk.X)
            
            # Add inner padding
            inner_card = ttk.Frame(route_card)
            inner_card.pack(padx=20, pady=20, fill=tk.X)
            
            # Route header with updated colors
            ttk.Label(
                inner_card,
                text=f"Route {route_id}",
                font=("Helvetica", 14, "bold"),
                foreground='#1976D2'  # Darker blue
            ).pack(anchor="w", pady=(0, 5))
            
            ttk.Label(
                inner_card,
                text=route_info['name'],
                font=("Helvetica", 12, "bold"),
                foreground='#424242'
            ).pack(anchor="w")
            
            # Route details
            details_frame = ttk.Frame(inner_card)
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
            
            # Show route on Google Maps
            self.show_google_maps_route(route_id)
        else:
            messagebox.showerror("Error", "No seats available!")

    def show_google_maps_route(self, route_id):
        """Display the route on Google Maps in the default web browser"""
        route = ROUTES[route_id]
        
        # Extract coordinates
        start_coords = route['start_gps'].replace(' ', '')
        end_coords = route['end_gps'].replace(' ', '')
        
        # Create Google Maps URL with route
        maps_url = (
            f"https://www.google.com/maps/dir/{start_coords}/{end_coords}"
            "?travelmode=driving"
        )
        
        # Open in default web browser
        webbrowser.open(maps_url)
        
        # Show success message
        messagebox.showinfo(
            "Route Map",
            "The route has been opened in your web browser using Google Maps."
        )
        
        self.show_user_dashboard()

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
            text="Marinduque Municipality Map",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Create a map centered on Marinduque
        m = folium.Map(
            location=[13.4013, 121.9694],  # Center of Marinduque
            zoom_start=11
        )
        
        # Define municipality locations with proper names and coordinates
        municipalities = {
            "Boac": {"coords": [13.4488, 121.8386], "color": "red"},        # Provincial Capital
            "Mogpog": {"coords": [13.4819, 121.8637], "color": "blue"},
            "Santa Cruz": {"coords": [13.4280, 122.0094], "color": "green"},
            "Torrijos": {"coords": [13.3127, 122.0871], "color": "purple"},
            "Buenavista": {"coords": [13.2574, 121.9226], "color": "orange"},
            "Gasan": {"coords": [13.3197, 121.8685], "color": "darkblue"}
        }
        
        # Add markers for each municipality
        for name, data in municipalities.items():
            # Add municipality marker
            folium.Marker(
                data["coords"],
                popup=f"{name} Municipality",
                tooltip=name,
                icon=folium.Icon(color=data["color"], icon='info-sign')
            ).add_to(m)
        
        # Draw routes between municipalities
        for route_id, route in ROUTES.items():
            # Parse start and end coordinates
            start_coords = [float(x.strip()) for x in route['start_gps'].split(',')]
            end_coords = [float(x.strip()) for x in route['end_gps'].split(',')]
            
            # Draw line between points
            folium.PolyLine(
                locations=[start_coords, end_coords],
                weight=3,
                color='red',
                opacity=0.6,
                popup=f"Route {route_id}: {route['name']}"
            ).add_to(m)
        
        # Save map to HTML file
        map_file = "marinduque_municipalities.html"
        m.save(map_file)
        
        # Create info frame
        info_frame = ttk.Frame(map_frame, style='Card.TFrame')
        info_frame.pack(fill=tk.X, padx=40, pady=20)
        
        # Add legend information
        ttk.Label(
            info_frame,
            text="Municipality Information",
            font=("Helvetica", 14, "bold"),
            foreground='#2196F3'
        ).pack(pady=(10, 5))
        
        ttk.Label(
            info_frame,
            text="Click on markers to see municipality names\nRed lines show transportation routes",
            font=("Helvetica", 11),
            foreground='#616161'
        ).pack(pady=(0, 10))
        
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

    def confirm_logout(self, logout_command):
        """Show confirmation dialog before logging out"""
        if messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?"):
            logout_command()

    def show_admin_dashboard(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create modern dashboard layout
        dashboard_frame = ttk.Frame(self.main_frame)
        dashboard_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Welcome section with admin info
        welcome_frame = ttk.Frame(dashboard_frame, style='Card.TFrame')
        welcome_frame.pack(fill=tk.X, padx=20, pady=10, ipady=15)
        
        ttk.Label(
            welcome_frame,
            text="Admin Dashboard",
            font=("Helvetica", 20, "bold"),
            foreground='#2196F3'
        ).pack(pady=(10, 5))
        
        ttk.Label(
            welcome_frame,
            text="Manage routes and seats",
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
            "Manage Seats",
            "Update available seats for routes",
            self.show_seat_management
        )
        
        self.create_dashboard_card(
            grid_frame, 0, 1,
            "View Routes",
            "Browse all transportation routes",
            self.show_routes
        )
        
        self.create_dashboard_card(
            grid_frame, 1, 0,
            "View All Bookings",
            "Check all user bookings",
            self.show_all_bookings
        )
        
        self.create_dashboard_card(
            grid_frame, 1, 1,
            "Logout",
            "Sign out of admin account",
            self.logout
        )

    def show_seat_management(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create container
        seats_frame = ttk.Frame(self.main_frame)
        seats_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            seats_frame,
            text="Manage Available Seats",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(seats_frame)
        scrollbar = ttk.Scrollbar(seats_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=(40, 0))
        
        # Create entry widgets for each route
        entries = {}
        for route_id, route_info in ROUTES.items():
            route_card = ttk.Frame(scrollable_frame, style='Card.TFrame')
            route_card.pack(pady=10, fill=tk.X, padx=20)
            
            # Route info
            ttk.Label(
                route_card,
                text=f"Route {route_id}: {route_info['name']}",
                font=("Helvetica", 14, "bold"),
                foreground='#1976D2'
            ).pack(pady=10, padx=20)
            
            # Seats entry
            seats_frame = ttk.Frame(route_card)
            seats_frame.pack(pady=(0, 10), padx=20)
            
            ttk.Label(
                seats_frame,
                text="Available Seats:",
                font=("Helvetica", 12)
            ).pack(side=tk.LEFT, padx=(0, 10))
            
            seats_entry = ttk.Entry(seats_frame, width=10)
            seats_entry.insert(0, str(route_info['seats']))
            seats_entry.pack(side=tk.LEFT)
            
            entries[route_id] = seats_entry
        
        # Update button
        def update_seats():
            try:
                for route_id, entry in entries.items():
                    new_seats = int(entry.get())
                    if new_seats < 0:
                        raise ValueError
                    ROUTES[route_id]['seats'] = new_seats
                messagebox.showinfo("Success", "Seats updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers for seats!")
        
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=20)
        
        ttk.Button(
            button_frame,
            text="Update Seats",
            style='Action.TButton',
            command=update_seats
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=lambda: self.show_admin_dashboard()
        ).pack(side=tk.LEFT, padx=10)

    def show_all_bookings(self):
        # Clear previous frames
        for widget in self.main_frame.winfo_children()[1:]:
            widget.destroy()
        
        # Create bookings container
        bookings_frame = ttk.Frame(self.main_frame)
        bookings_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Header
        ttk.Label(
            bookings_frame,
            text="All Bookings",
            font=("Helvetica", 24, "bold"),
            foreground='#2196F3'
        ).pack(pady=(0, 20))
        
        # Create scrollable frame
        canvas = tk.Canvas(bookings_frame)
        scrollbar = ttk.Scrollbar(bookings_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True, padx=(40, 0))
        
        # Show all bookings from all users
        has_bookings = False
        for email, user_info in users.items():
            if not user_info.get('is_admin', False) and user_info['bookings']:
                has_bookings = True
                user_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
                user_frame.pack(pady=10, fill=tk.X, padx=20)
                
                ttk.Label(
                    user_frame,
                    text=f"User: {user_info['name']} ({email})",
                    font=("Helvetica", 14, "bold"),
                    foreground='#1976D2'
                ).pack(pady=10, padx=20)
                
                for booking in user_info['bookings']:
                    booking_frame = ttk.Frame(user_frame)
                    booking_frame.pack(pady=5, padx=20, fill=tk.X)
                    
                    ttk.Label(
                        booking_frame,
                        text=f"Route: {booking['route_name']}",
                        font=("Helvetica", 12)
                    ).pack(anchor="w")
                    
                    schedule_time = ROUTES[booking['route_id']]['schedule']
                    ttk.Label(
                        booking_frame,
                        text=f"Date: {booking['date']} at {schedule_time}",
                        font=("Helvetica", 12)
                    ).pack(anchor="w")
        
        if not has_bookings:
            empty_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
            empty_frame.pack(pady=20, ipady=30, fill=tk.X)
            
            ttk.Label(
                empty_frame,
                text="No bookings found",
                font=("Helvetica", 14),
                foreground='#757575'
            ).pack()
        
        # Back button
        ttk.Button(
            bookings_frame,
            text="Back to Dashboard",
            style='Action.TButton',
            command=self.show_admin_dashboard
        ).pack(pady=30)

# Update the main function to use the GUI
def main():
    root = ttk.Window()
    app = TransConnectApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
