# Lane Detection

This is a program that detects lane on a road-view video.

![test_image](https://github.com/Rietchie0119/Lane-detection/assets/28763133/bde25778-df6a-4fb0-8988-9f5c13cb7c91)

This program splits the video into frames and analyzes each frame to detect the lane lines. Following is the process I used to detect lines in the image.

![gray](https://github.com/Rietchie0119/Lane-detection/assets/28763133/b3acbef1-aa1a-4ce4-8a08-d1996e6ba690)

1. Use cvtColor function to convert the image in grayscale. This process reduces the complexity and computation.

![blur](https://github.com/Rietchie0119/Lane-detection/assets/28763133/9791f37b-6504-401a-8651-230896c395de)

2. Apply Gaussian Blur to reduce noise.

![canny](https://github.com/Rietchie0119/Lane-detection/assets/28763133/892c6231-d08e-4936-9449-1ff5996d8d85)

3. Use canny edge detection

![cropped](https://github.com/Rietchie0119/Lane-detection/assets/28763133/59095cdb-3df5-4c75-a177-fd5259109367)
4. Extract the region of interest using bitwise operation.

![](https://miro.medium.com/v2/resize:fit:1400/1*Cr73Mte5NNgO16D4moKDQg.png)
5. Convert white pixel into sinusoidal curve in hough space. The bin that contains intersections more than threshold corresponds rho, theta value of a line in catesian space.

![linedetec](https://github.com/Rietchie0119/Lane-detection/assets/28763133/a6a7003f-a59d-4276-868c-764387c370cb)
6. Show detected lines in each frame.
