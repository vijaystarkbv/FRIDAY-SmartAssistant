import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import get_key
import os
from time import sleep

# Function to open and display images
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    # Generate the filenames for the images
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)

        try:
            # Open and display image
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

# Async function to send a request to Hugging Face
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=HEADERS, json=payload)
    return response.content

# Async function to generate images
async def generate_images(prompt: str):
    tasks = []

    for _ in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    # Wait for all tasks to get completed
    image_bytes_list = await asyncio.gather(*tasks)

    # Save the generated images to files
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ', '_')}{i + 1}.jpg", "wb") as f:
            f.write(image_bytes)

# Wrapping function to generate images synchronously
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Continuous loop to monitor the image generation request
while True:
    try:
        # Read the status and prompt from the data file
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data: str = f.read()

        prompt, status = data.split(",")

        if status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt=prompt)

            # Reset the status to prevent repeated execution
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False,False")
            
            break  # Exit the loop after generating images

        else:
            sleep(1)

    except:
        pass
     