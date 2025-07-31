# -*- coding: utf-8 -*-
"""
A script to resize an image to specified dimensions.

This script uses the Pillow library for image processing.
You must install it first:
pip install Pillow

Usage in the terminal:
python resize_image.py input_image.png 180x180 output_image.png
"""
import argparse
from pathlib import Path
from PIL import Image

def resize_image(input_path: Path, output_path: Path, size: tuple[int, int]):
    """
    Resizes an image to the specified size and saves it.

    Args:
        input_path (Path): The path to the input image file.
        output_path (Path): The path where the resized image will be saved.
        size (tuple[int, int]): A tuple with the new width and height (e.g., (180, 180)).
    """
    print(f"Resizing '{input_path.name}' to {size[0]}x{size[1]}...")

    try:
        # Open the original image using the Pillow library
        with Image.open(input_path) as img:
            # Resize the image. We use LANCZOS for the best quality downscaling.
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            
            # Save the resized image
            resized_img.save(output_path)
            
            print(f"✅ Image successfully saved at: {output_path}")

    except FileNotFoundError:
        print(f"❌ ERROR: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def parse_size(size_str: str) -> tuple[int, int]:
    """Helper function to parse size from a 'WIDTHxHEIGHT' string."""
    try:
        width, height = map(int, size_str.lower().split('x'))
        return width, height
    except ValueError:
        raise argparse.ArgumentTypeError("Size must be in WxH format (e.g., 180x180).")

if __name__ == "__main__":
    # We use argparse to create a professional command-line interface
    parser = argparse.ArgumentParser(
        description="Resize a PNG image to a specific size.",
        epilog="Example: python resize_image.py logo.png 180x180 apple-touch-icon.png"
    )
    
    # Define the arguments the script should accept
    parser.add_argument(
        "input_file", 
        type=str, 
        help="The path to the input PNG file."
    )
    parser.add_argument(
        "size",
        type=parse_size,
        help="The new size in WxH format (e.g., 180x180)."
    )
    parser.add_argument(
        "output_file", 
        type=str, 
        help="The path for the output image file."
    )
    
    args = parser.parse_args()
    
    # Convert the string paths to Path objects for better handling
    input_path = Path(args.input_file)
    output_path = Path(args.output_file)
    
    resize_image(input_path, output_path, args.size)
