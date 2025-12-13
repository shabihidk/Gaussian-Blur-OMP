#ifndef IMAGE_UTILS_H
#define IMAGE_UTILS_H

typedef struct {
    unsigned char* data;
    int width;
    int height;
    int channels;
} Image;

Image* load_image(const char* filename);
int save_image(const char* filename, Image* img);
void free_image(Image* img);
Image* create_image(int width, int height, int channels);

#endif
