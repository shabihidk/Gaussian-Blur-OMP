#include "image_utils.h"
#include <stdio.h>
#include <stdlib.h>

#define STB_IMAGE_IMPLEMENTATION
#include "../../lib/stb_image.h"
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "../../lib/stb_image_write.h"

Image* load_image(const char* filename) {
    Image* img = malloc(sizeof(Image));
    if (!img) return NULL;
    
    img->data = stbi_load(filename, &img->width, &img->height, &img->channels, 0);
    if (!img->data) {
        free(img);
        return NULL;
    }
    
    printf("Loaded: %dx%d (%d channels)\n", img->width, img->height, img->channels);
    return img;
}

int save_image(const char* filename, Image* img) {
    if (!img || !img->data) return 0;
    return stbi_write_png(filename, img->width, img->height, img->channels, img->data, img->width * img->channels);
}

void free_image(Image* img) {
    if (img) {
        if (img->data) stbi_image_free(img->data);
        free(img);
    }
}

Image* create_image(int width, int height, int channels) {
    Image* img = malloc(sizeof(Image));
    if (!img) return NULL;
    
    img->width = width;
    img->height = height;
    img->channels = channels;
    img->data = calloc(width * height * channels, sizeof(unsigned char));
    
    if (!img->data) {
        free(img);
        return NULL;
    }
    
    return img;
}
