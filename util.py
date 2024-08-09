import os
import pickle
import cv2
import pytesseract

import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Helvetica bold', 20)
                    )

    return button


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=2,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
        j += 1

    if match:
        return db_dir[j - 1][:-7]
    else:
        return 'unknown_person'


def extract_and_detect(img, db_path):
    # Load the image
    image_path = 'data/spl100/bad.JPG'
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to load image at {image_path}")
        return

    # Define the coordinates for the ROI (manually inspected)
    x, y, w, h = 163, 200, 71, 27  # Example coordinates Spl100

    # Ensure coordinates are within the image bounds
    height, width, _ = image.shape
    if x < 0 or y < 0 or x + w > width or y + h > height:
        print("Error: ROI coordinates are out of image bounds")
        return

    # Crop the ROI from the image
    roi = image[y:y+h, x:x+w]

    # Save the cropped ROI as an image
    output_path = 'data/spl100/extracted_roi_manual.png'
    cv2.imwrite(output_path, roi)
    print(f"Cropped ROI saved to {output_path}")

    # Read the cropped ROI image
    image = cv2.imread(output_path)
    image = cv2.resize(image, None, fx=1.5, fy=1.5)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # Apply Otsu's thresholding
    _, otsu_thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_OTSU)

    # Optional: Increase the contrast of the image
    contrast_enhanced = cv2.convertScaleAbs(otsu_thresh, alpha=1.5, beta=0)

    # Morphological operations to enhance the threshold image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morphed = cv2.morphologyEx(contrast_enhanced, cv2.MORPH_OPEN, kernel)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    morphed = cv2.erode(morphed, kernel)
    cv2.imshow("Processed Image", morphed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Detect digits from the preprocessed image
    config = '--psm 6 -c tessedit_char_whitelist="0123456789."'
    detected_text = pytesseract.image_to_string(morphed, config=config, lang='lets').replace('\f', '').replace('\n', '')

    # Process the detected text to add a decimal point
    if len(detected_text) > 1:
        index = detected_text.find(detected_text[1:])
        detected_text = detected_text[:index] + '.' + detected_text[index:]

    # Print the detected text
    print(output_path, detected_text)

    # Save the detected value to a file
    output_file = 'detected_value.txt'
    with open(output_file, 'w') as file:
        file.write(detected_text)
