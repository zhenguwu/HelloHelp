# Google Cloud Vision Methods
from google.cloud import vision
from collections import Counter
import re
from PIL import Image, ImageDraw
from io import BytesIO

def detect_text_location(content, match_string):
    """Detects text in the file."""

    # Break match_string into words
    match = re.sub(r'[^\w\s]', '', match_string).split()
    matchLower = [x.lower() for x in match]
    print("Matching for text: ", end="")
    print(match)

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    image_file = BytesIO(content)
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    matchRanking = []
    for text in texts:
        if " " in text.description:
            print("Found multiword: " + text.description)
        if (text.description.lower() in matchLower):
            # Only take first and third vertex
            vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices][::2]
            draw.rectangle(vertices, outline="red", width=10)
            matchRanking.append({text.description: vertices})
    print(matchRanking)

    all_texts = [list(item.keys())[0] for item in matchRanking]

    # Count occurrences of each text (case-sensitive)
    counts = Counter(all_texts)

    # Find a match that is both in 'match' (case-sensitive) and has a repetition of 1
    unique_match = None
    for text in counts:
        if counts[text] == 1 and text in match:
            unique_match = text
            break

    # Decide on the outcome based on finding a unique match
    if unique_match is not None:
        # Extract the bounds for the unique match
        unique_match_bounds = [item[unique_match] for item in matchRanking if unique_match in item][0]
        result = {"text": unique_match, "bounds": unique_match_bounds}
    else:
        raise ValueError("No unique case-sensitive match found with repetition 1.")
    print("best match: ")
    print(result)
    draw.rectangle(result["bounds"], outline="green", width=10)
    image.show()

        
        # print(f'\n"{text.description}"')

        # vertices = [
        #     f"({vertex.x},{vertex.y})" for vertex in text.bounding_poly.vertices
        # ]

        # print("bounds: {}".format(",".join(vertices)))

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
if __name__ == '__main__':
    detect_text_location('uploads/test.png', "Search restaurants, cuisines, etc.")