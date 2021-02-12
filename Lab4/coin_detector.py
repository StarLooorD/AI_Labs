import numpy as np
import matplotlib.pyplot as plt
import cv2

# Frames period
N = 10
FILE_PATH = 'Coins1.mp4'

frames = []
# Capturing video
cap = cv2.VideoCapture(FILE_PATH)
# Check if cap is initialized
while cap.isOpened():
    ret, frame = cap.read()
    # If frame was not read
    if not ret:
        break
    # List with all frames
    frames.append(frame)
# Releasing resources
cap.release()
# Destroys all created windows
cv2.destroyAllWindows()
# Getting each frame through period
frames = frames[::N]
# Output number of frames used
print(f'Number of frames is: {len(frames)}')

# Tool that stitches our frames into one big image
stitcher = cv2.Stitcher_create(mode=1)
print("Stitching...")
# im is our big stitched image
_, im = stitcher.stitch(frames)
print("Stitching done!")

# Firstly showing stitched image without detected circles
plt.figure(figsize=(10, 10))
plt.imshow(im)
plt.show()

# Setting image to black and white
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# Applying a median blur to reduce noise and avoid false circle detection
img = cv2.medianBlur(img, 5)
cimg = im.copy()

print("Searching for coins...")
# Main method of cv2 that searches for circles in image
circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1, 10, np.array([]), 69, 21, 9, 26)

# Checking if circles founded
if circles is not None:
    # We need only b parameter here, its number of circles
    _a, b, _c = circles.shape
    for i in range(b):
        # Drawing circle perimeter
        cv2.circle(cimg, (int(circles[0][i][0]), int(circles[0][i][1])), int(circles[0][i][2]), (0, 0, 255), 2, cv2.LINE_AA)
        # Drawing circle centre
        cv2.circle(cimg, (int(circles[0][i][0]), int(circles[0][i][1])), 2, (0, 255, 0), 3, cv2.LINE_AA)

    print("Searching done!")
    # Output number of detected coins
    print(f"Number of coins: ", int(b))

    # Showing image with all circles detected
    plt.figure(figsize=(10, 10))
    plt.imshow(cimg)
    plt.show()
