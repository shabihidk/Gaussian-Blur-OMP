#ifndef FILTERS_H
#define FILTERS_H

#include "image_utils.h"

Image* apply_gaussian_blur(Image* img, const char* schedule);
Image* apply_sharpen(Image* img, const char* schedule);
Image* apply_sobel(Image* img, const char* schedule);

#endif
