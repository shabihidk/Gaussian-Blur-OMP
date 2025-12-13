import subprocess
import time
from PyQt5.QtCore import QThread, pyqtSignal

class ProcessWorker(QThread):
    finished_signal = pyqtSignal(dict)
    
    def __init__(self, input_path, output_path, filter_name, threads, schedule):
        super().__init__()
        self.cmd = ['src/parallel/filter.exe', input_path, output_path, filter_name, str(threads), schedule]
        
    def run(self):
        start = time.time()
        result = subprocess.run(self.cmd, capture_output=True, text=True)
        exec_time = (time.time() - start) * 1000
        
        for line in result.stdout.split('\n'):
            if 'Time:' in line:
                exec_time = float(line.split(':')[1].strip().replace('ms', ''))
                break
        
        self.finished_signal.emit({'time': exec_time, 'output': result.stdout, 'success': result.returncode == 0})

class TestRunner(QThread):
    output_signal = pyqtSignal(str)
    
    def __init__(self, input_image=None):
        super().__init__()
        self.input_image = input_image
    
    def run(self):
        import sys
        import os
        
        # Set input image if provided
        if self.input_image:
            os.environ['TEST_IMAGE'] = self.input_image
        
        # Run tests with real-time output streaming
        process = subprocess.Popen(
            ['python', 'src/app/run_tests.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream stdout line by line
        for line in process.stdout:
            self.output_signal.emit(line.rstrip())
        
        # Wait for completion
        process.wait()
        
        # Get stderr if any
        stderr = process.stderr.read()
        if stderr:
            self.output_signal.emit(stderr)
        
        # Run visualization
        result = subprocess.run(['python', 'src/app/visualize_results.py'], capture_output=True, text=True)
        self.output_signal.emit('\n' + result.stdout)
