import cv2
import pytesseract

def detect_7_segments(image):
    config = '--psm 6 -c tessedit_char_whitelist="0123456789."'
    return pytesseract.image_to_string(image, config=config, lang='lets')


# Image file path
img_file = 'extracted_roi_manual.png'
# Read the image
image = cv2.imread(img_file)
image = cv2.resize(image, None, fx=1.5, fy=1.5)
#11717
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
cv2.imshow("n", otsu_thresh)
cv2.waitKey(0)

# Detect digits from the preprocessed image
detected_text = detect_7_segments(otsu_thresh).replace('\f', '').replace('\n', '')
detected_text = ''.join(detected_text.split())

# Print the detected text
print(img_file, detected_text)

