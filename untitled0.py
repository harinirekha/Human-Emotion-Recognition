# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1QdF0ApmwK4fiHzSwjtkuxxKAw3aihZ6g
"""

!pip install opencv-python-headless matplotlib fer tensorflow mtcnn

"""# **Detection In Image *Format***"""

import cv2
from fer import FER
import matplotlib.pyplot as plt

def detect_emotions(image_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to read image. Please check the file path.")
        return

    # Convert image to RGB (for matplotlib and FER)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Initialize FER detector
    detector = FER(mtcnn=True)  # Use MTCNN for face detection

    # Detect emotions
    emotions = detector.detect_emotions(rgb_image)

    # Initialize counters
    happy_count = 0
    sad_count = 0

    # Process detected emotions
    for emotion in emotions:
        emotion_scores = emotion['emotions']
        if emotion_scores['happy'] > 0.5:  # Threshold for "happy"
            happy_count += 1
        elif emotion_scores['sad'] > 0.5:  # Threshold for "sad"
            sad_count += 1

    # Display results
    print(f"Number of happy people: {happy_count}")
    print(f"Number of sad people: {sad_count}")

    # Plot the image with emotion boxes
    plt.imshow(rgb_image)
    plt.axis("off")
    plt.title("Emotion Detection")
    plt.show()

# Replace with the path to your image
image_path = "/content/multiracial-group-of-young-people-taking-selfie-photo.jpg"
detect_emotions(image_path)

"""# **Detection In a Video Format**"""

import cv2
from fer import FER
from google.colab.patches import cv2_imshow  # This line ensures cv2_imshow is imported

def detect_emotions_in_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file. Please check the file path.")
        return

    # Initialize FER detector
    detector = FER(mtcnn=True)  # Use MTCNN for face detection

    # Initialize counters
    happy_count = 0
    sad_count = 0
    total_frames = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:  # Break if no more frames are available
            break

        total_frames += 1
        # Convert the frame to RGB (required by FER)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect emotions in the frame
        emotions = detector.detect_emotions(rgb_frame)

        # Process detected emotions
        for emotion in emotions:
            emotion_scores = emotion['emotions']
            if emotion_scores['happy'] > 0.5:  # Threshold for "happy"
                happy_count += 1
            elif emotion_scores['sad'] > 0.5:  # Threshold for "sad"
                sad_count += 1

        # Display the frame with annotations (optional)
        for face in emotions:
            box = face["box"]  # Bounding box
            emotion_scores = face["emotions"]
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            x, y, w, h = box
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, dominant_emotion, (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

        # Show the frame (optional)
        cv2_imshow(frame)  # Use cv2_imshow to display the frame in Colab
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit (emulated in Colab logs)
            break

    # Release the video capture object
    cap.release()

    # Display the results
    print(f"Total frames processed: {total_frames}")
    print(f"Number of happy people detected: {happy_count}")
    print(f"Number of sad people detected: {sad_count}")

# Replace with the path to your video file
video_path = "/content/istockphoto-1272595740-640_adpp_is.mp4"
detect_emotions_in_video(video_path)