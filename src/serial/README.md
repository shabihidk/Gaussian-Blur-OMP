# Serial Image Filters - Build Instructions

## Compile

### Windows (MinGW/MSYS2)
```bash
gcc -O3 -Wall -o filter main.c filters.c image_utils.c -lm
```

### Linux/macOS
```bash
gcc -O3 -Wall -o filter main.c filters.c image_utils.c -lm
```

## Usage

```bash
./filter <input> <output> <filter>
```

### Filters Available
- `gaussian` - Gaussian Blur (5×5 kernel)
- `sharpen` - Sharpen Filter (3×3 kernel)
- `sobel` - Sobel Edge Detector (3×3 kernel)

### Examples

```bash
# Gaussian Blur
./filter ../../images/input/test.png ../../images/output/blurred.png gaussian

# Sharpen
./filter ../../images/input/test.png ../../images/output/sharp.png sharpen

# Sobel Edge Detection
./filter ../../images/input/test.png ../../images/output/edges.png sobel
```

## Notes

- All images are processed in RGB format
- Output is saved as PNG
- Execution time is displayed in milliseconds
- Place test images in `images/input/`
