import os
import tkinter as tk
from tkinter import messagebox as mb
from PIL import Image, ImageTk
import time

# Function to convert characters to binary
def string_to_binary(data):
    return [format(ord(i), '08b') for i in data]

# Helper function to modify the pixel based on binary data
def modify_pixel_for_data(pixels, binary_char):
    for bit in range(8):
        if binary_char[bit] == '1' and (pixels[bit] % 2 == 0):
            pixels[bit] += 1
        elif binary_char[bit] == '0' and (pixels[bit] % 2 != 0):
            pixels[bit] -= 1
    return tuple(pixels)

# Function to generate data to be hidden in the image
def generate_data(pixels, data):
    data_in_binary = string_to_binary(data) + ['00000011']  # Append a delimiter
    image_data = iter(pixels)
    
    for binary_char in data_in_binary:
        pixels = [val for val in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        modified_pixels = modify_pixel_for_data(pixels, binary_char)
        yield modified_pixels[:3]
        yield modified_pixels[3:6]
        yield modified_pixels[6:9]

# Function to encode data into the image
def encryption(img, data):
    x, y = 0, 0
    for pixel in generate_data(img.getdata(), data):
        img.putpixel((x, y), pixel)
        if x == img.size[0] - 1:
            x = 0
            y += 1
        else:
            x += 1

# Function to check if the file exists
def check_file_exists(file_path):
    if not os.path.exists(file_path):
        mb.showerror("Error", f"The file {file_path} does not exist.")
        return False
    return True

# Function to decode data from the image
def decode_image_data(img):
    data = ''
    image_data = iter(img.getdata())
    decoding = True
    
    while decoding:
        pixels = [value for value in image_data.__next__()[:3] + image_data.__next__()[:3] + image_data.__next__()[:3]]
        binary_string = ''.join(['0' if i % 2 == 0 else '1' for i in pixels[:8]])
        char = chr(int(binary_string, 2))
        
        if char == chr(3):  # Check for the delimiter
            decoding = False
        else:
            data += char
    return data

# Function to handle encoding process
def main_encryption(img_path, data, new_image_name):
    if not check_file_exists(img_path):
        return
    
    try:
        image = Image.open(img_path, 'r')
        new_image = image.copy()
        encryption(new_image, data)
        new_image.save(f"{new_image_name}.png", 'PNG')
        mb.showinfo("Success", "Image encoded successfully!")
    except Exception as e:
        mb.showerror("Error", str(e))

# Function to handle decoding process
def main_decryption(img_path, strvar):
    if not check_file_exists(img_path):
        return
    
    try:
        image = Image.open(img_path, 'r')
        data = decode_image_data(image)
        strvar.set(data)
    except Exception as e:
        mb.showerror("Error", str(e))

# Smooth fade-in animation effect for buttons
def fade_in_button(button):
    button.pack_forget()  # Remove button initially
    time.sleep(0.1)
    button.pack()  # Show the button with fade-in effect

# Function to create encoding window
def encode_image():
    encode_wn = tk.Toplevel(root)
    encode_wn.title("Encode an Image")
    encode_wn.geometry('500x350')
    encode_wn.config(bg='#b0e0e6')

    title = tk.Label(encode_wn, text="Encode an Image", font=("Arial", 18, "bold"), bg='#b0e0e6', fg="#003366")
    title.pack(pady=20)
    
    # Image Path
    label_img_path = tk.Label(encode_wn, text="Enter Image Path:", font=("Arial", 12), bg='#b0e0e6', fg="#003366")
    label_img_path.pack(pady=5)
    img_path_entry = tk.Entry(encode_wn, width=40, font=("Arial", 12))
    img_path_entry.pack(pady=5)

    # Data to encode
    label_data = tk.Label(encode_wn, text="Enter Data to Encode:", font=("Arial", 12), bg='#b0e0e6', fg="#003366")
    label_data.pack(pady=5)
    data_to_encode_entry = tk.Entry(encode_wn, width=40, font=("Arial", 12))
    data_to_encode_entry.pack(pady=5)

    # Output Filename
    label_output = tk.Label(encode_wn, text="Output File Name (without extension):", font=("Arial", 12), bg='#b0e0e6', fg="#003366")
    label_output.pack(pady=5)
    output_filename_entry = tk.Entry(encode_wn, width=40, font=("Arial", 12))
    output_filename_entry.pack(pady=5)

    # Encode Button with fade-in effect
    def encode_button_action():
        img_path = img_path_entry.get()
        data = data_to_encode_entry.get()
        output_filename = output_filename_entry.get()
        main_encryption(img_path, data, output_filename)

    encode_button = tk.Button(encode_wn, text="Encode Image", font=("Arial", 14), bg="#ffb6c1", command=encode_button_action)
    encode_button.pack(pady=20)

    fade_in_button(encode_button)

# Function to create decoding window
def decode_image():
    decode_wn = tk.Toplevel(root)
    decode_wn.title("Decode an Image")
    decode_wn.geometry('500x350')
    decode_wn.config(bg='#add8e6')

    title = tk.Label(decode_wn, text="Decode an Image", font=("Arial", 18, "bold"), bg='#add8e6', fg="#003366")
    title.pack(pady=20)

    # Image Path
    label_img_path = tk.Label(decode_wn, text="Enter Image Path:", font=("Arial", 12), bg='#add8e6', fg="#003366")
    label_img_path.pack(pady=5)
    img_path_entry = tk.Entry(decode_wn, width=40, font=("Arial", 12))
    img_path_entry.pack(pady=5)

    # Decoded text
    label_data = tk.Label(decode_wn, text="Decoded Data:", font=("Arial", 12), bg='#add8e6', fg="#003366")
    label_data.pack(pady=5)
    decoded_data_text = tk.Text(decode_wn, width=40, height=5, font=("Arial", 12), wrap=tk.WORD)
    decoded_data_text.pack(pady=5)

    # Decode Button with fade-in effect
    def decode_button_action():
        img_path = img_path_entry.get()
        decoded_data = tk.StringVar()
        main_decryption(img_path, decoded_data)
        decoded_data_text.delete(1.0, tk.END)
        decoded_data_text.insert(tk.END, decoded_data.get())

    decode_button = tk.Button(decode_wn, text="Decode Image", font=("Arial", 14), bg="#ffb6c1", command=decode_button_action)
    decode_button.pack(pady=20)

    fade_in_button(decode_button)

# Main Window for the application
root = tk.Tk()
root.title('Image Steganography - Professional & Magical')
root.geometry('500x400')
root.config(bg='#87cefa')

title = tk.Label(root, text="Welcome to Image Steganography", font=("Arial", 20, "bold"), bg='#87cefa', fg="#003366")
title.pack(pady=20)

# Buttons for Encoding and Decoding with hover effects
def on_enter_encode(e):
    encode_button.config(bg='#ff69b4')

def on_leave_encode(e):
    encode_button.config(bg='#ffb6c1')

def on_enter_decode(e):
    decode_button.config(bg='#ff69b4')

def on_leave_decode(e):
    decode_button.config(bg='#ffb6c1')

encode_button = tk.Button(root, text="Encode Image", font=("Arial", 14), bg="#ffb6c1", width=20, command=encode_image)
encode_button.pack(pady=20)

encode_button.bind("<Enter>", on_enter_encode)
encode_button.bind("<Leave>", on_leave_encode)

decode_button = tk.Button(root, text="Decode Image", font=("Arial", 14), bg="#ffb6c1", width=20, command=decode_image)
decode_button.pack(pady=20)

decode_button.bind("<Enter>", on_enter_decode)
decode_button.bind("<Leave>", on_leave_decode)

root.mainloop()
