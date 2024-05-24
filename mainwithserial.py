import tkinter as tk
import numpy as np
import time
import threading
import serial.tools.list_ports  # Import serial library
from FruitBox import FruitBoxesApp


# Define a function to read from Arduino serial and update boxes
def read_and_update():
    global ids_array, weights_array, box_1, box_2, box_3, box_4
    arduino_serial_data = serial.Serial('COM7', 9600)

    while True:
        if arduino_serial_data.in_waiting > 0:
            try:
                my_data = arduino_serial_data.readline().decode().strip()
                id_start = my_data.find("Got request from: ")
                force_start = my_data.find(" Received value: ")
                end = my_data.find(".")

                new_id = int(my_data[id_start + len("Got request from: "):force_start].strip())
                new_units = int(my_data[force_start + len(" Received value: "):end].strip())
                new_weights = new_units / 1000
                print(new_id, new_weights)

                ids_array = np.append(ids_array, new_id)
                weights_array = np.append(weights_array, new_weights)

                if ids_array[-1] == 1:
                    box_1 = np.append(box_1, weights_array[-1])
                    if len(box_1) > 100:
                        box_1 = box_1[1:]
                elif ids_array[-1] == 2:
                    box_2 = np.append(box_2, weights_array[-1])
                    if len(box_2) > 100:
                        box_2 = box_2[1:]
                elif ids_array[-1] == 3:
                    box_3 = np.append(box_3, weights_array[-1])
                    if len(box_3) > 100:
                        box_3 = box_3[1:]
                elif ids_array[-1] == 4:
                    box_4 = np.append(box_4, weights_array[-1])
                    if len(box_4) > 100:
                        box_4 = box_4[1:]

                last_elements = [box_1[-1], box_2[-1], box_3[-1], box_4[-1]]
                app.update_boxes(last_elements)
                time.sleep(0.5)  # Sleep to simulate delay if necessary

            except Exception as e:
                print(f"Error processing data: {e}")


# Create arrays and initialize Tkinter app
ids_array = np.array([])
weights_array = np.array([])
box_1 = np.array([0])  # Initialize box arrays with initial value
box_2 = np.array([0])
box_3 = np.array([0])
box_4 = np.array([0])

# Set window dimensions
window_width = 1540
window_height = 860

root = tk.Tk()
app = FruitBoxesApp(root, window_width, window_height)

# Start a new thread for reading from Arduino serial and updating boxes
update_thread = threading.Thread(target=read_and_update)
update_thread.start()

root.mainloop()  # This will run the Tkinter main loop
