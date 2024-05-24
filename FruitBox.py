# FruitBox.py
# FruitBox.py
import tkinter as tk
from PIL import Image, ImageTk

class FruitBoxesApp:
    def __init__(self, master, window_width, window_height):
        self.master = master
        self.master.title("Fruit Boxes")

        # Set window size
        self.master.geometry(f"{window_width}x{window_height}")

        # Load background image and resize it to match window size
        background_image = Image.open("images/background.png")
        background_image = background_image.resize((window_width, window_height))
        self.background_photo = ImageTk.PhotoImage(background_image)

        self.canvas = tk.Canvas(master, bg="white", width=window_width, height=window_height)
        self.canvas.pack(fill="both", expand=True)

        # Display background image covering the entire window
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)

        # Define the initial positions for the bar images and fruit images
        self.image_positions = [(130, 125), (555, 125), (985, 125), (1415, 125)]
        self.fruit_positions = [(70, 424), (495, 424), (920, 424), (1343, 424)]

        # Rest of your code...


        self.image_labels = []
        self.fruit_labels = []
        self.box_images = []
        self.box_fruits = {}  # Dictionary to store selected fruit for each box

        for i, pos in enumerate(self.image_positions):
            # Create image labels at the specified positions
            image_label = self.canvas.create_image(pos[0], pos[1], anchor="nw")
            self.image_labels.append(image_label)

            # Create fruit labels at the specified positions
            fruit_label = self.canvas.create_image(self.fruit_positions[i][0], self.fruit_positions[i][1], anchor="nw")
            self.fruit_labels.append(fruit_label)

            # Initialize box images with empty image
            empty_image = Image.open("images/empty_bar.png").resize((150, 150))
            empty_photo = ImageTk.PhotoImage(empty_image)
            self.box_images.append([empty_photo] * 4)  # Each box has 4 stages, initialize with empty image

        # Initialize the dropdown menus directly below each image
        self.dropdowns = []
        self.info_frames = []
        for i, pos in enumerate(self.image_positions):
            variable = tk.StringVar(master)
            options = ["Empty", "Tomatoes", "Oranges", "Potatoes", "Kiwis", "Apples", "Bananas"]
            variable.set("Empty")  # Set default option to "Empty"

            dropdown = tk.OptionMenu(self.canvas, variable, *options,
                                     command=lambda value, idx=i: self.update_image(idx, value))
            dropdown.config(font=("Helvetica", 12))  # Set the font size for the dropdown
            dropdown['menu'].config(font=("Helvetica", 12))  # Set the font size for the dropdown menu items
            self.dropdowns.append(variable)

            # Position dropdown menu directly below the image
            self.canvas.create_window(pos[0] - 50, pos[1] + 240, anchor="nw", window=dropdown)

            # Create a frame for the info labels, initially hidden
            info_frame = tk.Frame(master, bg="white", borderwidth=2, relief="solid", width=250, height=250)
            weight_label = tk.Label(info_frame, text="Weight: 0", bg="white", font=("Helvetica", 13))
            avg_weight_label = tk.Label(info_frame, text="Avg. weight: 0", bg="white", font=("Helvetica", 13))
            no_of_fruit_label = tk.Label(info_frame, text="No. of fruit: 0", bg="white", font=("Helvetica", 13))

            weight_label.grid(row=0, column=0, padx=5, pady=5)
            avg_weight_label.grid(row=1, column=0, padx=5, pady=5)
            no_of_fruit_label.grid(row=2, column=0, padx=5, pady=5)

            self.info_frames.append((info_frame, weight_label, avg_weight_label, no_of_fruit_label))

            # Position the info frame directly below the dropdown menu, centered
            info_frame.place(x=pos[0] - 35, y=pos[1] + 250)
            info_frame.place_forget()

        self.update_boxes([0] * 4)

    def update_image(self, box_index, fruit_type):
        if fruit_type == "Empty":
            # Set the box images to always show empty_bar if "Empty" is selected
            empty_image = Image.open("images/empty_bar.png").resize((150, 150))
            empty_photo = ImageTk.PhotoImage(empty_image)
            self.box_images[box_index] = [empty_photo] * 4

            # Hide the info frame
            self.hide_info_frame(box_index)

            # Clear the fruit image
            self.canvas.itemconfig(self.fruit_labels[box_index], image="")
        else:
            fruit_images = self.get_fruit_images(fruit_type)
            if fruit_images:
                images = [Image.open(path).resize((150, 150)) for path in fruit_images]
                self.box_images[box_index] = [ImageTk.PhotoImage(img) for img in images]

            # Load and set the fruit image
            fruit_image_path = f"images/{fruit_type.lower()}.png"
            fruit_image = Image.open(fruit_image_path).resize((100, 100))
            fruit_photo = ImageTk.PhotoImage(fruit_image)
            self.canvas.itemconfig(self.fruit_labels[box_index], image=fruit_photo)
            self.box_fruits[box_index] = fruit_photo  # Store the reference to avoid garbage collection

            # Show the info frame
            self.show_info_frame(box_index)

        # Update the image of the label
        self.canvas.itemconfig(self.image_labels[box_index], image=self.box_images[box_index][0])

        # Update the avg weight and no. of fruit
        self.update_info(box_index, 0)  # Reset weight to 0 initially

    def get_fruit_images(self, fruit_type):
        # Return the image paths for the selected fruit type
        return {
            "Empty": ["images/empty_bar.png"] * 4,
            "Tomatoes": ["images/empty_bar.png",
                         "images/red1.png",
                         "images/red2.png",
                         "images/red3.png"],
            "Oranges": ["images/empty_bar.png",
                        "images/orange1.png",
                        "images/orange2.png",
                        "images/orange3.png"],
            "Potatoes": ["images/empty_bar.png",
                         "images/brown1.png",
                         "images/brown2.png",
                         "images/brown3.png"],
            "Kiwis": ["images/empty_bar.png",
                      "images/green1.png",
                      "images/green2.png",
                      "images/green3.png"],
            "Apples": ["images/empty_bar.png",
                       "images/red1.png",
                       "images/red2.png",
                       "images/red3.png"],
            "Bananas": ["images/empty_bar.png",
                        "images/yellow1.png",
                        "images/yellow2.png",
                        "images/yellow3.png"]
        }.get(fruit_type, [])

    def update_boxes(self, last_elements):
        try:
            for i, last_element in enumerate(last_elements):
                fruit_type = self.dropdowns[i].get()
                if fruit_type == "Empty":
                    image_index = 0  # Always empty
                else:
                    # Choose image based on fruit count range
                    if last_element <= 0.5:
                        image_index = 0  # Empty
                    elif last_element <= 1.25:
                        image_index = 1  # First stage
                    elif last_element <= 2:
                        image_index = 2  # Second stage
                    else:
                        image_index = 3  # Third stage

                # Update the image of the label
                self.canvas.itemconfig(self.image_labels[i], image=self.box_images[i][image_index])

                # Update the info frame
                self.update_info(i, last_element)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_avg_weight(self, fruit_type):
        # Return the average weight for the selected fruit type
        avg_weights = {
            "Tomatoes": 0.1,
            "Oranges": 0.24,
            "Potatoes": 0.15,
            "Kiwis": 0.075,
            "Apples": 0.18,
            "Bananas": 0.12,
            "Empty": 1  # Avoid division by zero, not used actually
        }
        return avg_weights.get(fruit_type, 0)

    def update_info(self, box_index, weight):
        fruit_type = self.dropdowns[box_index].get()
        avg_weight = self.get_avg_weight(fruit_type) * 1000  # Convert to integer and multiply by 1000
        if self.get_avg_weight(fruit_type) > 0:
            num_fruits = int(weight / self.get_avg_weight(fruit_type))  # Convert to integer
        else:
            num_fruits = 0

        # Update labels
        self.info_frames[box_index][1].config(text=f"Weight: {weight:.2f}kg")
        self.info_frames[box_index][2].config(text=f"Avg. weight: {int(avg_weight)}g")  # Display as integer
        self.info_frames[box_index][3].config(text=f"No. of fruit: {int(num_fruits)}")

    def show_info_frame(self, box_index):
        self.info_frames[box_index][0].place(x=self.image_positions[box_index][0] - 65,
                                             y=self.image_positions[box_index][1] + 450)

    def hide_info_frame(self, box_index):
        self.info_frames[box_index][0].place_forget()

