import cv2

# Load the image
image_path = 'db/temp_capture_image.jpg'
image = cv2.imread(image_path)

# Define the coordinates for the ROI (manually inspected)
# Adjust these coordinates based on the position of the blue display
#x, y, w, h = 100, 200, 55, 27  # Example coordinates compact
#x, y, w, h = 163, 143, 60, 27 #Example coordinates DIPL
#x, y, w, h = 163, 200, 71, 27 #Example coordinates Spl100
x, y, w, h = 282, 218, 143, 41



# Crop the ROI from the image
roi = image[y:y+h, x:x+w]

# Save the cropped ROI as an image
output_path = 'extracted_roi_manual.png'
cv2.imwrite(output_path, roi)
