import tkinter as tk
from tkinter import filedialog, END
from PIL import Image, ImageDraw, ImageFont, ImageTk

USER_IMAGES = []


# Function to add a watermark to the image
def apply_watermark(watermark_text):
    # Get the image
    new_image = USER_IMAGES[1]

    # Creating a drawing object
    draw = ImageDraw.Draw(new_image)

    # Define the font of the watermark
    font = ImageFont.truetype("arial.ttf", 24)

    # Calculate the width and height to position the watermarks
    a, b, text_width, text_height = draw.textbbox((0, 0), watermark_text, font=font)

    # Adding the watermarks into place
    for y in range(5, new_image.height, text_height + 20):
        for x in range(1, new_image.width, text_width + 50):
            draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 200))

    # Adding the new image into the list and display the watermark image.
    USER_IMAGES.append(new_image)
    new_img = ImageTk.PhotoImage(new_image)
    imageLabel.config(image=new_img)
    imageLabel.image = new_img


# Function triggers as soon as adding watermark is clicked.
def watermark_click():
    # Getting the label of the button
    get_watermark_button_text = activate_watermark.cget("text")

    # If the button shows "Add Watermark"
    if "Add Watermark" in get_watermark_button_text:
        watermark_entry = watermark_text_entry.get()
        if len(watermark_entry) == 0:
            hidden_label.config(text="The Watermark need to be filled.", fg="red")
        elif len(USER_IMAGES) == 0:
            hidden_label.config(text="You need to upload an image first.", fg="red")
        else:
            hidden_label.config(text="")
            apply_watermark(watermark_entry)
            activate_watermark.config(text="Remove Watermark")

    # If the button shows "Remove Watermark"
    else:
        USER_IMAGES.pop()
        USER_IMAGES.pop()
        img_open = Image.open(USER_IMAGES[0])
        USER_IMAGES.append(img_open)
        img = ImageTk.PhotoImage(img_open)
        imageLabel.config(image=img)
        imageLabel.image = img
        activate_watermark.config(text="Add Watermark to Image")


def upload_image():
    get_button_text = add_image.cget('text')
    if "Upload" in get_button_text:
        image_filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png; *.jpeg; *.jpg")])
        if image_filepath:
            img_open = Image.open(image_filepath)
            USER_IMAGES.append(image_filepath)
            USER_IMAGES.append(img_open)
            img = ImageTk.PhotoImage(img_open)
            imageLabel.config(image=img)
            imageLabel.image = img
            add_image.config(text="Remove Image")
    else:
        USER_IMAGES.pop()
        USER_IMAGES.pop()
        imageLabel.image = None
        add_image.config(text="Upload an Image")

        get_watermark_button_text = activate_watermark.cget("text")
        # If the button shows "Add Watermark"
        if "Add Watermark" not in get_watermark_button_text:
            USER_IMAGES.pop()
            watermark_text_entry.delete(0, END)
            activate_watermark.config(text="Add Watermark to Image")


def save_image():
    if len(USER_IMAGES) == 3:
        save_filepath = filedialog.asksaveasfilename(defaultextension=".jpg",
                                                     filetypes=[("All Files", "*.*"), ("PNG Files", "*.png"),
                                                                ("JPEG Files", "*.jpg")])
        if save_filepath:
            if not save_filepath.lower().endswith((".png", ".jpg", "jpeg")):
                hidden_label.config(text="Invalid file format. Please choose a valid format.", fg="red")
            else:
                image = USER_IMAGES[1]
                image.save(save_filepath)
                USER_IMAGES.pop()
                USER_IMAGES.pop()
                USER_IMAGES.pop()
                watermark_text_entry.delete(0, END)
                imageLabel.image = None
                add_image.config(text="Upload an Image")
                activate_watermark.config(text="Add Watermark to Image")
        else:
            hidden_label.config(text="No file path provided. Image not saved.", fg="red")


window = tk.Tk()
window.title("Image Watermark")
window.geometry("800x600")

# Upload Image
add_image = tk.Button(window, text="Upload an Image", command=upload_image)
add_image.pack()

imageLabel = tk.Label(window, text="add image", bg="grey")
imageLabel.pack(pady=10)

# Watermark Components
watermark_label = tk.Label(window, text="Watermark Text: ")
watermark_label.pack()

watermark_text_entry = tk.Entry(window)
watermark_text_entry.pack()

activate_watermark = tk.Button(window, text="Add Watermark to Image", command=watermark_click)
activate_watermark.pack(pady=20)

# Warning Label
hidden_label = tk.Label(window)
hidden_label.pack()

# Save Image Button
save_button = tk.Button(window, text="Save Image", command=save_image)
save_button.pack(pady=10)

window.mainloop()
