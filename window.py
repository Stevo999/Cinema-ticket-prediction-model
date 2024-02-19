import tkinter as tk
from tkinter import messagebox
import joblib
import pandas as pd

class CinemaTicketApp:
    def __init__(self, master):
        self.master = master
        master.title("Cinema Ticket Prediction")

        self.label_date = tk.Label(master, text="Date (YYYY-MM-DD):", font=("Helvetica", 12))
        self.label_date.grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)

        self.entry_date = tk.Entry(master, font=("Helvetica", 12), width=20)
        self.entry_date.grid(row=0, column=1, padx=10, pady=5)

        # Add entry fields for other features
        labels = [
            ("Total Sales:", 1),
            ("Tickets Out:", 2),
            ("Show Time:", 3),
            ("Occupancy Percentage:", 4),
            ("Ticket Price:", 5),
            ("Ticket Use:", 6),
            ("Capacity:", 7)
        ]

        for label_text, row in labels:
            label = tk.Label(master, text=label_text, font=("Helvetica", 12))
            label.grid(row=row, column=0, sticky=tk.E, padx=10, pady=5)

        self.entries = {}

        for label_text, row in labels:
            entry = tk.Entry(master, font=("Helvetica", 12), width=20)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        self.predict_button = tk.Button(master, text="Predict", font=("Helvetica", 12, "bold"), command=self.predict_ticket_sales)
        self.predict_button.grid(row=8, columnspan=2, padx=10, pady=5)

        # Recommendation Section
        self.recommendation_label = tk.Label(master, text="Results:", font=("Helvetica", 12, "bold"))
        self.recommendation_label.grid(row=9, column=0, columnspan=2, pady=(20, 5))

        self.recommendation_text = tk.Text(master, height=5, font=("Helvetica", 12))
        self.recommendation_text.grid(row=10, column=0, columnspan=2, padx=10)

        # Load the trained model
        self.model = self.load_model()

    def load_model(self):
        # Load the saved model
        model = joblib.load('cinema_ticket_model.pkl')
        return model

    def predict_ticket_sales(self):
        date = self.entry_date.get()

        if date == '':
            messagebox.showerror("Error", "Please enter a date.")
            return

        try:
            # Feature engineering - extract month and quarter from date
            month = pd.to_datetime(date).month
            quarter = (pd.to_datetime(date).month - 1) // 3 + 1

            # Collect other features from GUI input fields
            features = {}
            for label_text in self.entries:
                features[label_text] = float(self.entries[label_text].get())

            day = pd.to_datetime(date).day  # Extract day from date

            # Make prediction using all features
            # Adjust this based on your model's input format
            prediction = self.model.predict([list(features.values()) + [month, quarter, day]])  

            # Display the prediction result
            prediction_text = f"Predicted number of tickets sold: {prediction}"

            # Provide comments based on the prediction result
            if prediction > 100:
                prediction_comment = "High predicted ticket sales. Expect a busy day at the cinema."
            elif prediction > 50:
                prediction_comment = "Moderate predicted ticket sales. A steady day at the cinema."
            else:
                prediction_comment = "Low predicted ticket sales. It might be a slow day at the cinema."

            # Update the recommendation section with the prediction and comment
            self.recommendation_text.delete(1.0, tk.END)  # Clear previous recommendation
            self.recommendation_text.insert(tk.END, f"{prediction_text}\n{prediction_comment}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


root = tk.Tk()
app = CinemaTicketApp(root)
root.mainloop()
