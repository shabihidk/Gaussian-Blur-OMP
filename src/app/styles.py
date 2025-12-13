APP_STYLE = """
    QMainWindow, QWidget {
        background: #1e1e1e;
        color: #e0e0e0;
        font-family: 'Segoe UI', Arial;
        font-size: 12px;
    }
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #0078d4, stop:1 #005a9e);
        color: white;
        border: 1px solid #0066b8;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #106ebe, stop:1 #0078d4);
        border: 1px solid #0078d4;
    }
    QPushButton:pressed {
        background: #005a9e;
    }
    QPushButton:disabled {
        background: #444;
        color: #888;
        border: 1px solid #555;
    }
    QComboBox {
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 3px;
        padding: 6px;
    }
    QProgressBar {
        background: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 3px;
        text-align: center;
        height: 18px;
    }
    QProgressBar::chunk {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
            stop:0 #0078d4, stop:1 #00bcf2);
    }
"""

SERIAL_BASELINE = 116.0
IMAGE_SIZE = (700, 320)
MAX_CPU_BARS = 6
