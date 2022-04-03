from tkinter.filedialog import askopenfile
from tkinter import *
from PIL import Image, ImageTk, ImageDraw, ImageFont

file_name = ""
file_path = ""
new_file_name = ""
watermark_image = None

window = Tk()
window.title("Add watermarks to your photos!")
window.config(padx=20, pady=20)
canvas = Canvas(width=500, height=500)


def get_watermark_position(image_dimensions):
    watermark_position = None
    position_str = position_variable.get()

    # set anchor, x_position and y_position based on position dropdown selection
    if position_str == "Center":
        watermark_position = {"anchor": "mm", "x_pos": image_dimensions[0] / 2, "y_pos": image_dimensions[1] / 2}
    elif position_str == "Top Left":
        watermark_position = {"anchor": "lt", "x_pos": 0, "y_pos": 0}
    elif position_str == "Top Right":
        watermark_position = {"anchor": "rt", "x_pos": image_dimensions[0], "y_pos": 0}
    elif position_str == "Bottom Left":
        watermark_position = {"anchor": "lb", "x_pos": 0, "y_pos": image_dimensions[1]}
    else:
        watermark_position = {"anchor": "rb", "x_pos": image_dimensions[0], "y_pos": image_dimensions[1]}

    return watermark_position


def add_image():
    global file_path, file_name, new_file_name
    file = askopenfile(filetypes=[('Image Files', '*jpeg'), ('Image Files', '*png')]).name
    file_path = file.split("/")
    file_name = file_path[-1]
    file_path = "/".join(file_path[:-1]) + "/"
    new_file_name = "watermarked_" + file_name
    canvas.delete("all")
    file_path_value["text"] = file_path
    file_name_value["text"] = file_name
    new_file_name_value["text"] = new_file_name

    # create Image
    im = Image.open(file)

    # resize image, so it fits in the window, real image remains full size
    resized_image = im.resize((500, 500))
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=NW, image=new_image)
    canvas.grid(row=3, column=0, columnspan=3)
    window.mainloop()


def add_watermark():
    pass
    global watermark_image
    image = Image.open(f"{file_path}{file_name}")

    # copies image to make changes
    watermark_image = image.copy()
    draw = ImageDraw.Draw(watermark_image)

    # selects font (need arial.ttf file in working directory, can use .load_default() otherwise
    fontsize = slider.get()
    font = ImageFont.truetype("arial.ttf", fontsize)
    # font = ImageFont.load_default()

    # get watermark position
    watermark_position = get_watermark_position(image.size)

    # add watermark
    watermark_text = watermark_entry.get()
    draw.text(
        xy=(watermark_position["x_pos"], watermark_position["y_pos"]),
        text=watermark_text,
        fill=(0, 0, 0),
        font=font,
        anchor=watermark_position["anchor"]
    )

    # purely visual, this renders the image on the GUI, real image is still full size, no resizing
    resized_image = watermark_image.resize((500, 500))
    new_image = ImageTk.PhotoImage(resized_image)
    canvas.create_image(0, 0, anchor=NW, image=new_image)
    canvas.grid(row=3, column=0, columnspan=3)
    window.mainloop()


def save_image():
    try:
        watermark_image.save(f'{file_path}{new_file_name}')
    except OSError:
        return print("Could not find file path")

    return print("Saved Successful")


# labels
file_path_label = Label(text="File path: ")
file_path_label.grid(row=0, column=1, sticky="w")
file_path_value = Label(text="")
file_path_value.grid(row=0, column=2, sticky="w")
file_name_label = Label(text="File name: ")
file_name_label.grid(row=1, column=1, sticky="w")
file_name_value = Label(text="")
file_name_value.grid(row=1, column=2, sticky="w")
new_file_name_label = Label(text="New file name: ")
new_file_name_label.grid(row=2, column=1, sticky="w")
new_file_name_value = Label(text="")
new_file_name_value.grid(row=2, column=2, sticky="w")

watermark_label = Label(text="Type your watermark:")
watermark_label.grid(row=5, column=0, sticky="w")
fontsize_label = Label(text="Font size: ")
fontsize_label.grid(row=6, column=0, sticky="w")
position_label = Label(text="Position: ")
position_label.grid(row=7, column=0, sticky="w")

# watermark text entry (easily change the watermark text)
watermark_entry_text = StringVar()
watermark_entry = Entry(textvariable=watermark_entry_text)
watermark_entry_text.set("YOUR NAME HERE")
watermark_entry.grid(row=5, column=1)

# font size (slider to select)
slider = Scale(from_=0, to=200, orient='horizontal')
slider.grid(row=6, column=1)

# watermark position menu (Choose Center, Top Left, ...)
watermark_avail_positions = ["Center", "Top Left", "Top Right", "Bottom Left", "Bottom Right"]
position_variable = StringVar(window)
position_variable.set(watermark_avail_positions[0])  # default value
position_selector = OptionMenu(window, position_variable, *watermark_avail_positions)
position_selector.grid(row=7, column=1)

# buttons
open_file_button = Button(text="Select image", command=add_image)
open_file_button.grid(row=0, column=0, rowspan=3)

add_watermark_button = Button(text="Add watermark", command=add_watermark)
add_watermark_button.grid(row=4, column=2, rowspan=3)

save_image_button = Button(text="Save image", command=save_image, padx=5, pady=10)
save_image_button.grid(row=8, column=1)

window.mainloop()
