from PIL import ImageDraw, Image

# Define the bounding box coordinates for the "9:00 PM" button again
button_top_left = (500, 100)
button_bottom_right = (1550, 200)

# Open the image
img = Image.open("images/screenshot.png")

# Initialize the drawing context
draw = ImageDraw.Draw(img)

# Define the color and width of the bounding box
box_color = 'red'
box_width = 5

# Draw the bounding box on the image
draw.rectangle([button_top_left, button_bottom_right], outline=box_color, width=box_width)

# Save the image with the bounding box
img_with_box_path = "images/screenshot2.png"
img.save(img_with_box_path)
