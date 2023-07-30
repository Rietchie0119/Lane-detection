# Lane Detection

This is a program that detects lane on a road-view video.

![test_image](https://github.com/Rietchie0119/Lane-detection/assets/28763133/bde25778-df6a-4fb0-8988-9f5c13cb7c91)

This program splits the video into frames and analyzes each frame to detect the lane lines. Following is the process I used to detect lines in the image.

![gray](https://github.com/Rietchie0119/Lane-detection/assets/28763133/d98a7dd3-7316-4cf2-aa50-76a5721a98dd)

1. Use cvtColor function to convert the image in grayscale. This process reduces the complexity and computation.

![blur](https://github.com/Rietchie0119/Lane-detection/assets/28763133/91e8e9bc-ade0-47da-ac1d-2adbdb76da37)

2. Apply Gaussian Blur to reduce noise.

![canny](https://github.com/Rietchie0119/Lane-detection/assets/28763133/892c6231-d08e-4936-9449-1ff5996d8d85)

3. Use canny edge detection
