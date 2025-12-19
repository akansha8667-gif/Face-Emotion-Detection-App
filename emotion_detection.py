from fer import FER
import cv2

def detect_emotion_from_image(image_path):
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        return "Error: Unable to load image"
    
    # Initialize the emotion detector
    detector = FER(mtcnn=True)  # mtcnn for better face detection
    
    # Detect emotions
    emotions = detector.detect_emotions(img)
    if not emotions:
        return "No face detected"
    
    # Get the dominant emotion for the first face
    dominant_emotion = max(emotions[0]['emotions'], key=emotions[0]['emotions'].get)
    return dominant_emotion.capitalize()