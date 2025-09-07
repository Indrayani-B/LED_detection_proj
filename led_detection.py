
import os
from skimage import measure
import numpy as np
import cv2

def process_image(image_path, output_image_path, output_text_path, threshold_value=200, min_pixel_area=300):
    """
    Process the input image to detect bright regions (LEDs).

    Args:
        image_path (str): Path to the input image file.
        output_image_path (str): Path to save the output image with detected LEDs highlighted.
        output_text_path (str): Path to save the detection results in a text file.
        threshold_value (int): Threshold value to isolate bright regions (default=200).
        min_pixel_area (int): Minimum area of connected components to consider as LEDs (default=300).
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image file '{image_path}' not found.")

    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Error reading the image file. Please ensure it is a valid image.")

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Threshold the image to reveal light regions
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Perform erosion and dilation to remove noise
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=4)

    # Perform connected component analysis
    labels = measure.label(thresh, connectivity=2, background=0)
    mask = np.zeros(thresh.shape, dtype="uint8")

    # Loop over unique components
    for label in np.unique(labels):
        if label == 0:
            continue

        # Construct a mask for the current label
        labelMask = np.zeros(thresh.shape, dtype="uint8")
        labelMask[labels == label] = 255

        # Count the number of pixels in the component
        numPixels = cv2.countNonZero(labelMask)

        # Add the large components to the mask
        if numPixels > min_pixel_area:
            mask = cv2.add(mask, labelMask)

    # Find contours in the mask and sort them from left to right
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    # Initialize lists to store centroid coordinates and area
    centroids = []
    areas = []

    # Loop over the contours
    for i, c in enumerate(contours):
        # Calculate the area of the contour
        area = cv2.contourArea(c)

        # Calculate the centroid of the contour
        M = cv2.moments(c)
        if M["m00"] == 0:
            continue
        centroid = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Draw the bright spot on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, centroid, 10, (0, 0, 255), -1)

        # Append centroid coordinates and area to the respective lists
        centroids.append(centroid)
        areas.append(area)

    # Resize output image before saving
    desired_width = 500  # Adjust as needed
    desired_height = 400  # Adjust as needed
    image = cv2.resize(image, (desired_width, desired_height), interpolation=cv2.INTER_AREA)

    # Save the resized output image
    cv2.imwrite(output_image_path, image)

    # Write the number of LEDs detected to the text file
    with open(output_text_path, "w") as file:
        file.write(f"No. of LEDs detected: {len(centroids)}\n")

        # Loop over the LEDs and write their centroid coordinates and area to the file
        for i, centroid in enumerate(centroids):
            area = areas[i]
            file.write(f"        LED {i + 1} - Centroid: {centroid}\n")
            file.write(f"        Area: {area}\n")

if __name__ == "__main__":
    # Define paths
    input_image_path = "led1.jpeg"  # Replace with your input image path
    output_image_path = "output/led_detection_result.png"
    output_text_path = "output/led_detection_results.txt"

    # Process the image
    try:
        process_image(input_image_path, output_image_path, output_text_path)
        print(f"Processing complete. Results saved to '{output_image_path}' and '{output_text_path}'.")
    except Exception as e:
        print(f"Error: {e}")
