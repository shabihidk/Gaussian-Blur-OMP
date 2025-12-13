#ifndef IMAGE_UTILS_H
#define IMAGE_UTILS_H

typedef struct {
    unsigned char* data;
    int width;
    int height;
    int channels;
} Image;

// Load image from file
Image* load_image(const char* filename);

// Save image to file
int save_image(const char* filename, Image* img);

// Free image memory
void free_image(Image* img);

// Create a new image
Image* create_image(int width, int height, int channels);

#endif // IMAGE_UTILS_H
