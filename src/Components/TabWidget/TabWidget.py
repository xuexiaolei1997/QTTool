import os
from PyQt5.QtWidgets import QTabWidget, QWidget


class TabWidget(QTabWidget):
    def __init__(self, parent=None, name="", tab_direc=QTabWidget.North):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.setObjectName(name)
        self.setTabPosition(tab_direc)

        qss_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'qss', 'style.qss')
        if os.path.exists(qss_file_path):
            with open(qss_file_path, 'r', encoding='utf8') as f:
                stylesheet = f.read()
            self.setStyleSheet(stylesheet)
    
    def close_tab(self, index):
        tab = self.widget(index)
        self.removeTab(index)
        tab.deleteLater()  # release reource after closed tab
    
