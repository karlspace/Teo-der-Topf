# SPDX-FileCopyrightText: 2023 Karl Bauer (BAUER GROUP)
# SPDX-License-Identifier: MIT

import os
import requests
import string
import json

# Function to clean the string for valid folder and file names
def clean_string(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    clean_chars = ''.join(c for c in s if c in valid_chars)
    return clean_chars.lower().replace(' ', '-')

# Download the JSON data
response = requests.get('https://googlefonts.github.io/noto-emoji-animation/data/api.json')
data = response.json()

# Base URLs for the images
webp_url_base = 'https://fonts.gstatic.com/s/e/notoemoji/latest/{codepoint}/512.webp'
gif_url_base = 'https://fonts.gstatic.com/s/e/notoemoji/latest/{codepoint}/512.gif'

# Make sure the base directory exists
os.makedirs('assets/emoji-animation', exist_ok=True)

# Create a dictionary to map each category to a list of emotions
category_to_emotion = {}

# Loop over all the icons
for icon in data['icons']:
    # Get the category and convert it to a valid folder name
    category_name = clean_string(icon['categories'][0])

    # Get the codepoint
    codepoint = icon['codepoint']

    # Get the first tag and convert it to a valid file name
    tag_name = clean_string(icon['tags'][0])

    # Add the emotion to its category's list in the dictionary
    if category_name not in category_to_emotion:
        category_to_emotion[category_name] = []
    category_to_emotion[category_name].append(tag_name)

    # Create the directory if it doesn't exist
    directory_path = os.path.join('assets', 'emoji-animation', category_name)
    os.makedirs(directory_path, exist_ok=True)

    # Download and save the .webp and .gif files
    for ext in ['webp', 'gif']:
        # Create the URL for the image
        url = webp_url_base.format(codepoint=codepoint) if ext == 'webp' else gif_url_base.format(codepoint=codepoint)

        # Download the image
        response = requests.get(url)

        # Create the path for the image file
        file_path = os.path.join(directory_path, f"{tag_name}.{ext}")

        # Save the image file
        with open(file_path, 'wb') as f:
            f.write(response.content)

        print(f"Saved file: {file_path}")

# Save the dictionary of categories and their lists of emotions as a JSON file
with open('emotions.json', 'w') as f:
    json.dump(category_to_emotion, f, indent=4)

print("Saved collection in emotions.json")
