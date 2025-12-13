#include <stdio.h>
#include <string.h>
#include <time.h>
#include "image_utils.h"
#include "filters.h"

void print_usage(const char* prog) {
    printf("Usage: %s <input> <output> <filter>\n", prog);
    printf("Filters: gaussian | sharpen | sobel\n");
}

int main(int argc, char** argv) {
    if (argc != 4) {
        print_usage(argv[0]);
        return 1;
    }
    
    printf("Input: %s\nFilter: %s\n", argv[1], argv[3]);
    
    Image* input = load_image(argv[1]);
    if (!input) return 1;
    
    Image* output = NULL;
    clock_t start = clock();
    
    if (strcmp(argv[3], "gaussian") == 0) output = apply_gaussian_blur(input);
    else if (strcmp(argv[3], "sharpen") == 0) output = apply_sharpen(input);
    else if (strcmp(argv[3], "sobel") == 0) output = apply_sobel(input);
    else {
        fprintf(stderr, "Unknown filter: %s\n", argv[3]);
        free_image(input);
        return 1;
    }
    
    if (!output) {
        free_image(input);
        return 1;
    }
    
    printf("Time: %.2f ms\n", ((double)(clock() - start)) / CLOCKS_PER_SEC * 1000.0);
    
    save_image(argv[2], output);
    free_image(input);
    free_image(output);
    
    return 0;
}
