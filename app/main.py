from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from pymongo import MongoClient
from datetime import datetime
import ttkbootstrap as ttk
import tkinter as tk
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def connection():
    # MongoDB connection
    client = MongoClient(f"mongodb+srv://{username_cont.get()}:{pswd_cont.get()}@cluster0.easnlpy.mongodb.net/?retryWrites=true&w=majority")
    db = client[dbname_cont.get()]
    collection = db[clntname_cont.get()]

    # Initialize empty lists for x and y data
    x_data = []
    y1_data = []
    y2_data = []

    # Function to retrieve data from MongoDB and update the graph
    def update_graph():
        # Clear previous data
        x_data.clear()
        y1_data.clear()
        y2_data.clear()

        # Query MongoDB to fetch the latest data
        data = collection.find({})

        # Process the retrieved data
        for entry in data:
            # Extract the date/time and values from each document
            date_str = entry['date']
            value1 = entry['aedes']
            value2 = entry['non_aedes']

            # Convert date string to datetime object
            date = datetime.strftime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")

            # Append data to x and y lists
            x_data.append(date)
            y1_data.append(value1)
            y2_data.append(value2)

        # Clear the previous graph
        ax1.clear()
        ax2.clear()

        # Plot the data on two separate y-axes
        ax1.plot(x_data, y1_data, color='blue')
        ax2.plot(x_data, y2_data, color='green')

        # Set labels and titles for the axes
        ax1.set_ylabel('aedes', color='blue')
        ax2.set_ylabel('non-aedes', color='green')
        ax1.set_title('AIDeM MongoDB')

        # Set the colors of the y-axis labels
        ax1.tick_params(axis='y', labelcolor='blue')
        ax2.tick_params(axis='y', labelcolor='green')

        # Move the y-axis labels to a different location
        ax1.yaxis.set_label_coords(-0.1, 0.5)
        ax2.yaxis.set_label_coords(1.1, 0.5)

        ax1.set_xticklabels([])

        # Rotate x-axis labels for better visibility
        fig.autofmt_xdate()

        # Refresh the canvas
        canvas.draw()

        # Schedule the next update after a delay
        root.after(1000, update_graph)  # Update every 1 second
    
    update_graph()

# Create the Tkinter application window
root = ttk.Window('darkly')
icon = tk.PhotoImage(file=resource_path('aidem_setup/yolo_setup/app/assets/aidem.png'))
root.iconphoto(False,icon)
root.title('AIDeM')

# Database Frame
db_frame = ttk.Labelframe(root, text='Database', bootstyle='info')
username_cont = tk.StringVar()
ttk.Label(db_frame, text="Username:").grid(column = 0, row = 0 ,sticky=tk.E, padx=5, pady=20)
username_entry = ttk.Entry(db_frame, textvariable = username_cont)
username_entry.grid(column = 1, row = 0, sticky=tk.W, padx=5, pady=5)

# password
pswd_cont = tk.StringVar()
ttk.Label(db_frame, text="Password:").grid(column = 2, row = 0,sticky=tk.E, padx=5, pady=20)
pswd_entry = ttk.Entry(db_frame, show = '*',textvariable = pswd_cont)
pswd_entry.grid(column = 3, row = 0, sticky=tk.W, padx=5, pady=5)

# database name
dbname_cont = tk.StringVar()
ttk.Label(db_frame, text="Database Name:").grid(column = 0, row = 2 ,sticky=tk.E, padx=5, pady=5)
dbname_entry = ttk.Entry(db_frame, textvariable = dbname_cont)
dbname_entry.grid(column = 1, row = 2, sticky=tk.W, padx=5, pady=5)

# collection name
clntname_cont = tk.StringVar()
ttk.Label(db_frame, text="Collection Name:").grid(column = 2, row = 2,sticky=tk.E, padx=5, pady=5)
clnt_entry = ttk.Entry(db_frame, textvariable = clntname_cont)
clnt_entry.grid(column = 3, row = 2, sticky=tk.W, padx=5, pady=5)

start_button = ttk.Button(master = db_frame, text = 'save', command = connection)
start_button.grid(column=3, row=3, padx= 5, pady=5)
db_frame.pack()

# Create a Figure and two Axes for the graph
fig = Figure(figsize=(8, 6), dpi=80)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()

# Create a canvas to display the graph
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack()

# Start the Tkinter event loop
root.mainloop()