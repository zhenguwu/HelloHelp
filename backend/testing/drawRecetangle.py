from PIL import Image, ImageDraw

def draw_rectangle(image_path, top_left, bottom_right):
    # Open the image
    image = Image.open(image_path)

    # Create drawing object
    draw = ImageDraw.Draw(image)

    # Draw rectangle outline
    draw.rectangle([top_left, bottom_right], outline="yellow", width=10)  # Increase the width for better visibility

    # Save or show the modified image
    # image.show()  # Uncomment this line to display the image
    image.save("images/output_image.png")  # Save the modified image

# Example usage
image_path = "images/screenshot.png"  # Provide the path to your input image
top_left = (655, 433)  # Top-left coordinates of the rectangle
bottom_right = (754, 461)  # Bottom-right coordinates of the rectangle

draw_rectangle(image_path, top_left, bottom_right)