from PyQt5.QtWidgets import *
from .workers import TestRunner

class TestingTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel('Automated Performance Testing')
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #0078d4;')
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        
        self.run_btn = QPushButton('Run All Tests')
        self.run_btn.setMinimumHeight(40)
        self.run_btn.clicked.connect(self.run_tests)
        btn_layout.addWidget(self.run_btn)
        
        load_btn = QPushButton('Load CSV Results')
        load_btn.setMinimumHeight(40)
        load_btn.clicked.connect(self.load_csv)
        btn_layout.addWidget(load_btn)
        layout.addLayout(btn_layout)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet('background: #0a0a0a; color: #00ff00; font-family: Consolas, monospace; border: 2px solid #3d3d3d; border-radius: 3px;')
        self.output.setText('Ready to run tests...\n\n3 filters × 5 thread counts × 3 scheduling policies × 3 iterations = 135 tests\n\nThis will take 2-3 minutes to complete.')
        layout.addWidget(self.output)
    
    def run_tests(self):
        self.run_btn.setEnabled(False)
        self.run_btn.setText('Running...')
        self.output.clear()
        self.output.append('Starting tests...\n')
        
        # Get input image from main window's filter tab if available
        input_image = None
        try:
            main_window = self.window()
            if hasattr(main_window, 'filter_tab') and hasattr(main_window.filter_tab, 'input_image'):
                input_image = main_window.filter_tab.input_image
                if input_image:
                    self.output.append(f'Using image: {input_image}\n')
        except:
            pass
        
        if not input_image:
            self.output.append('Warning: No image loaded. Using default test image.\n')
            input_image = 'images/input/test.jpg'
        
        self.worker = TestRunner(input_image)
        self.worker.output_signal.connect(self.output.append)
        self.worker.finished.connect(lambda: (self.output.append('\nTests complete!'),
                                             self.run_btn.setEnabled(True),
                                             self.run_btn.setText('Run All Tests')))
        self.worker.start()
    
    def load_csv(self):
        try:
            import pandas as pd
            df = pd.read_csv('results/performance/results.csv')
            output = f'Performance Test Results\n{"="*80}\n\n{df.to_string(index=False)}\n\n{"="*80}\nTotal: {len(df)} configurations'
            self.output.setText(output)
        except FileNotFoundError:
            self.output.setText('Error: results.csv not found.\n\nRun tests first.')
        except Exception as e:
            self.output.setText(f'Error: {str(e)}')
