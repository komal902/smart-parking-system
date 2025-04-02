Smart Parking System
Project Overview
A modern interactive parking management system built with Python and Tkinter, featuring real-time slot booking, payment processing, and an intuitive visual interface.

Key Features
Real-Time Slot Booking – Users can select and book available slots dynamically.

Visual Slot Representation – Interactive color-coded parking slots (Green = Free, Red = Occupied).

Payment Integration – Users can securely pay for their parking duration.

Automated Slot Reset – System resets after payment completion or booking expiration.

Intelligent UI – Clickable slots, dropdowns for available slots, and instant feedback messages.

Technologies Used
Python – Core logic and backend processing

Tkinter – Interactive GUI for real-time slot selection and updates

SQLite – Storing parking slot details and bookings

Time Module – Handling parking durations

How It Works
Select a parking slot (available slots are shown in green).

Enter your parking duration (in minutes).

Confirm and process payment.

The slot turns red, indicating it is booked.

Once time expires, the slot resets to free.

Installation & Setup
bash
Copy
Edit
# Clone the repository
git clone https://github.com/komal902/smart-parking.git

# Navigate to the project folder
cd smart-parking

# Install dependencies
pip install -r requirements.txt

# Run the system
python parking.py
User Controls
Click on slots – To book

Dropdown menu – Select slot manually

Payment Pop-up – Complete transaction

Reset Button – Free all slots instantly

Future Enhancements
Mobile App Integration

QR Code-Based Slot Booking

Automated Slot Sensors

Dynamic Pricing Models

Contributing
Want to improve this project? Fork, enhance, and submit a pull request.

License
This project is licensed under the MIT License.

Developed with Python and Tkinter
