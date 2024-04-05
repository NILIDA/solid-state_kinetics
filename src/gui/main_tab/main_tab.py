from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSplitter, QVBoxLayout, QWidget

from ..console_widget import ConsoleWidget
from .plot_canvas import PlotCanvas
from .side_bar import SideBar
from .sub_side_bar import SubSideBar


class MainTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.splitter = QSplitter(Qt.Orientation.Horizontal, self)
        self.layout.addWidget(self.splitter)

        self.sidebar = SideBar(self)
        self.splitter.addWidget(self.sidebar)

        self.sub_sidebar = SubSideBar(self)
        self.sub_sidebar.hide()
        self.splitter.addWidget(self.sub_sidebar)

        self.plot_canvas = PlotCanvas(self)
        self.splitter.addWidget(self.plot_canvas)

        self.console_widget = ConsoleWidget(self)
        self.splitter.addWidget(self.console_widget)

        self.sidebar.sub_side_bar_needed.connect(self.toggle_sub_sidebar)

    def initialize_sizes(self):
        total_width = self.width()
        sidebar_width = int(total_width / 5)
        console_width = int(total_width / 5)

        if self.sub_sidebar.isVisible():
            sub_sidebar_width = int(total_width / 6)
            canvas_width = int(total_width - sidebar_width - sub_sidebar_width - console_width)
            self.splitter.setSizes([sidebar_width, sub_sidebar_width, canvas_width, console_width])
        else:
            canvas_width = int(total_width - sidebar_width - console_width)
            self.splitter.setSizes([sidebar_width, 0, canvas_width, console_width])

    def showEvent(self, event):
        super().showEvent(event)
        self.initialize_sizes()

    def toggle_sub_sidebar(self, content_type):
        if content_type:
            if content_type in self.sidebar.get_experiment_files_list():
                self.sub_sidebar.update_content("Эксперимент")
            else:
                self.sub_sidebar.update_content(content_type)
                self.sub_sidebar.setVisible(True)
        else:
            self.sub_sidebar.setVisible(False)
        self.initialize_sizes()
