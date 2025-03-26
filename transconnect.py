# Import required Python libraries
# time: for adding delays in the program
# typing: for adding type hints to make code more readable
import time
from typing import Dict, List

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

# Function to clear the console screen by printing multiple newlines
def clear_screen() -> None:
    print("\n" * 50)

# Function to handle new user registration
def register_user() -> None:
    clear_screen()
    print("=== TransConnect Registration ===")
    # Get user information through console input
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    # Check if user already exists in the system
    if email in users:
        print("User already exists! Please login instead.")
        return
    
    # Create new user record in the users dictionary
    users[email] = {
        "name": name,
        "email": email,
        "password": password,
        "bookings": []
    }
    print("\nRegistration successful!")
    time.sleep(2)  # Add a 2-second delay to show the success message

# Function to handle user login
def login() -> str:
    clear_screen()
    print("=== TransConnect Login ===")
    # Get login credentials
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    
    # Check if user exists in the system
    if email not in users:
        print("User not found! Please register first.")
        time.sleep(2)
        return ""
    
    # Verify password
    if users[email]["password"] != password:
        print("Incorrect password!")
        time.sleep(2)
        return ""
    
    return email  # Return email if login successful

# Function to show all available routes
def display_routes() -> None:
    print("\n=== Available Routes ===")
    # Loop through each route and display its details
    for route_id, route in ROUTES.items():
        print(f"\nRoute {route_id}:")
        print(f"From: {route['name']}")
        print(f"Start GPS: {route['start_gps']}")
        print(f"End GPS: {route['end_gps']}")
        print(f"Available Seats: {route['seats']}")
        print(f"Schedule: {route['schedule']}")

# Function to handle seat booking process
def book_seat(user_email: str) -> None:
    display_routes()
    
    try:
        # Get route choice from user
        route_choice = int(input("\nEnter route number to book (1 or 2): "))
        if route_choice not in ROUTES:
            print("Invalid route number!")
            return
        
        # Check if seats are available and process booking
        if ROUTES[route_choice]["seats"] > 0:
            ROUTES[route_choice]["seats"] -= 1  # Reduce available seats by 1
            # Create booking record
            booking = {
                "route": ROUTES[route_choice]["name"],
                "schedule": ROUTES[route_choice]["schedule"]
            }
            users[user_email]["bookings"].append(booking)  # Add booking to user's records
            print("\nBooking confirmed!")
            print(f"You have booked a seat on {booking['route']} at {booking['schedule']}")
        else:
            print("Sorry, no seats available on this route!")
    except ValueError:
        print("Please enter a valid route number!")

# Main function that runs the program
def main() -> None:
    while True:
        clear_screen()
        # Display main menu
        print("=== Welcome to TransConnect ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        # Handle user's main menu choice
        if choice == "1":
            register_user()
        elif choice == "2":
            user_email = login()
            if user_email:  # If login successful
                while True:
                    clear_screen()
                    # Display user menu
                    print(f"\nWelcome, {users[user_email]['name']}!")
                    print("\n1. View Routes")
                    print("2. Book a Seat")
                    print("3. View My Bookings")
                    print("4. Logout")
                    
                    user_choice = input("\nEnter your choice (1-4): ")
                    
                    # Handle user's menu choices
                    if user_choice == "1":
                        display_routes()
                        input("\nPress Enter to continue...")
                    elif user_choice == "2":
                        book_seat(user_email)
                        input("\nPress Enter to continue...")
                    elif user_choice == "3":
                        print("\n=== Your Bookings ===")
                        # Display all bookings for the current user
                        for booking in users[user_email]["bookings"]:
                            print(f"\nRoute: {booking['route']}")
                            print(f"Schedule: {booking['schedule']}")
                        input("\nPress Enter to continue...")
                    elif user_choice == "4":
                        break  # Return to main menu
        elif choice == "3":
            print("\nThank you for using TransConnect!")
            break  # Exit the program

# Standard Python idiom to ensure main() only runs if this file is run directly
if __name__ == "__main__":
    main()
