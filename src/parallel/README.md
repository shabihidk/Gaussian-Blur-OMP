# Parallel Image Filters - OpenMP

## Compile

```bash
gcc -O3 -Wall -fopenmp -o filter.exe main.c filters.c image_utils.c -lm
```

## Usage

```bash
./filter.exe <input> <output> <filter> <threads> <schedule>
```

### Example

```bash
# Gaussian blur with 8 threads, static scheduling
./filter.exe ../../images/input/test.jpg ../../images/output/result.png gaussian 8 static

# Sobel with 4 threads, dynamic scheduling
./filter.exe ../../images/input/test.jpg ../../images/output/result.png sobel 4 dynamic

# Sharpen with 16 threads, guided scheduling
./filter.exe ../../images/input/test.jpg ../../images/output/result.png sharpen 16 guided
```

### Options

- **Filters**: `gaussian`, `sharpen`, `sobel`
- **Threads**: 1, 2, 4, 8, 16 (or any number)
- **Schedule**: `static`, `dynamic`, `guided`
