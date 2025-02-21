#SECURE DATA HIDING IN IMAGE USING STEGANOGRAPHY


#Overview

This project demonstrates the concept of Image Steganography, a technique used to hide secret information (data) within an image. In this case, the data is hidden inside the least significant bits (LSB) of an image's pixels. This method allows for data to be hidden in plain sight while maintaining the visual integrity of the image.The project is implemented using Python and supports hiding and retrieving textual data within an image file. This technique can be used to securely transmit data by embedding it inside an image file.


#Features

Hide text-based data (message) inside an image.

Extract the hidden message from an image.

Support for different image formats (PNG, JPEG, etc.).

Preserve the quality of the image while embedding the data.


#Requirements

To run this project, you need the following Python libraries:

1. Pillow (for image processing)
  
2. numpy (for handling binary data)

3. os (for file and directory operations)


#Install the dependencies using:

pip install pillow numpy


#Files Structure

steganography.py – The main Python script that handles the embedding and extraction of data.

README.md – This README file.

example_image.png – A sample image to demonstrate the project.

hiddendata_image.png – A image that contains the hidden data.


