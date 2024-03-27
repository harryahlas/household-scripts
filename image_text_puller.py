import os
from PIL import Image
import pytesseract

# Specify the path to the folder containing the JPG files
folder_path = 'D:\github\household-scripts\sample_images'

# Specify the path to the Tesseract executable if it's not in your PATH #
pytesseract.pytesseract.tesseract_cmd = r'D:\SoftwareInstalls\tesseract\tesseract.exe'

# Open the output file in write mode
with open('output.txt', 'w', encoding='utf-8') as output_file:
    # Iterate over all files in the specified folder
    for filename in os.listdir(folder_path):
        # Check if the file is a JPG
        if filename.endswith('.jpg'):
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)
            # Open the image file
            with Image.open(file_path) as img:
                # Use pytesseract to convert the image to text
                text = pytesseract.image_to_string(img)
                # Write the extracted text to the output file
                output_file.write(text + '\n')
