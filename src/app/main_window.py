from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget
from .filter_tab import FilterTab
from .results_tab import ResultsTab
from .testing_tab import TestingTab
from .styles import APP_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle('Parallel Image Filter')
        self.setGeometry(100, 100, 1400, 850)
        self.setStyleSheet(APP_STYLE)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(10, 10, 10, 10)
        
        tabs = QTabWidget()
        tabs.setStyleSheet('QTabBar::tab { padding: 10px 20px; font-size: 13px; }')
        
        self.filter_tab = FilterTab()
        tabs.addTab(self.filter_tab, 'Filter')
        
        tabs.addTab(ResultsTab(), 'Results')
        tabs.addTab(TestingTab(), 'Testing')
        
        layout.addWidget(tabs)
