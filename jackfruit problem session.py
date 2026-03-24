import tkinter as tk
from tkinter import messagebox
import pandas as pd
from datetime import datetime

# File names
RESTAURANTS_FILE = "restaurants.csv"
USERS_FILE = "users.csv"
BOOKINGS_FILE = "bookings.csv"

# Fonts
DEFAULT_FONT = ("Segoe UI", 12)
TITLE_FONT = ("Segoe UI", 16, "bold")

def load_data(file_name):
    try:
        return pd.read_csv(file_name)
    except FileNotFoundError:
        return pd.DataFrame()

def save_data(df, file_name):
    df.to_csv(file_name, index=False)

class RestaurantBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurant Booking System")
        self.root.configure(bg="#f5f5f5")

        self.restaurants = load_data(RESTAURANTS_FILE)
        self.users = load_data(USERS_FILE)
        self.bookings = load_data(BOOKINGS_FILE)

        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()

        tk.Label(self.root, text="🍽 Restaurant Booking System", font=TITLE_FONT, bg="#f5f5f5").pack(pady=20)

        tk.Button(self.root, text="View Restaurants", font=DEFAULT_FONT,
                  bg="#2196F3", fg="white", width=20,
                  command=self.view_restaurants).pack(pady=10)

        tk.Button(self.root, text="Manage Bookings", font=DEFAULT_FONT,
                  bg="#4CAF50", fg="white", width=20,
                  command=self.manage_bookings).pack(pady=10)

    def view_restaurants(self):
        self.clear_frame()

        tk.Label(self.root, text="Restaurants", font=TITLE_FONT, bg="#f5f5f5").pack(pady=10)

        self.restaurant_list = tk.Listbox(self.root, width=70, height=15, font=DEFAULT_FONT)
        self.restaurant_list.pack(pady=10)

        for _, r in self.restaurants.iterrows():
            self.restaurant_list.insert(
                tk.END,
                f"{r['restaurant_id']} - {r['name']} ({r['cuisine_type']}) ⭐{r['rating']}"
            )

        tk.Button(self.root, text="Back", font=DEFAULT_FONT,
                  command=self.create_main_menu).pack(pady=10)

    def manage_bookings(self):
        self.clear_frame()

        tk.Label(self.root, text="Manage Bookings", font=TITLE_FONT, bg="#f5f5f5").pack(pady=20)

        tk.Button(self.root, text="Make Reservation", font=DEFAULT_FONT,
                  bg="#4CAF50", fg="white", width=20,
                  command=self.make_reservation).pack(pady=10)

        tk.Button(self.root, text="Cancel Reservation", font=DEFAULT_FONT,
                  bg="#f44336", fg="white", width=20,
                  command=self.cancel_reservation).pack(pady=10)

        tk.Button(self.root, text="Back", font=DEFAULT_FONT,
                  command=self.create_main_menu).pack(pady=10)

    def make_reservation(self):
        self.clear_frame()

        tk.Label(self.root, text="Make Reservation", font=TITLE_FONT, bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="User ID (e.g., U001):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        user_id = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        user_id.pack()

        tk.Label(self.root, text="Restaurant ID (e.g., R001):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        restaurant_id = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        restaurant_id.pack()

        tk.Label(self.root, text="Table ID (e.g., T1):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        table_id = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        table_id.pack()

        tk.Label(self.root, text="Date (YYYY-MM-DD):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        date = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        date.pack()

        tk.Label(self.root, text="Time (HH:MM):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        time = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        time.pack()

        tk.Label(self.root, text="Party Size:", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        party_size = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        party_size.pack()

        tk.Button(self.root, text="Confirm", font=DEFAULT_FONT,
                  bg="#4CAF50", fg="white",
                  command=lambda: self.confirm_reservation(
                      user_id.get(), restaurant_id.get(), table_id.get(),
                      date.get(), time.get(), party_size.get()
                  )).pack(pady=15)

        tk.Button(self.root, text="Back", font=DEFAULT_FONT,
                  command=self.manage_bookings).pack()

    def confirm_reservation(self, user_id, restaurant_id, table_id, date, time, party_size):
        try:
            party_size = int(party_size)

            if user_id not in self.users['user_id'].values:
                raise ValueError("Invalid User ID!")

            if restaurant_id not in self.restaurants['restaurant_id'].values:
                raise ValueError("Invalid Restaurant ID!")

            datetime.strptime(date, "%Y-%m-%d")
            datetime.strptime(time, "%H:%M")

            new_id = f"B{len(self.bookings) + 1:03d}"

            new_booking = {
                "booking_id": new_id,
                "user_id": user_id,
                "restaurant_id": restaurant_id,
                "table_id": table_id,
                "date": date,
                "time": time,
                "party_size": party_size
            }

            self.bookings = pd.concat(
                [self.bookings, pd.DataFrame([new_booking])],
                ignore_index=True
            )

            save_data(self.bookings, BOOKINGS_FILE)

            messagebox.showinfo("Success", f"Booking Confirmed! ID: {new_id}")
            self.manage_bookings()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def cancel_reservation(self):
        self.clear_frame()

        tk.Label(self.root, text="Cancel Reservation", font=TITLE_FONT, bg="#f5f5f5").pack(pady=10)

        tk.Label(self.root, text="Booking ID (e.g., B001):", font=DEFAULT_FONT, bg="#f5f5f5").pack(pady=5)
        booking_id = tk.Entry(self.root, font=DEFAULT_FONT, width=25)
        booking_id.pack()

        tk.Button(self.root, text="Cancel", font=DEFAULT_FONT,
                  bg="#f44336", fg="white",
                  command=lambda: self.confirm_cancel(booking_id.get())).pack(pady=15)

        tk.Button(self.root, text="Back", font=DEFAULT_FONT,
                  command=self.manage_bookings).pack()

    def confirm_cancel(self, booking_id):
        try:
            if booking_id not in self.bookings['booking_id'].values:
                raise ValueError("Invalid Booking ID!")

            self.bookings = self.bookings[self.bookings['booking_id'] != booking_id]
            self.bookings.reset_index(drop=True, inplace=True)

            save_data(self.bookings, BOOKINGS_FILE)

            messagebox.showinfo("Success", "Reservation Cancelled")
            self.manage_bookings()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x600")  # Bigger window
    app = RestaurantBookingSystem(root)
    root.mainloop()