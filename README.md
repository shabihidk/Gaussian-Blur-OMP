# Parallel Image Filters Using OpenMP

**CS361L Project** | Muhammad Shabih Ul Hassan Raja (2023506) | Syed Ghazi Abbas (2023679)

## What is This?

A parallel computing project that applies image filters using OpenMP. We're exploring how multi-threading speeds up image processing by implementing three filters:

1. **Gaussian Blur** - Smooths images
2. **Sharpen Filter** - Enhances edges  
3. **Sobel Edge Detector** - Detects edges

**Plus**: A clean Python GUI app for testing and visualization!

## Project Structure

```
Parallel Image Filtering/
├── src/parallel/       # OpenMP implementation (1 thread = serial)
├── src/app/           # Python GUI modules
├── images/            # Input/output images
├── results/           # Performance data & graphs
└── lib/               # stb_image library
```

## Quick Setup

### 1. C/OpenMP
- Install GCC with OpenMP: `gcc -fopenmp --version`
- Download [stb_image.h](https://github.com/nothings/stb) → place in `lib/`

### 2. Python GUI
```bash
pip install PyQt5 opencv-python pillow numpy matplotlib pandas psutil
```

## Run It

**Compile once:**
```bash
cd src/parallel
gcc -O3 -fopenmp -Wall -o filter.exe main.c filters.c image_utils.c -lm
```

**Run (1 thread = serial, >1 = parallel):**
```bash
./filter.exe input.jpg output.png gaussian 1 static    # Serial execution
./filter.exe input.jpg output.png gaussian 8 static    # Parallel with 8 threads
OMP_NUM_THREADS=8 ./filter input.png output.png gaussian
```

**GUI App:**
```bash
python src/app/main.py
```

## What We're Testing

- Thread counts: 1, 2, 4, 8, 16
- Scheduling: static, dynamic, guided
- Images: 1080p and 4K
- Metrics: Speedup ($S_p = T_1/T_p$), Efficiency ($E_p = S_p/p$)

## Development Phases

1. ✅ Setup & Docs
2. ⏳ Serial Implementation  
3. ⏳ Parallel Implementation
4. ⏳ Performance Analysis
5. ⏳ GUI Application
6. ⏳ Final Report

---

**CS361L** - Ghulam Ishaq Khan Institute | December 2025
