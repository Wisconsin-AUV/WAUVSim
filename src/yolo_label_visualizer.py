import cv2
import numpy as np
from PIL import Image

# Open the image file
img = Image.open('15.png')

# Convert PIL image to NumPy array
img_array = np.array(img)

# Convert from RGB (PIL default) to BGR (OpenCV default)
img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

h, w, _ = img_array.shape

# Your normalized coordinates
pts_10 = [
    (0.316890, 0.677081), (0.225361, 0.673667), (0.131612, 0.669835),
    (0.132087, 0.753827), (0.133949, 0.843028), (0.308990, 0.843028)
]

pts_15 = [(0.949910, 0.425659), (0.411603, 0.401562), (0.404739, 0.683831), (0.400261, 0.863683), (0.514885, 0.861796), (0.927031, 0.851745), (0.939124, 0.626593)]

# 1. Scale to image size and convert to Integers
pts = np.array(pts_15) * [w, h]
pts = pts.astype(np.int32)

# 2. Draw the Lines (Polygon)
# We reshape strictly for the polylines function
pts_reshaped = pts.reshape((-1, 1, 2))
cv2.polylines(img_array, [pts_reshaped], isClosed=True, color=(0, 0, 255), thickness=2)

# 3. Draw the Big Dots
for point in pts:
    # point is [x, y]
    # radius=6 makes them big
    # thickness=-1 fills the circle solid
    cv2.circle(img_array, (point[0], point[1]), radius=6, color=(0, 255, 0), thickness=-1)

# Display
cv2.imshow('img', img_array)
cv2.waitKey(0)
cv2.destroyAllWindows()