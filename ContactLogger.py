import tkinter as tk
import csv
import requests
import datetime as dt
from tkhtmlview import HTMLLabel
import webbrowser
import os
import pytz  # Import pytz module for timezone conversion
from qsl_design_app import QSLDesignApp
from tkinter import filedialog
import tkinter.simpledialog
from tkinter import filedialog, simpledialog
class HamRadioLogger:
    def __init__(self, root):
        self.root = root
        self.root.title("Ham Radio Logger")
        self.dark_mode = False  # Flag to track current mode
        self.root.configure(bg="#333333")

        # Create frames for left and right columns
        self.left_frame = tk.Frame(root, bg="#333333")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.middle_frame = tk.Frame(root, bg="#333333")
        self.middle_frame.grid(row=0, column=1, padx=10, pady=10, rowspan=10)

        self.right_frame = tk.Frame(root, bg="#333333")
        self.right_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=10)

        # Left column widgets
        # Labels
        labels = [ "Callsign:", "Name:", "Frequency (MHz):", "Date & Time UTC:", "Location:", "Signal In / Out:", "Power In / Out:"]
        for i, label_text in enumerate(labels):
            tk.Label(self.left_frame, text=label_text, bg="#333333", fg="white", font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=5, sticky="w")
            

        # Entry fields
        
        self.call_sign_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.call_sign_entry.grid(row=0, column=1, padx=5, pady=5)
        self.name_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, padx=5, pady=5)
        self.frequency_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.frequency_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.date_entry.grid(row=3, column=1, padx=5, pady=5)
        self.location_entry = tk.Entry(self.left_frame, font=("Arial", 12))
        self.location_entry.grid(row=4, column=1, padx=5, pady=5)

        # Entry fields for signal reports
        self.signal_in_entry = tk.Entry(self.left_frame, font=("Arial", 10), width=10)
        self.signal_in_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.signal_out_entry = tk.Entry(self.left_frame, font=("Arial", 10), width=10)
        self.signal_out_entry.grid(row=5, column=1, padx=5, pady=5, sticky="e")

        # Entry fields for power
        self.power_in_entry = tk.Entry(self.left_frame, font=("Arial", 10), width=10)
        self.power_in_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        self.power_out_entry = tk.Entry(self.left_frame, font=("Arial", 10), width=10)
        self.power_out_entry.grid(row=6, column=1, padx=5, pady=5, sticky="e")


        

        # Buttons
        buttons = ["Check Call Sign", "QRZ Lookup", "Get Time", "Submit" ]
        commands = [self.check_call_sign, self.qrz_lookup, self.get_time, self.log_contact]
        for i, (button_text, command) in enumerate(zip(buttons, commands)):
            button = tk.Button(self.left_frame, text=button_text, command=command, font=("Arial", 12))
            button.grid(row=i+7, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        
        self.qsl_design_button = tk.Button(self.right_frame, text="Open QSL Designer", command=self.open_qsl_designer)
        self.qsl_design_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        #self.qsl_design_button = tk.Button(self.right_frame, text="add web browser here")
        #self.qsl_design_button.grid(row=0, column=2, padx=5, pady=5)
        


        # Toggle switch button
        self.toggle_button = tk.Button(self.right_frame, text="Dark/Light", command=self.toggle_mode, font=("Arial", 12))
        self.toggle_button.grid(row=0, column=3, padx=5, pady=5, sticky="e")

        # Right column widgets
        # HTML content
        html_content = """
        <center>
        <a href="https://www.hamqsl.com/solar.html" title="Click to add Solar-Terrestrial Data to your website!">
        <img src="https://www.hamqsl.com/solarn0nbh.php">
        </a>
        </center>
        """
        self.html_label = HTMLLabel(self.middle_frame, html=html_content, width=22, height=41)
        self.html_label.grid(row=3, column=0, padx=5, pady=5)

        # Canvas for image display
        self.canvas = tk.Canvas(self.right_frame, width=600, height=624, bg="black", highlightbackground="#cccccc")
        self.canvas.grid(row=1, column=0, padx=5, pady=5, columnspan=4)

        # Button for loading CSV file
        #self.load_csv_button = tk.Button(self.left_frame, text="Load CSV", command=self.load_csv)
        #self.load_csv_button.grid(row=12, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Entry field for call sign filter
        #self.filter_entry = tk.Entry(self.right_frame, font=("Arial", 12))
        #self.filter_entry.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Configure column width based on HTML content's width
        self.middle_frame.grid_columnconfigure(0, weight=1)

        # spacer label
        self.spacer_label = tk.Label(self.middle_frame, text='\n ')
        self.spacer_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Button to apply the filter
        self.filter_button = tk.Button(self.middle_frame, text="Filter by Callsign", command=self.apply_filter, font=("Arial", 12))
        self.filter_button.grid(row=1, column=0, padx=5, pady=5, sticky="nwe")

        # spacer label
        self.spacer_label = tk.Label(self.middle_frame, text='\n ')
        self.spacer_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Dropdown menu label
        self.dropdown_label = tk.Label(self.right_frame, text='Filter by:  ')
        self.dropdown_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        
        # Dropdown menu for filtering
        self.filter_var = tk.StringVar()
        self.filter_var.set("All")
        self.filter_menu = tk.OptionMenu(self.right_frame, self.filter_var, "All", "Day", "Week", "Month", "Year", command=self.apply_filter)
        self.filter_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Button to clear input fields and refresh canvas
        self.clear_button = tk.Button(self.left_frame, text="Refresh", command=self.clear_all, font=("Arial", 12))
        self.clear_button.grid(row=13, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Add a new button for moving entries
        self.move_entry_button = tk.Button(self.middle_frame, text="Remove Entry", command=self.move_entry, font=("Arial", 12))
        self.move_entry_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="we")

        # Create a frame to hold the canvas and scrollbars
        self.canvas_frame = tk.Frame(self.right_frame, bg="#333333")
        self.canvas_frame.grid(row=1, column=0, padx=5, pady=5, columnspan=4, sticky="nsew")

        # Canvas for image display
        self.canvas = tk.Canvas(self.canvas_frame, bg="black", highlightbackground="#cccccc")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Vertical scrollbar
        self.scrollbar_y = tk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar_y.set)

        # Horizontal scrollbar
        self.scrollbar_x = tk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")
        self.canvas.config(xscrollcommand=self.scrollbar_x.set)

        # Configure row and column weights for the canvas frame
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # After configuring the canvas, set the horizontal scrollbar to the leftmost position
        self.canvas.xview_moveto(100)

        try:
            self.load_csv()
        except:
            print('failed to load csv')

    def clear_all(self):
        # Clear all input fields
        self.call_sign_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.frequency_entry.delete(0, tk.END)
        self.date_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.signal_in_entry.delete(0, tk.END)
        self.signal_out_entry.delete(0, tk.END)
        #self.filter_var = tk.StringVar()
        self.filter_var.set("All")  # Set the default value to "All"

        # Refresh the canvas
        self.load_csv()

    # Method to handle the removal of specific entries
    # Method to handle the removal of specific entries
    def move_entry(self):
        try:
            # Prompt the user for the entry number
            entry_number = tkinter.simpledialog.askinteger("Move Entry", "Enter the entry number to move:")
            if entry_number is not None:
                # Check if the entry number is within range
                if entry_number > 0:
                    with open("ham_radio_logs.csv", "r") as file:
                        reader = csv.reader(file)
                        rows = list(reader)
                        # Check if the entry number is within the range of available entries
                        if 0 < entry_number <= len(rows):
                            # Remove the selected entry
                            del rows[entry_number - 1]  # Adjust for 0-based indexing
                            # Rewrite the CSV file with updated data
                            with open("ham_radio_logs.csv", "w", newline="") as new_file:
                                writer = csv.writer(new_file)
                                writer.writerows(rows)
                            # Reload the CSV data
                            self.load_csv()
                        else:
                            self.show_message("Invalid entry number.")
                else:
                    self.show_message("Entry number must be greater than zero.")
        except Exception as e:
            self.show_error(f"Error occurred: {str(e)}")
    
    def load_csv(self):
        # Open file dialog to select CSV file
        #file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        file_path = "ham_radio_logs.csv"
        if file_path:
            # Clear canvas before loading new data
            self.canvas.delete("all")
            # Read CSV file and display its contents in the canvas
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                row_index = 0
                y_offset = 20  # Adjust as needed
                x_offset = 20  # Adjust as needed
                for row_index, row in enumerate(reader):
                    call_sign_filter = self.call_sign_entry.get().upper()
                    if not call_sign_filter or (row and row[1].strip().upper() == call_sign_filter):
                        # Display the entry number
                        entry_number = row_index + 1  # Entry numbers start from 1
                        self.canvas.create_text(x_offset, y_offset + row_index * 20, text=f"{entry_number}. ", anchor="e")

                        # Display the row content
                        for col_index, value in enumerate(row):
                            # Adjust the starting position for the first column
                            if col_index == 0:
                                x_position = col_index * 100 + x_offset + 20
                            else:
                                x_position = col_index * 100 + 20
                            # Adjust the starting position for the first row
                            y_position = row_index * 20 + y_offset

                            # Update the canvas scroll region
                            self.canvas.config(scrollregion=self.canvas.bbox("all"))
                            
                            # Create text object
                            self.canvas.create_text(x_position, y_position, text=value)
                # Update the canvas scroll region based on the bounding box of all items
                self.canvas.update_idletasks()  # Update the canvas to get correct bbox
                bbox = self.canvas.bbox("all")
                self.canvas.config(scrollregion=bbox)  # Set scroll region to the bounding box

                # Ensure that the canvas view is moved to the leftmost position
                self.canvas.xview_moveto(0)
                self.canvas.yview_moveto(0)  # Optionally, move the vertical scrollbar to the top


    def remove_selected_entry(self):
        try:
            # Get the entry number to be removed
            selected_entry = int(self.remove_entry_var.get())

            # Remove the entry from the CSV file or data structure
            # You can implement this part based on your specific data storage mechanism

            # After removing the entry, refresh the canvas
            self.load_csv()
        except ValueError:
            # Handle the case where the user enters a non-numeric value
            self.show_error("Please enter a valid entry number.")


    def apply_filter(self, *args):
        # Apply filter to the canvas based on the selected option
        selected_filter = self.filter_var.get()
        print("Selected filter:", selected_filter)

        # Define filter functions
        filter_functions = {
            "Day": self.filter_by_day,
            "Week": self.filter_by_week,
            "Month": self.filter_by_month,
            "Year": self.filter_by_year,
            "All": self.filter_all
        }

        # Call the selected filter function
        filter_function = filter_functions.get(selected_filter)
        if filter_function:
            filter_function()

    # Implement filter functions
    def filter_by_day(self):
        # Get the current date
        current_date = dt.datetime.now().date()

        # Clear canvas before loading new data
        self.canvas.delete("all")

        # Read CSV file and display its contents in the canvas
        with open("ham_radio_logs.csv", "r") as file:
            reader = csv.reader(file)
            row_index = 0
            y_offset = 20  # Adjust as needed
            x_offset = 20  # Adjust as needed
            call_sign_filter = self.call_sign_entry.get().upper()  # Get the callsign filter value
            for row in reader:
                if row:
                    # Parse date from the row and strip the time portion
                    date_str = row[3].split()[0].strip()  # Strip leading and trailing whitespaces
                    try:
                        date = dt.datetime.strptime(date_str, "%d/%m/%Y").date()
                    except ValueError:
                        continue  # Skip invalid dates
                    # Check if the date matches the current date and callsign matches the filter
                    if date == current_date and (not call_sign_filter or row[1].strip().upper() == call_sign_filter):
                        for col_index, value in enumerate(row):
                            # Adjust the starting position for the first column
                            if col_index == 0:
                                x_position = col_index * 100 + x_offset
                            else:
                                x_position = col_index * 100
                            # Adjust the starting position for the first row
                            y_position = row_index * 20 + y_offset

                            # Create text object
                            self.canvas.create_text(x_position, y_position, text=value)
                        row_index += 1


    def filter_by_week(self):
        # Get the current week number
        current_week = dt.datetime.now().isocalendar()[1]

        # Clear canvas before loading new data
        self.canvas.delete("all")

        # Read CSV file and display its contents in the canvas
        with open("ham_radio_logs.csv", "r") as file:
            reader = csv.reader(file)
            row_index = 0
            y_offset = 20  # Adjust as needed
            x_offset = 20  # Adjust as needed
            call_sign_filter = self.call_sign_entry.get().upper()  # Get the callsign filter value
            for row in reader:
                if row:
                    # Parse date from the row and strip the time portion
                    date_str = row[3].split()[0].strip()  # Strip leading and trailing whitespaces
                    try:
                        date = dt.datetime.strptime(date_str, "%d/%m/%Y")
                        # Check if the week number matches the current week number and callsign matches the filter
                        if date.isocalendar()[1] == current_week and (not call_sign_filter or row[1].strip().upper() == call_sign_filter):
                            for col_index, value in enumerate(row):
                                # Adjust the starting position for the first column
                                if col_index == 0:
                                    x_position = col_index * 100 + x_offset
                                else:
                                    x_position = col_index * 100
                                # Adjust the starting position for the first row
                                y_position = row_index * 20 + y_offset

                                # Create text object
                                self.canvas.create_text(x_position, y_position, text=value)
                            row_index += 1
                    except ValueError:
                        continue  # Skip invalid dates

    def filter_by_month(self):
        # Get the current month
        current_month = dt.datetime.now().month

        # Clear canvas before loading new data
        self.canvas.delete("all")

        # Read CSV file and display its contents in the canvas
        with open("ham_radio_logs.csv", "r") as file:
            reader = csv.reader(file)
            row_index = 0
            y_offset = 20  # Adjust as needed
            x_offset = 20  # Adjust as needed
            call_sign_filter = self.call_sign_entry.get().upper()  # Get the callsign filter value
            for row in reader:
                if row:
                    # Parse date from the row and strip the time portion
                    date_str = row[3].split()[0].strip()  # Strip leading and trailing whitespaces
                    try:
                        date = dt.datetime.strptime(date_str, "%d/%m/%Y")
                        # Check if the month matches the current month and callsign matches the filter
                        if date.month == current_month and (not call_sign_filter or row[1].strip().upper() == call_sign_filter):
                            for col_index, value in enumerate(row):
                                # Adjust the starting position for the first column
                                if col_index == 0:
                                    x_position = col_index * 100 + x_offset
                                else:
                                    x_position = col_index * 100
                                # Adjust the starting position for the first row
                                y_position = row_index * 20 + y_offset

                                # Create text object
                                self.canvas.create_text(x_position, y_position, text=value)
                            row_index += 1
                    except ValueError:
                        continue  # Skip invalid dates

            
    def filter_by_year(self):
        # Get the current year
        current_year = dt.datetime.now().year

        # Clear canvas before loading new data
        self.canvas.delete("all")

        # Read CSV file and display its contents in the canvas
        with open("ham_radio_logs.csv", "r") as file:
            reader = csv.reader(file)
            row_index = 0
            y_offset = 20  # Adjust as needed
            x_offset = 20  # Adjust as needed
            call_sign_filter = self.call_sign_entry.get().upper()  # Get the callsign filter value
            for row in reader:
                if row:
                    # Parse date from the row and strip the time portion
                    date_str = row[3].split()[0].strip()  # Strip leading and trailing whitespaces
                    try:
                        date = dt.datetime.strptime(date_str, "%d/%m/%Y")
                        # Check if the year matches the current year and callsign matches the filter
                        if date.year == current_year and (not call_sign_filter or row[1].strip().upper() == call_sign_filter):
                            for col_index, value in enumerate(row):
                                # Adjust the starting position for the first column
                                if col_index == 0:
                                    x_position = col_index * 100 + x_offset
                                else:
                                    x_position = col_index * 100
                                # Adjust the starting position for the first row
                                y_position = row_index * 20 + y_offset

                                # Create text object
                                self.canvas.create_text(x_position, y_position, text=value)
                            row_index += 1
                    except ValueError:
                        continue  # Skip invalid dates


    def filter_all(self):
        # Open file dialog to select CSV file
        #file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        file_path = "ham_radio_logs.csv"
        if file_path:
            # Clear canvas before loading new data
            self.canvas.delete("all")
            # Read CSV file and display its contents in the canvas
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                row_index = 0
                y_offset = 20  # Adjust as needed
                x_offset = 20  # Adjust as needed
                for row in reader:
                    call_sign_filter = self.call_sign_entry.get().upper()
                    if not call_sign_filter or (row and row[1].strip().upper() == call_sign_filter):
                        for col_index, value in enumerate(row):
                            # Adjust the starting position for the first column
                            if col_index == 0:
                                x_position = col_index * 100 + x_offset
                            else:
                                x_position = col_index * 100
                            # Adjust the starting position for the first row
                            y_position = row_index * 20 + y_offset

                            # Create text object
                            self.canvas.create_text(x_position, y_position, text=value)
                        row_index += 1






    def open_qsl_designer(self):
        os.system("python3 qsl_design.py")


    def toggle_mode(self):
        # Toggle between light and dark mode
        if self.dark_mode:
            self.root.configure(bg="#333333")
            self.left_frame.configure(bg="#333333")
            self.middle_frame.configure(bg="#333333")
            self.toggle_button.configure(bg="#333333", fg="white")
            self.dark_mode = False
        else:
            self.root.configure(bg="white")
            self.left_frame.configure(bg="white")
            self.middle_frame.configure(bg="white")
            self.toggle_button.configure(bg="white", fg="black")
            self.dark_mode = True

    def open_qsl_designer(self):
        qsl_window = tk.Toplevel(self.root)
        qsl_window.title("QSL Card Designer")
        #qsl_window.geometry("800x600")

        qsl_app = QSLDesignApp(qsl_window)


    # Rest of the class methods...
    def log_contact(self):
        name = self.name_entry.get()
        call_sign = self.call_sign_entry.get()
        frequency = self.frequency_entry.get()
        date = self.date_entry.get()
        location = self.location_entry.get()
        signal_in = self.signal_in_entry.get()
        signal_out = self.signal_out_entry.get()
        power_in = self.power_in_entry.get()
        power_out = self.power_out_entry.get()

        # Save to CSV
        try:
            with open("ham_radio_logs.csv", mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([name, call_sign, frequency, date, location, f"{signal_in}/{signal_out}"])
                self.show_message(f"Logged: {name}, Call Sign: {call_sign}, Frequency: {frequency} MHz, Date: {date}, Location: {location}, Signal In: {signal_in}, Signal Out: {signal_out}, Power In: {power_in}, Power Out: {power_out}")
        except Exception as e:
            self.show_error(f"Error occurred while saving the log: {str(e)}")
        self.load_csv()

    # Rest of the class methods...



    def get_time(self):
        # Get current time in UTC timezone
        utc_time = dt.datetime.utcnow().replace(tzinfo=pytz.utc)

        # Convert UTC time to local time
        local_time = utc_time.astimezone(pytz.timezone('UTC'))  # Change 'UTC' to your local timezone if needed

        # Format time as string
        formatted_time = local_time.strftime("%d/%m/%Y %H:%M:%S")

        # Update date entry field with UTC time
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, formatted_time)

    def qrz_lookup(self):
        call_sign = self.call_sign_entry.get().upper()
        if not call_sign:
            self.show_error("Please enter a call sign.")
            return

        # Open QRZ website with the call sign appended
        qrz_url = f"https://www.qrz.com/db/{call_sign}"
        webbrowser.open(qrz_url)

    def check_call_sign(self):
        call_sign = self.call_sign_entry.get().upper()
        if not call_sign:
            self.show_error("Please enter a call sign.")
            return

        try:
            with open("ham_radio_logs.csv", mode="r") as file:
                reader = csv.reader(file)
                found = False
                appearances = 0
                contact_info = None  # Store contact information (name, location) for display
                dates_and_details = []  # Store dates, frequencies, and bands of appearances
                for row in reader:
                    if row and row[1].strip().upper() == call_sign:
                        found = True
                        appearances += 1
                        # Store contact information for the first appearance only
                        if not contact_info:
                            contact_info = (row[0], row[4])  # Name, location
                            signal_report = row[5]  # Signal report is at index 5
                        band = self.calculate_band(float(row[2]))
                        dates_and_details.append((row[3], row[2], band))  # Append (date, frequency, band) tuple to the list
                if found:
                    if appearances > 1:
                        message = f"{call_sign} - {contact_info[0]}, from {contact_info[1]} has appeared {appearances} times.\nPrevious Contacts:\n"
                        for date, freq, band in dates_and_details:
                            message += f"Date: {date}, Frequency: {freq} MHz ({band}), Sig Report: {signal_report}\n"
                        self.show_message(message)
                    else:
                        self.show_message(f"{call_sign} - {contact_info[0]}, from {contact_info[1]} has not appeared in the logs.")
                else:
                    self.show_message(f"{call_sign} has not appeared in the logs.")
        except Exception as e:
            # Error handling: Show error message
            self.show_error(f"Error occurred while checking call sign: {str(e)}")

    def calculate_band(self, frequency):
        # Determine band based on frequency
        frequency = float(frequency)
        if 1.8 <= frequency <= 2:
            return "160m"
        elif 3.5 <= frequency <= 4:
            return "80m"
        elif 5.06 <= frequency <= 5.45:
            return "60m"
        elif 7 <= frequency <= 7.3:
            return "40m"
        elif 10.1 <= frequency <= 10.15:
            return "30m"
        elif 14 <= frequency <= 14.35:
            return "20m"
        elif 18.068 <= frequency <= 18.168:
            return "17m"
        elif 21 <= frequency <= 21.45:
            return "15m"
        elif 24.89 <= frequency <= 24.99:
            return "12m"
        elif 28 <= frequency <= 29.7:
            return "10m"
        elif 50 <= frequency <= 54:
            return "6m"
        elif 144 <= frequency <= 148:
            return "2m"
        elif 222 <= frequency <= 225:
            return "1.25m"
        elif 420 <= frequency <= 450:
            return "70cm"
        elif 902 <= frequency <= 928:
            return "33cm"
        elif 1240 <= frequency <= 1300:
            return "23cm"
        else:
            return "Unknown band"
        
    def show_message(self, message):
        # Create a new window for displaying messages
        message_window = tk.Toplevel(self.root)
        message_window.title("Message")
        message_window.configure(bg="#333333")

        text_widget = tk.Text(message_window, wrap="word", width=67, height=10, font=("Arial", 12), bg="#333333", fg="white")
        text_widget.insert("1.0", message)
        text_widget.pack(expand=True, fill="both")

        # Create a close button
        close_button = tk.Button(message_window, text="Close", command=message_window.destroy, font=("Arial", 12))
        close_button.pack()

    def show_error(self, message):
        # Create a new window for displaying errors
        error_window = tk.Toplevel(self.root)
        error_window.title("Error")
        error_window.configure(bg="#333333")

        text_widget = tk.Text(error_window, wrap="word", width=67, height=10, font=("Arial", 12), bg="#333333", fg="white")
        text_widget.insert("1.0", message)
        text_widget.pack(expand=True, fill="both")

        # Create a close button
        close_button = tk.Button(error_window, text="Close", command=error_window.destroy, font=("Arial", 12))
        close_button.pack()


if __name__ == "__main__":
    root = tk.Tk()
    app = HamRadioLogger(root)
    #root.geometry("475x400")  # Width x Height
    root.mainloop()
