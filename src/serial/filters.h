#ifndef FILTERS_H
#define FILTERS_H

#include "image_utils.h"

// Apply Gaussian Blur filter (5x5 kernel)
Image* apply_gaussian_blur(Image* img);

// Apply Sharpen filter (3x3 kernel)
Image* apply_sharpen(Image* img);

// Apply Sobel Edge Detector (3x3 kernel)
Image* apply_sobel(Image* img);

#endif // FILTERS_H
