# -*- coding: utf-8 -*-
"""
A script to convert a PNG image into a multi-size icon file (.ico).

This script uses the Pillow library for image processing.
You must install it first:
pip install Pillow

Usage in the terminal:
python script_name.py C:\path\to\image.png C:\path\to\favicon.ico
"""
import argparse
from pathlib import Path
from PIL import Image

def convert_png_to_favicon(input_path: Path, output_path: Path):
    """
    Converts a PNG file to an .ico file containing standard icon sizes.

    Args:
        input_path (Path): The path to the input PNG file.
        output_path (Path): The path where the favicon.ico file will be saved.
    """
    # A list of standard sizes that an .ico file should contain
    # for the best compatibility with various browsers and devices.
    icon_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

    print(f"Attempting to convert '{input_path.name}' to '{output_path.name}'...")

    try:
        # Open the original image using the Pillow library
        img = Image.open(input_path)

        # Check if the image is in RGBA mode (with transparency).
        # If not, convert it to preserve transparency.
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
            print("Image converted to RGBA mode to preserve transparency.")

        # Save the image in ICO format.
        # The Pillow library will automatically create a multi-layered icon
        # if we provide a list of sizes in the `sizes` parameter.
        img.save(output_path, format='ICO', sizes=icon_sizes)
        
        print(f"✅ Favicon successfully created at: {output_path}")

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    # We use argparse to create a professional command-line interface
    parser = argparse.ArgumentParser(
        description="Convert a PNG image to a multi-size .ico file.",
        epilog="Example: python convert.py logo.png favicon.ico"
    )
    
    # Define the arguments the script should accept
    parser.add_argument(
        "input_file", 
        type=str, 
        help="The path to the input PNG file."
    )
    parser.add_argument(
        "output_file", 
        type=str, 
        nargs='?', # '?' means the argument is optional
        default="favicon.ico", # Default name for the output file
        help="The path for the output .ico file (default: favicon.ico)."
    )
    
    args = parser.parse_args()
    
    # Convert the string paths to Path objects for better handling
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    # Ensure the output file has the .ico extension
    if output_path.suffix.lower() != ".ico":
        output_path = output_path.with_suffix(".ico")
        
    convert_png_to_favicon(input_path, output_path)
