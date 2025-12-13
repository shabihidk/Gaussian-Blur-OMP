# Parallel Image Filters Using OpenMP

> **OpenMP-accelerated image filters with real-time thread monitoring**

**CS361L Project** | Muhammad Shabih Ul Hassan Raja (2023506) | Syed Ghazi Abbas (2023679)

📦 **Repository**: [github.com/shabihidk/Gaussian-Blur-OMP](https://github.com/shabihidk/Gaussian-Blur-OMP)

## What is This?

A parallel computing project that applies image filters using OpenMP. We're exploring how multi-threading speeds up image processing by implementing three filters:

1. **Gaussian Blur** - Smooths images
2. **Sharpen Filter** - Enhances edges  
3. **Sobel Edge Detector** - Detects edges

**Plus**: A clean Python GUI app with **task-manager-style live monitoring** - see each thread's progress in real-time!

## Project Structure

```
Parallel Image Filtering/
├── src/serial/         # Baseline C code
├── src/parallel/       # OpenMP parallelized code
├── src/app/           # Python GUI
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
cd src/app
pip install PyQt5 opencv-python pillow numpy matplotlib pandas psutil
python check_dependencies.py
```

## Run It

**Serial version:**
```bash
gcc -O3 -o filter main.c -lm
./filter input.png output.png gaussian
```

**Parallel version:**
```bash
gcc -O3 -fopenmp -o filter main.c -lm
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

🔗 **GitHub**: [shabihidk/Gaussian-Blur-OMP](https://github.com/shabihidk/Gaussian-Blur-OMP)
