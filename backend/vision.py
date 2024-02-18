# Google Cloud Vision Methods
from google.cloud import vision
from collections import Counter
import re
from PIL import Image, ImageDraw
from io import BytesIO
import Levenshtein

def similarity(word1, word2):
    # Calculate Levenshtein distance
    distance = Levenshtein.distance(word1.lower(), word2.lower())
    # Normalize to 0-1 scale
    max_len = max(len(word1), len(word2))
    if max_len == 0:
        return 1.0  # Both strings are empty
    similarity = 1 - distance / max_len
    return similarity

def detect_text_location(content, match_string, i, user_id):
    """Detects text in the file."""

    # Break match_string into words
    match = re.sub(r'[^\w\s]', '', match_string).split()
    #match = match_string.split()
    print("Matching for text: ", end="")
    print(match)

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

    texts = response.text_annotations

    image_file = BytesIO(content)
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)

    matchRanking = []
    for text in texts:
        if (text.description in match):
            # Only take first and third vertex
            vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices][::2]
            draw.rectangle(vertices, outline="red", width=10)
            matchRanking.append({text.description: vertices})
    
    # No matches found, use similarity
    if len(matchRanking) == 0:
        for text in texts:
            for word in match:
                sim = similarity(text.description, word)
                print(f"Similarity between '{text.description}' and '{word}': {sim}")
                if sim >= 0.8:
                    vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices][::2]
                    draw.rectangle(vertices, outline="blue", width=10)
                    matchRanking.append({text.description: vertices})
                    break
    if len(matchRanking) == 0:
        print("Nothing found!")
        return None
    
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
    result = None
    if unique_match is not None:
        # Extract the bounds for the unique match
        unique_match_bounds = [item[unique_match] for item in matchRanking if unique_match in item][0]
        result = {"text": unique_match, "bounds": unique_match_bounds}
    else:
        return None
    
    draw.rectangle(result["bounds"], outline="green", width=10)
    image.save('user_data/' + user_id + '/' + str(i) + '.png')
    
    return result["bounds"]
    
if __name__ == '__main__':
    detect_text_location('uploads/test.png', "Search restaurants, cuisines, etc.")