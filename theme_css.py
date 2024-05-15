dark_theme = """
    QWidget {
        background-color: #333333;
        color: #ffffff;
        border: none;
    }
    QPushButton {
        background-color: #4d4d4d;
        border: 1px solid #4d4d4d;
        border-radius: 4px;
        color: #ffffff;
        padding: 5px;
    }
    QPushButton:hover {
        background-color: #5a5a5a;
        border: 1px solid #5a5a5a;
    }
    QCheckBox {
        color: #ffffff;
    }
    QLineEdit {
        background-color: #4d4d4d;
        border: 1px solid #4d4d4d;
        color: #ffffff;
        padding: 5px;
    }
    QTextEdit {
        background-color: #4d4d4d;
        border: 1px solid #4d4d4d;
        color: #ffffff;
        padding: 5px;
    }
    QProgressBar {
        border: 1px solid #444444;
        border-radius: 7px;
        background-color: #2e2e2e;
        text-align: center;
        font-size: 10pt;
        color: white;
    }
    QProgressBar::chunk {
        background-color: #3a3a3a;
        width: 5px;
    }
    QScrollBar:vertical {
        border: none;
        background-color: #3a3a3a;
        width: 10px;
        margin: 16px 0 16px 0;
    }
    QScrollBar::handle:vertical {
        background-color: #444444;
        border-radius: 5px;
    }
    QScrollBar:horizontal {
        border: none;
        background-color: #3a3a3a;
        height: 10px;
        margin: 0px 16px 0 16px;
    }
    QScrollBar::handle:horizontal {
        background-color: #444444;
        border-radius: 5px;
    }
    QTabWidget {
        background-color: #2e2e2e;
        border: none;
    }
    QTabBar::tab {
        background-color: #2e2e2e;
        color: #b1b1b1;
        padding: 8px 20px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
        border: none;
    }
 
    QTabBar::tab:selected, QTabBar::tab:hover {
        background-color: #3a3a3a;
        color: white;
    }
    
    QTableCornerButton::section {
        background-color:#2e2e2e;
    }

    QHeaderView::section {
    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                      stop:0 #616161, stop: 0.5 #505050,
                                      stop: 0.6 #434343, stop:1 #656565);
    color: white;
    padding-left: 4px;
    border: 1px solid #6c6c6c;
    }

    QHeaderView::section:checked
    {
        background-color: red;
    }

    QMdiSubWindow
    {
        border-radius: 7px;
        border: 1px solid #aaaaaa;
    }

    

"""