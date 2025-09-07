# 💡 LED Detection Project :

![Python](https://img.shields.io/badge/Python-3.11-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-orange)
![License](https://img.shields.io/badge/License-MIT-green)

A **Python-based LED detection tool** that identifies bright light sources in images, highlights them, and generates detailed reports with LED count, positions, and areas. Perfect for hobbyists, electronics enthusiasts, and image processing projects.  

---

## 🚀 Features :
- 🔍 Detect and highlight bright regions (LEDs) in images  
- 🖼 Output annotated images with contours and centroids  
- 📝 Export detailed text reports (LED count, positions, area)  
- ⚙️ Customizable threshold and minimum pixel area  

---

## ⚙️ Installation & Setup :
-git clone https://github.com/Indrayani-B/LED_detection_proj.git
-python -m venv venv
-venv\Scripts\activate   # Windows
-pip install -r requirements.txt

---

##⚡ How It Works :
-Converts the image to grayscale
-Applies thresholding to isolate bright regions
-Removes noise with erosion and dilation
-Detects LED candidates via connected component analysis
-Extracts contours, centroids, and area
-Draws results on the image and saves a detailed report
