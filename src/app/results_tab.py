from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class ResultsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title = QLabel('Performance Results Viewer')
        title.setStyleSheet('font-size: 18px; font-weight: bold; color: #0078d4;')
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        for text, path in [('Load Execution Time Graph', 'results/graphs/execution_time.png'),
                          ('Load Speedup/Efficiency Graph', 'results/graphs/speedup_efficiency.png')]:
            btn = QPushButton(text)
            btn.setMinimumHeight(40)
            btn.clicked.connect(lambda checked, p=path: self.load_image(p))
            btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)
        
        self.display = QLabel('Load a graph to view results')
        self.display.setStyleSheet('border: 2px solid #3d3d3d; background: #0a0a0a; border-radius: 3px;')
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setMinimumHeight(600)
        
        scroll = QScrollArea()
        scroll.setWidget(self.display)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
    
    def load_image(self, path):
        try:
            pixmap = QPixmap(path)
            if pixmap.isNull():
                self.display.setText(f'Error: Could not load {path}\n\nRun tests first.')
            else:
                self.display.setPixmap(pixmap.scaled(1200, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            self.display.setText(f'Error: {str(e)}')
