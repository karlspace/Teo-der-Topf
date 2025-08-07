# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

import os
from PIL import Image

# Get the current script directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Specify the input directory and output roots
input_dir = os.path.join(script_dir, '../Application/assets', 'sources')
output_root1 = os.path.join(script_dir, '../Application/assets', 'emotion')
output_root2 = os.path.join(script_dir, '../Application/assets', 'emotion-flip')

# Initialize counters
processed_files_count = 0
rotated_files_count = 0

# Walk through the directory tree
for dirpath, dirnames, filenames in os.walk(input_dir):

    # Process each file
    for filename in filenames:
        if filename.endswith('.png'):

            # Get the relative path
            rel_path = os.path.relpath(dirpath, input_dir)

            # Construct output directories
            output_dir1 = os.path.join(output_root1, rel_path)
            output_dir2 = os.path.join(output_root2, rel_path)

            # Create output directories if they don't exist
            os.makedirs(output_dir1, exist_ok=True)
            os.makedirs(output_dir2, exist_ok=True)

            # Extract frame number from filename, pad it to 3 digits
            frame_num = filename.replace('frame', '').replace('.png', '')
            frame_num = str(int(frame_num) + 1).zfill(3)  # Pad the frame number with leading zeros
            new_filename = f'frame{frame_num}.png'

            # Open the image file
            with Image.open(os.path.join(dirpath, filename)) as img:

                # Save the original image to the output directory1
                img.save(os.path.join(output_dir1, new_filename))
                processed_files_count += 1

                # Rotate the image, save it to the output directory2
                img_rotated = img.rotate(180)
                img_rotated.save(os.path.join(output_dir2, new_filename))
                rotated_files_count += 1

# Print summary of actions
print(f"Total number of processed files: {processed_files_count}")
print(f"Total number of rotated files: {rotated_files_count}")

