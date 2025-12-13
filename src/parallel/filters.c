#include "filters.h"
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <omp.h>

static inline unsigned char clamp(int val) {
    return (val < 0) ? 0 : (val > 255) ? 255 : val;
}

static inline int clamp_coord(int val, int max) {
    return (val < 0) ? 0 : (val >= max) ? max - 1 : val;
}

static void set_schedule(const char* schedule) {
    omp_sched_t sched = omp_sched_static;
    if (strcmp(schedule, "dynamic") == 0) sched = omp_sched_dynamic;
    else if (strcmp(schedule, "guided") == 0) sched = omp_sched_guided;
    omp_set_schedule(sched, 0);
}

static Image* apply_kernel(Image* img, float kernel[][5], int ksize, const char* schedule) {
    Image* output = create_image(img->width, img->height, img->channels);
    if (!output) return NULL;
    
    set_schedule(schedule);
    int half = ksize / 2;
    
    #pragma omp parallel for collapse(2) schedule(runtime)
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            for (int c = 0; c < img->channels; c++) {
                float sum = 0.0f;
                for (int ky = -half; ky <= half; ky++) {
                    for (int kx = -half; kx <= half; kx++) {
                        int px = clamp_coord(x + kx, img->width);
                        int py = clamp_coord(y + ky, img->height);
                        sum += img->data[(py * img->width + px) * img->channels + c] * kernel[ky + half][kx + half];
                    }
                }
                output->data[(y * img->width + x) * img->channels + c] = clamp((int)(sum + 0.5f));
            }
        }
    }
    return output;
}

Image* apply_gaussian_blur(Image* img, const char* schedule) {
    if (!img || !img->data) return NULL;
    float kernel[5][5] = {
        {1/273.0f,  4/273.0f,  7/273.0f,  4/273.0f, 1/273.0f},
        {4/273.0f, 16/273.0f, 26/273.0f, 16/273.0f, 4/273.0f},
        {7/273.0f, 26/273.0f, 41/273.0f, 26/273.0f, 7/273.0f},
        {4/273.0f, 16/273.0f, 26/273.0f, 16/273.0f, 4/273.0f},
        {1/273.0f,  4/273.0f,  7/273.0f,  4/273.0f, 1/273.0f}
    };
    return apply_kernel(img, kernel, 5, schedule);
}

Image* apply_sharpen(Image* img, const char* schedule) {
    if (!img || !img->data) return NULL;
    float kernel[5][5] = {{0,0,0,0,0},{0,0,-1,0,0},{0,-1,5,-1,0},{0,0,-1,0,0},{0,0,0,0,0}};
    return apply_kernel(img, kernel, 3, schedule);
}

Image* apply_sobel(Image* img, const char* schedule) {
    if (!img || !img->data) return NULL;
    
    float gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    float gy[3][3] = {{-1, -2, -1}, { 0, 0, 0}, { 1, 2, 1}};
    
    Image* output = create_image(img->width, img->height, img->channels);
    if (!output) return NULL;
    
    set_schedule(schedule);
    
    #pragma omp parallel for collapse(2) schedule(runtime)
    for (int y = 0; y < img->height; y++) {
        for (int x = 0; x < img->width; x++) {
            for (int c = 0; c < img->channels; c++) {
                float sum_x = 0.0f, sum_y = 0.0f;
                for (int ky = -1; ky <= 1; ky++) {
                    for (int kx = -1; kx <= 1; kx++) {
                        int px = clamp_coord(x + kx, img->width);
                        int py = clamp_coord(y + ky, img->height);
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
