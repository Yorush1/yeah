import json
import os

#file paths
USERS_FILE = "users.json"
BOOKINGS_FILE = "bookings.json"
ROOMS_FILE = "rooms.json"

# Initialize files if they don't exist
def initialize_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    if not os.path.exists(BOOKINGS_FILE):
        with open(BOOKINGS_FILE, "w") as f:
            json.dump([], f)
    if not os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, "w") as f:
            json.dump({
                "Suite": {"price": 300, "available": 5},
                "Deluxe": {"price": 200, "available": 10},
                "Standard": {"price": 100, "available": 15}
            }, f)

# Load data from files
def load_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Save data to files
def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

#sign up
def sign_up():
    users = load_data(USERS_FILE)
    username = input("Enter username: ")
    if username in users:
        print("Username already exists!")
        return
    password = input("Enter password: ")
    users[username] = {"password": password}
    save_data(USERS_FILE, users)
    print("Sign-up successful!")

# user log in
def login():
    users = load_data(USERS_FILE)
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username in users and users[username]["password"] == password:
        print(f"Welcome, {username}!")
        return username
    else:
        print("Invalid username or password!")
        return None

#displays available rooms
def display_rooms():
    rooms = load_data(ROOMS_FILE)
    print("\nAvailable Rooms:")
    for room_type, details in rooms.items():
        print(f"{room_type}: ${details['price']} (Available: {details['available']})")

#room booking
def book_room(username):
    rooms = load_data(ROOMS_FILE)
    bookings = load_data(BOOKINGS_FILE)

    display_rooms()
    room_type = input("Enter room type to book: ")
    if room_type not in rooms:
        print("Invalid room type!")
        return

    if rooms[room_type]["available"] <= 0:
        print("No rooms available!")
        return

    rooms[room_type]["available"] -= 1
    save_data(ROOMS_FILE, rooms)

    booking = {
        "username": username,
        "room_type": room_type,
        "price": rooms[room_type]["price"]
    }
    bookings.append(booking)
    save_data(BOOKINGS_FILE, bookings)
    print(f"Room {room_type} booked successfully!")

#main menu
def main():
    initialize_files()
    while True:
        print("\n--- Hotel Management System ---")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            sign_up()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("\n--- User Menu ---")
                    print("1. View Available Rooms")
                    print("2. Book a Room")
                    print("3. Logout")
                    user_choice = input("Enter your choice: ")
                    if user_choice == "1":
                        display_rooms()
                    elif user_choice == "2":
                        book_room(username)
                    elif user_choice == "3":
                        break
                    else:
                        print("Invalid choice!")
        elif choice == "3":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()