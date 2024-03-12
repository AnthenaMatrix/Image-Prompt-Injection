import cv2
import numpy as np

def text_to_binary(text):
    binary_string = ''.join(format(ord(char), '08b') for char in text)
    return binary_string

def embed_prompt(image_path, prompt):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the prompt text to binary
    binary_prompt = text_to_binary(prompt)

    # Embed the binary prompt into the least significant bits of the image pixels
    prompt_index = 0
    for row in image:
        for pixel in row:
            if prompt_index >= len(binary_prompt):
                break
            for i in range(3):  # Embed in RGB channels
                pixel[i] = pixel[i] & ~1 | int(binary_prompt[prompt_index])
                prompt_index += 1
        if prompt_index >= len(binary_prompt):
            break

    # Save the modified image
    cv2.imwrite("image_with_prompt.png", image)
    print("Prompt embedded successfully.")

def extract_prompt(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Extract the binary prompt from the least significant bits of the image pixels
    binary_prompt = ""
    for row in image:
        for pixel in row:
            for i in range(3):  # Extract from RGB channels
                binary_prompt += str(pixel[i] & 1)

    # Convert the binary prompt to text
    extracted_prompt = ""
    for i in range(0, len(binary_prompt), 8):
        extracted_prompt += chr(int(binary_prompt[i:i+8], 2))

    return extracted_prompt

# Example usage:
if __name__ == "__main__":
    # Define the image path and prompt
    image_path = "original_image.png"
    prompt = "This is a secret prompt that will be embedded within the image."

    # Embed the prompt into the image
    embed_prompt(image_path, prompt)

    # Extract the prompt from the modified image
    extracted_prompt = extract_prompt("image_with_prompt.png")
    print("Extracted prompt:", extracted_prompt)
