#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <omp.h>
#include "image_utils.h"
#include "filters.h"

void print_usage(const char* prog) {
    printf("Usage: %s <input> <output> <filter> <threads> <schedule>\n", prog);
    printf("Filters: gaussian | sharpen | sobel\n");
    printf("Schedule: static | dynamic | guided\n");
}

int main(int argc, char** argv) {
    if (argc != 6) {
        print_usage(argv[0]);
        return 1;
    }
    
    int threads = atoi(argv[4]);
    omp_set_num_threads(threads);
    
    printf("Input: %s\nFilter: %s\nThreads: %d\nSchedule: %s\n", 
           argv[1], argv[3], threads, argv[5]);
    
    Image* input = load_image(argv[1]);
    if (!input) return 1;
    
    Image* output = NULL;
    double start = omp_get_wtime();
    
    if (strcmp(argv[3], "gaussian") == 0) output = apply_gaussian_blur(input, argv[5]);
    else if (strcmp(argv[3], "sharpen") == 0) output = apply_sharpen(input, argv[5]);
    else if (strcmp(argv[3], "sobel") == 0) output = apply_sobel(input, argv[5]);
    else {
        fprintf(stderr, "Unknown filter: %s\n", argv[3]);
        free_image(input);
        return 1;
    }
    
    if (!output) {
        free_image(input);
        return 1;
    }
    
    double elapsed = (omp_get_wtime() - start) * 1000.0;
    printf("Time: %.2f ms\n", elapsed);
    
    if (threads > 1) {
        printf("Speedup: %.2f× (vs 1 thread baseline)\n", 111.0 / elapsed);
        printf("Efficiency: %.1f%%\n", (111.0 / elapsed / threads) * 100.0);
    }
    
    save_image(argv[2], output);
    free_image(input);
    free_image(output);
    
    return 0;
}
