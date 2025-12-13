import subprocess
import csv
import time
import os
import sys

# Ensure we're working from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(project_root)

filters = ['gaussian', 'sharpen', 'sobel']
threads = [1, 2, 4, 8, 16]
schedules = ['static', 'dynamic', 'guided']
iterations = 3  # Reduced from 5 for faster testing

input_image = os.environ.get('TEST_IMAGE', 'images/input/test.jpg')
output_image = 'images/output/temp.png'

results = []

print("Starting performance tests...", flush=True)
print(f"Filters: {len(filters)}, Threads: {len(threads)}, Schedules: {len(schedules)}, Iterations: {iterations}", flush=True)
print(f"Total tests: {len(filters) * len(threads) * len(schedules) * iterations}\n", flush=True)

for filter_name in filters:
    for thread_count in threads:
        for schedule in schedules:
            times = []
            print(f"Testing {filter_name} with {thread_count} threads ({schedule})...", end=' ', flush=True)
            
            for i in range(iterations):
                cmd = [
                    'src/parallel/filter.exe',
                    input_image,
                    output_image,
                    filter_name,
                    str(thread_count),
                    schedule
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                
                if result.returncode != 0:
                    print(f"\nError running test: {result.stderr}", flush=True)
                    continue
                
                for line in result.stdout.split('\n'):
                    if 'Time:' in line:
                        time_ms = float(line.split(':')[1].strip().replace('ms', ''))
                        times.append(time_ms)
                        break
            
            avg_time = sum(times) / len(times)
            print(f"{avg_time:.2f} ms", flush=True)
            
            results.append({
                'filter': filter_name,
                'threads': thread_count,
                'schedule': schedule,
                'avg_time_ms': avg_time,
                'min_time_ms': min(times),
                'max_time_ms': max(times)
            })

with open('results/performance/results.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['filter', 'threads', 'schedule', 'avg_time_ms', 'min_time_ms', 'max_time_ms'])
    writer.writeheader()
    writer.writerows(results)

print("\nResults saved to results/performance/results.csv", flush=True)
