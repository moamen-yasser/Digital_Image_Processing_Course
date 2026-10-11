# ============================================
# Python Image Processing Using FOR Loops
# ============================================

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------------
# 1. Read and Display Image
# ------------------------------------------------

image = Image.open("image.png").convert("RGB")

plt.imshow(image)
plt.title("Original Image")
plt.axis("off")
plt.show()


# Convert image to NumPy array
img = np.array(image)

height, width, channels = img.shape

print("Image Height:", height)
print("Image Width :", width)
print("Channels    :", channels)


# ------------------------------------------------
# 2. Display Pixel Values
# ------------------------------------------------

print("\nFirst 5 x 5 pixels:")

for i in range(min(5, height)):
    for j in range(min(5, width)):
        print(f"pixel[{i},{j}] = {img[i,j]}")


# ------------------------------------------------
# 3. Convert RGB Image to Grayscale
# ------------------------------------------------

gray = np.zeros((height, width), dtype=np.uint8)

for i in range(height):
    for j in range(width):

        R = int(img[i, j, 0])
        G = int(img[i, j, 1])
        B = int(img[i, j, 2])

        # Grayscale formula
        gray_value = int(0.299 * R + 0.587 * G + 0.114 * B)

        gray[i, j] = gray_value


plt.imshow(gray, cmap="gray")
plt.title("Grayscale Image")
plt.axis("off")
plt.show()


# ------------------------------------------------
# 4. Convert Grayscale to Binary
# ------------------------------------------------

threshold = 128

binary = np.zeros((height, width), dtype=np.uint8)

for i in range(height):
    for j in range(width):

        if gray[i, j] >= threshold:
            binary[i, j] = 255
        else:
            binary[i, j] = 0


plt.imshow(binary, cmap="gray")
plt.title("Binary Image")
plt.axis("off")
plt.show()