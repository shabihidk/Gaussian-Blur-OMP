import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys

# Ensure we're working from project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
os.chdir(project_root)

os.makedirs('results/graphs', exist_ok=True)

df = pd.read_csv('results/performance/results.csv')

serial_times = {}
for filter_name in df['filter'].unique():
    serial_time = df[(df['filter'] == filter_name) & (df['threads'] == 1)]['avg_time_ms'].values[0]
    serial_times[filter_name] = serial_time

df['speedup'] = df.apply(lambda row: serial_times[row['filter']] / row['avg_time_ms'], axis=1)
df['efficiency'] = (df['speedup'] / df['threads']) * 100

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

schedules = df['schedule'].unique()
colors = {'static': '#2E86AB', 'dynamic': '#A23B72', 'guided': '#F18F01'}
markers = {'static': 'o', 'dynamic': 's', 'guided': '^'}

for idx, filter_name in enumerate(df['filter'].unique()):
    ax_speedup = axes[0, idx]
    ax_efficiency = axes[1, idx]
    
    filter_df = df[df['filter'] == filter_name]
    
    for schedule in schedules:
        schedule_df = filter_df[filter_df['schedule'] == schedule]
        
        ax_speedup.plot(schedule_df['threads'], schedule_df['speedup'], 
                       marker=markers[schedule], color=colors[schedule], 
                       label=schedule, linewidth=2, markersize=8)
        
        ax_efficiency.plot(schedule_df['threads'], schedule_df['efficiency'], 
                          marker=markers[schedule], color=colors[schedule], 
                          label=schedule, linewidth=2, markersize=8)
    
    ax_speedup.plot(schedule_df['threads'], schedule_df['threads'], 
                   'k--', alpha=0.3, label='Linear')
    
    ax_speedup.set_title(f'{filter_name.capitalize()} - Speedup', fontsize=12, fontweight='bold')
    ax_speedup.set_xlabel('Threads')
    ax_speedup.set_ylabel('Speedup')
    ax_speedup.legend()
    ax_speedup.grid(True, alpha=0.3)
    
    ax_efficiency.set_title(f'{filter_name.capitalize()} - Efficiency', fontsize=12, fontweight='bold')
    ax_efficiency.set_xlabel('Threads')
    ax_efficiency.set_ylabel('Efficiency (%)')
    ax_efficiency.legend()
    ax_efficiency.grid(True, alpha=0.3)
    ax_efficiency.set_ylim([0, 100])

plt.tight_layout()
plt.savefig('results/graphs/speedup_efficiency.png', dpi=300)
print("Saved results/graphs/speedup_efficiency.png", flush=True)

fig, ax = plt.subplots(figsize=(10, 6))

for filter_name in df['filter'].unique():
    filter_df = df[(df['filter'] == filter_name) & (df['schedule'] == 'static')]
    ax.plot(filter_df['threads'], filter_df['avg_time_ms'], 
           marker='o', label=filter_name.capitalize(), linewidth=2, markersize=8)

ax.set_title('Execution Time vs Thread Count (Static Scheduling)', fontsize=14, fontweight='bold')
ax.set_xlabel('Threads')
ax.set_ylabel('Time (ms)')
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/graphs/execution_time.png', dpi=300)
print("Saved results/graphs/execution_time.png", flush=True)

summary = df.groupby(['filter', 'schedule'])['speedup'].max().reset_index()
summary.columns = ['Filter', 'Schedule', 'Max Speedup']
print("\nBest Speedup by Filter and Schedule:")
print(summary.to_string(index=False))
