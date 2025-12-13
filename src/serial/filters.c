#include "filters.h"
#include <math.h>
#include <stdlib.h>

static inline unsigned char clamp(int val) {
    return (val < 0) ? 0 : (val > 255) ? 255 : val;
}

Image* apply_gaussian_blur(Image* img) {
    if (!img || !img->data) return NULL;
    
    float kernel[5][5] = {
        {1/273.0f,  4/273.0f,  7/273.0f,  4/273.0f, 1/273.0f},
        {4/273.0f, 16/273.0f, 26/273.0f, 16/273.0f, 4/273.0f},
        {7/273.0f, 26/273.0f, 41/273.0f, 26/273.0f, 7/273.0f},
        {4/273.0f, 16/273.0f, 26/273.0f, 16/273.0f, 4/273.0f},
        {1/273.0f,  4/273.0f,  7/273.0f,  4/273.0f, 1/273.0f}
    };
    
    Image* output = create_image(img->width, img->height, img->channels);
    if (!output) return NULL;
    
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            for (int c = 0; c < img->channels; c++) {
                float sum = 0.0f;
                
                for (int ky = -2; ky <= 2; ky++) {
                    for (int kx = -2; kx <= 2; kx++) {
                        int px = (x + kx < 0) ? 0 : (x + kx >= img->width) ? img->width - 1 : x + kx;
                        int py = (y + ky < 0) ? 0 : (y + ky >= img->height) ? img->height - 1 : y + ky;
                        
                        sum += img->data[(py * img->width + px) * img->channels + c] * kernel[ky + 2][kx + 2];
                    }
                }
                
                output->data[(y * img->width + x) * img->channels + c] = clamp((int)(sum + 0.5f));
            }
        }
    }
    
    return output;
}

Image* apply_sharpen(Image* img) {
    if (!img || !img->data) return NULL;
    
    float kernel[3][3] = {{ 0, -1,  0}, {-1,  5, -1}, { 0, -1,  0}};
    
    Image* output = create_image(img->width, img->height, img->channels);
    if (!output) return NULL;
    
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            for (int c = 0; c < img->channels; c++) {
                float sum = 0.0f;
                
                for (int ky = -1; ky <= 1; ky++) {
                    for (int kx = -1; kx <= 1; kx++) {
                        int px = (x + kx < 0) ? 0 : (x + kx >= img->width) ? img->width - 1 : x + kx;
                        int py = (y + ky < 0) ? 0 : (y + ky >= img->height) ? img->height - 1 : y + ky;
                        
                        sum += img->data[(py * img->width + px) * img->channels + c] * kernel[ky + 1][kx + 1];
                    }
                }
                
                output->data[(y * img->width + x) * img->channels + c] = clamp((int)(sum + 0.5f));
            }
        }
    }
    
    return output;
}

Image* apply_sobel(Image* img) {
    if (!img || !img->data) return NULL;
    
    float gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    float gy[3][3] = {{-1, -2, -1}, { 0, 0, 0}, { 1, 2, 1}};
    
    Image* output = create_image(img->width, img->height, img->channels);
    if (!output) return NULL;
    
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            for (int c = 0; c < img->channels; c++) {
                float sum_x = 0.0f, sum_y = 0.0f;
                
                for (int ky = -1; ky <= 1; ky++) {
                    for (int kx = -1; kx <= 1; kx++) {
                        int px = (x + kx < 0) ? 0 : (x + kx >= img->width) ? img->width - 1 : x + kx;
                        int py = (y + ky < 0) ? 0 : (y + ky >= img->height) ? img->height - 1 : y + ky;
                        
                        unsigned char val = img->data[(py * img->width + px) * img->channels + c];
                        sum_x += val * gx[ky + 1][kx + 1];
                        sum_y += val * gy[ky + 1][kx + 1];
                    }
                }
                
                output->data[(y * img->width + x) * img->channels + c] = clamp((int)(sqrtf(sum_x * sum_x + sum_y * sum_y) + 0.5f));
            }
        }
    }
    
    return output;
}
