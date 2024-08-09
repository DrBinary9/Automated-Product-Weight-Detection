import cv2

# Initialize variables to store coordinates
point1 = None
point2 = None

def click_event(event, x, y, flags, params):
    global point1, point2

    # checking for left mouse clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if point1 is None:
            # Store the first point coordinates
            point1 = (x, y)
            # Display the coordinates on the image window
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, str(x) + ',' + str(y), (x, y), font, 1, (255, 0, 0), 2)
            cv2.imshow('image', img)
        else:
            # Store the second point coordinates
            point2 = (x, y)
            # Calculate width and height
            w = point2[0] - point1[0]
            h = point2[1] - point1[1]
            # Display the coordinates (x1, y1, w, h)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = f"{point1[0]}, {point1[1]}, {w}, {h}"
            cv2.putText(img, text, (point2[0], point2[1]), font, 1, (0, 255, 0), 2)
            cv2.imshow('image', img)
            # Print the coordinates to the console
            print(text)
            # Reset points for next selection
            point1 = None
            point2 = None

    # checking for right mouse clicks
    if event == cv2.EVENT_RBUTTONDOWN:
        # displaying the coordinates on the Shell
        print(x, ' ', y)
        # displaying the color values at the point on the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        b = img[y, x, 0]
        g = img[y, x, 1]
        r = img[y, x, 2]
        cv2.putText(img, str(b) + ',' + str(g) + ',' + str(r), (x, y), font, 1, (255, 255, 0), 2)
        cv2.imshow('image', img)

if __name__ == "__main__":
    # reading the image
    img = cv2.imread('db/temp_capture_image.jpg', 1)

    # displaying the image
    cv2.imshow('image', img)

    # setting mouse handler for the image and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # wait for a key to be pressed to exit
    cv2.waitKey(0)

    # close the window
    cv2.destroyAllWindows()

