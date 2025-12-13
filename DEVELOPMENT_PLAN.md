# Development Plan

Simple roadmap for the CS361L parallel image filters project.

---

## Phase 1: Setup ✅
- [x] Create project structure
- [x] Write README and docs
- [x] Set up requirements

---

## Phase 2: Serial Implementation ⏳

**Goal**: Working C code for all three filters (baseline for comparison)

### Tasks
- [ ] Download stb_image.h → place in `lib/`
- [ ] Write `image_utils.c` - load/save images
- [ ] Implement Gaussian Blur (5×5 kernel)
- [ ] Implement Sharpen Filter (3×3 kernel)  
- [ ] Implement Sobel Edge Detector
- [ ] Test with sample images
- [ ] Measure execution time

### Files to Create
```
src/serial/
├── main.c           # Entry point
├── filters.c        # Filter implementations
├── filters.h
├── image_utils.c    # Image I/O
└── image_utils.h
```

---

## Phase 3: Parallel Implementation ⏳

**Goal**: Speed up filters with OpenMP

### Tasks
- [ ] Add OpenMP pragmas to loops
- [ ] Test static scheduling
- [ ] Test dynamic scheduling
- [ ] Test guided scheduling
- [ ] Run with 1, 2, 4, 8, 16 threads
- [ ] Verify output matches serial

### Key Code
```c
#pragma omp parallel for collapse(2) schedule(static)
for (int y = 0; y < height; y++)
    for (int x = 0; x < width; x++)
        // process pixel
```

---

## Phase 4: Performance Analysis ⏳

**Goal**: Measure and visualize speedup

### Tasks
- [ ] Run all configurations (5 iterations each)
- [ ] Save results to CSV
- [ ] Calculate speedup: $S_p = T_1 / T_p$
- [ ] Calculate efficiency: $E_p = S_p / p$
- [ ] Generate graphs with Python

### Graphs to Make
- Speedup vs threads
- Efficiency vs threads  
- Scheduling policy comparison

---

## Phase 5: GUI Application ⏳

**Goal**: Clean Python app with live visualization

### Tasks
- [ ] Design simple UI layout
- [ ] Add image upload button
- [ ] Add camera capture
- [ ] Show live processing
- [ ] Add overall progress bar with timer
- [ ] Create task-manager-style report panel:
  - [ ] Live thread monitor table
  - [ ] Per-thread progress bars
  - [ ] CPU/Memory usage display
  - [ ] Real-time updates (50-100ms refresh)
- [ ] Connect to C backend

### UI Layout
```
┌──────────────────────────────────────────────┐
│  [📸 Capture] [📁 Upload] [Filter ▼] [Threads ▼] │
├────────────────────┬─────────────────────────┤
│                    │ ⚡ PROCESS MONITOR      │
│                    │ ┌───────────────────────┐│
│   Live Preview     │ │ Filter: Gaussian Blur ││
│                    │ │ Image: 1920x1080      ││
│   [Processing      │ │ Threads: 8 active     ││
│    Image Here]     │ ├───────────────────────┤│
│                    │ │ Thread │ Status │ Px  ││
│                    │ │   0    │ ████░░ │ 45% ││
│                    │ │   1    │ █████░ │ 52% ││
│                    │ │   2    │ ███░░░ │ 38% ││
│                    │ │   3    │ ████░░ │ 41% ││
│                    │ │   4    │ █████░ │ 56% ││
│                    │ │   5    │ ███░░░ │ 35% ││
│                    │ │   6    │ ████░░ │ 48% ││
│                    │ │   7    │ ████░░ │ 43% ││
│                    │ ├───────────────────────┤│
│                    │ │ CPU: 87% │ Mem: 234MB ││
│                    │ └───────────────────────┘│
├────────────────────┴─────────────────────────┤
│ Overall Progress: [████████░░] 82%   ETA: 1.8s │
└──────────────────────────────────────────────┘
```

**Task Manager-Style Report Panel:**
- Live thread status (like Windows Task Manager processes)
- Individual thread progress bars
- Real-time CPU and memory usage
- Active thread count
- Per-thread completion percentage
- Updates every 50-100ms for smooth monitoring

### Tech Stack
- PyQt5 (GUI + QTableWidget for thread monitor)
- OpenCV (camera + images)
- subprocess (run C code)
- psutil (CPU/memory monitoring)

---

## Phase 6: Final Report ⏳

**Goal**: Document everything

### Tasks
- [ ] Write project report
- [ ] Present results with graphs
- [ ] Discuss bottlenecks
- [ ] Create presentation slides
- [ ] Record demo video
- [ ] Clean up code

---

## Timeline

| Week | Phase | Focus |
|------|-------|-------|
| 1 | 1 | Setup |
| 2 | 2 | Serial code |
| 3 | 3 | OpenMP |
| 4 | 4 | Analysis |
| 5-6 | 5 | GUI app |
| 7 | 6 | Report |

---

**Keep it simple. Make it work. Make it fast.**
