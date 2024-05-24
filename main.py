import tkinter as tk
import numpy as np
import time
import threading
from FruitBox import FruitBoxesApp


# Define a function to read from file and update boxes
def read_and_update():
    global ids_array, weights_array, box_1, box_2, box_3, box_4
    with open('C:/Users/sokra/rand_inputs.txt', 'r') as file:
        for line in file:
            inputs = line.split()
            new_id = float(inputs[0])
            new_units = float(inputs[1])
            new_weights = new_units / 1

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

            time.sleep(0.5)
            last_elements = [box_1[-1], box_2[-1], box_3[-1], box_4[-1]]
            app.update_boxes(last_elements)


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

# Start a new thread for reading from file and updating boxes
update_thread = threading.Thread(target=read_and_update)
update_thread.start()

root.mainloop()  # This will run the Tkinter main loop