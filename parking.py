import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import time

# Create or connect to SQLite database
conn = sqlite3.connect("smart_parking.db")
cursor = conn.cursor()

# Create table for parking slots
cursor.execute("""
CREATE TABLE IF NOT EXISTS parking_slots (
    slot_id INTEGER PRIMARY KEY,
    status TEXT CHECK( status IN ('occupied', 'free') ) NOT NULL,
    booked_time TIMESTAMP,
    parked_for INTEGER -- duration in minutes
)
""")
conn.commit()

# Sample parking lot graph (using dictionary for simplicity)
parking_slots = {slot: {"status": "free", "booked_time": None, "parked_for": None, "car": None} for slot in range(1, 8)}

def update_parking_slots():
    cursor.execute("SELECT slot_id, status FROM parking_slots")
    slots = cursor.fetchall()
    for slot, status in slots:
        color = "green" if status == "free" else "red"
        canvas.itemconfig(slot_shapes[slot], fill=color)

def book_parking_slot(slot_id, parking_time):
    if parking_slots[slot_id]["status"] == "free":
        parking_slots[slot_id]["status"] = "pending"
        parking_slots[slot_id]["booked_time"] = time.time()
        parking_slots[slot_id]["parked_for"] = parking_time
        canvas.itemconfig(slot_shapes[slot_id], fill="yellow")
        open_payment_window(slot_id, parking_time)
    else:
        messagebox.showerror("Slot Unavailable", "The selected slot is already occupied.")

def open_payment_window(slot_id, parking_time):
    payment_window = tk.Toplevel(root)
    payment_window.title("Payment")
    payment_window.geometry("300x200")
    
    tk.Label(payment_window, text=f"Total Fee: ${parking_time * 2}", font=("Arial", 12)).pack(pady=10)
    
    pay_button = tk.Button(payment_window, text="Pay Now", font=("Arial", 12), command=lambda: complete_payment(slot_id, payment_window))
    pay_button.pack(pady=20)

def complete_payment(slot_id, payment_window):
    payment_window.destroy()
    parking_slots[slot_id]["status"] = "occupied"
    cursor.execute("UPDATE parking_slots SET status='occupied' WHERE slot_id=?", (slot_id,))
    conn.commit()
    canvas.itemconfig(slot_shapes[slot_id], fill="red")
    
    car_shape = canvas.create_rectangle(slot_positions[slot_id][0] + 10, slot_positions[slot_id][1] + 30, slot_positions[slot_id][0] + 50, slot_positions[slot_id][1] + 80, fill="blue", outline="black")
    parking_slots[slot_id]["car"] = car_shape
    
    messagebox.showinfo("Payment Successful", f"Payment completed. Your car is parked in slot {slot_id}.")

def reset_slots():
    cursor.execute("UPDATE parking_slots SET status='free'")
    conn.commit()
    for slot in parking_slots:
        parking_slots[slot]["status"] = "free"
        parking_slots[slot]["car"] = None
        canvas.itemconfig(slot_shapes[slot], fill="green")
    messagebox.showinfo("Reset", "All parking slots have been reset to free.")

def on_slot_click(event, slot_id):
    if parking_slots[slot_id]["status"] == "free":
        try:
            parking_time = int(parking_time_var.get())
            book_parking_slot(slot_id, parking_time)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid parking duration.")
    else:
        messagebox.showerror("Slot Occupied", f"Slot {slot_id} is already occupied!")

root = tk.Tk()
root.title("Smart Parking System")
root.geometry("800x600")

tk.Label(root, text="Smart Parking System", font=("Arial", 18, "bold")).pack(pady=20)

tk.Label(root, text="Enter Parking Duration (Minutes):", font=("Arial", 12)).pack(pady=10)
parking_time_var = tk.Entry(root, font=("Arial", 12))
parking_time_var.pack(pady=5)

reset_button = tk.Button(root, text="Reset Parking Slots", font=("Arial", 12), command=reset_slots)
reset_button.pack(pady=10)

canvas = tk.Canvas(root, width=700, height=300, bg="lightgray")
canvas.pack(pady=20)

slot_positions = {1: (50, 50), 2: (150, 50), 3: (250, 50), 4: (350, 50),
                  5: (50, 150), 6: (150, 150), 7: (250, 150)}

slot_shapes = {}
for slot, (x, y) in slot_positions.items():
    rect = canvas.create_rectangle(x, y, x + 60, y + 100, fill="green", outline="black")
    canvas.create_text(x + 30, y + 50, text=str(slot), font=("Arial", 12, "bold"))
    slot_shapes[slot] = rect
    canvas.tag_bind(rect, "<Button-1>", lambda event, slot_id=slot: on_slot_click(event, slot_id))

update_parking_slots()
root.mainloop()