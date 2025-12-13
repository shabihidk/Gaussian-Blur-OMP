import psutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from .workers import ProcessWorker
from .styles import SERIAL_BASELINE, IMAGE_SIZE, MAX_CPU_BARS

class FilterTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.input_image = None
        self.output_image = 'images/output/gui_output.png'
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setSpacing(15)
        layout.addWidget(self.create_control_panel(), 1)
        layout.addWidget(self.create_image_panel(), 2)
        
    def create_control_panel(self):
        panel = QWidget()
        panel.setStyleSheet('background: #252526; border-radius: 6px;')
        panel.setMaximumWidth(350)
        layout = QVBoxLayout(panel)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        layout.addWidget(self.create_label('Controls', 18, '#0078d4'))
        
        load_btn = self.create_button('Load Image', self.load_image, 40)
        layout.addWidget(load_btn)
        
        self.image_label = QLabel('No image loaded')
        self.image_label.setStyleSheet('color: #888; padding: 8px; background: #1e1e1e; border-radius: 3px;')
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)
        
        self.add_separator(layout)
        
        for label, widget in [('Filter:', self.create_combo(['gaussian', 'sharpen', 'sobel'])),
                             ('Threads:', self.create_thread_slider()),
                             ('Scheduling:', self.create_combo(['static', 'dynamic', 'guided']))]:
            layout.addWidget(QLabel(label))
            layout.addWidget(widget)
        
        self.process_btn = self.create_button('Apply Filter', self.process_image, 45)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        self.add_separator(layout)
        layout.addWidget(self.create_label('Performance', 15))
        
        perf_scroll = QScrollArea()
        perf_scroll.setWidgetResizable(True)
        perf_scroll.setStyleSheet('QScrollArea { border: none; background: transparent; }')
        perf_scroll.setMaximumHeight(120)
        
        self.perf_label = QLabel('Ready')
        self.perf_label.setStyleSheet('padding: 10px; background: #1e1e1e; border-radius: 3px;')
        self.perf_label.setWordWrap(True)
        perf_scroll.setWidget(self.perf_label)
        layout.addWidget(perf_scroll)
        
        layout.addStretch()
        return panel
    
    def create_combo(self, items):
        combo = QComboBox()
        combo.addItems(items)
        if items[0] == 'static':
            self.schedule_combo = combo
        elif items[0] == 'gaussian':
            self.filter_combo = combo
        return combo
    
    def create_thread_slider(self):
        self.thread_slider = QSlider(Qt.Horizontal)
        self.thread_slider.setRange(1, 16)
        self.thread_slider.setValue(4)
        self.thread_slider.setTickPosition(QSlider.TicksBelow)
        self.thread_slider.valueChanged.connect(self.update_thread_label)
        
        self.thread_label = QLabel('4 threads')
        self.thread_label.setStyleSheet('color: #00bcf2; font-weight: bold;')
        
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.thread_slider)
        layout.addWidget(self.thread_label)
        return widget
    
    def create_image_panel(self):
        panel = QWidget()
        panel.setStyleSheet('background: #252526; border-radius: 6px;')
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        for title, attr in [('Original', 'input_display'), ('Filtered', 'output_display')]:
            widget = QWidget()
            widget.setStyleSheet('background: #1e1e1e; border-radius: 4px; padding: 8px;')
            w_layout = QVBoxLayout(widget)
            w_layout.setSpacing(6)
            w_layout.setContentsMargins(8, 8, 8, 8)
            
            w_layout.addWidget(self.create_label(title, 13, '#888'))
            
            display = QLabel('No image')
            display.setMinimumSize(*IMAGE_SIZE)
            display.setStyleSheet('border: 2px solid #3d3d3d; background: #0a0a0a; border-radius: 3px;')
            display.setAlignment(Qt.AlignCenter)
            w_layout.addWidget(display)
            
            setattr(self, attr, display)
            layout.addWidget(widget)
        
        return panel
    
    def create_label(self, text, size=12, color='#e0e0e0'):
        label = QLabel(text)
        label.setStyleSheet(f'font-size: {size}px; font-weight: bold; color: {color};')
        return label
    
    def create_button(self, text, callback, height=40):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        btn.setMinimumHeight(height)
        return btn
    
    def add_separator(self, layout):
        line = QLabel()
        line.setStyleSheet('background: #3d3d3d; max-height: 1px;')
        layout.addWidget(line)
    
    def update_thread_label(self):
        count = self.thread_slider.value()
        self.thread_label.setText(f'{count} thread{"s" if count > 1 else ""}')
    
    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg)')
        if file_path:
            self.input_image = file_path
            self.image_label.setText(file_path.replace('\\', '/').split('/')[-1])
            self.image_label.setStyleSheet('color: #00d084; padding: 8px; background: #1e1e1e; border-radius: 3px; font-weight: bold;')
            self.process_btn.setEnabled(True)
            self.input_display.setPixmap(QPixmap(file_path).scaled(*IMAGE_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.output_display.setText('No image')
    
    def process_image(self):
        if not self.input_image:
            return
        
        self.process_btn.setEnabled(False)
        self.process_btn.setText('Processing...')
        self.perf_label.setText('Processing...')
        
        self.worker = ProcessWorker(self.input_image, self.output_image, self.filter_combo.currentText(),
                                    self.thread_slider.value(), self.schedule_combo.currentText())
        self.worker.finished_signal.connect(self.on_processing_complete)
        self.worker.start()
    
    def on_processing_complete(self, result):
        self.process_btn.setEnabled(True)
        self.process_btn.setText('Apply Filter')
        
        if not result['success']:
            self.perf_label.setText('Processing failed')
            return
        
        threads = self.thread_slider.value()
        speedup = SERIAL_BASELINE / result['time'] if result['time'] > 0 else 0
        efficiency = (speedup / threads * 100) if threads > 1 else 100
        
        perf_text = f"<b style='color: #00d084'>Complete</b><br><br><b>Time:</b> {result['time']:.2f} ms<br>"
        if threads > 1:
            perf_text += f"<b>Speedup:</b> {speedup:.2f}x<br><b>Efficiency:</b> {efficiency:.1f}%"
        
        self.perf_label.setText(perf_text)
        self.output_display.setPixmap(QPixmap(self.output_image).scaled(*IMAGE_SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation))
