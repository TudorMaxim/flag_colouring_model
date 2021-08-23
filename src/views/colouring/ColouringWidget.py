from typing import Tuple, List
from PyQt5.QtGui import QColor
import numpy as np
import pyqtgraph as pg
from math import cos, radians, sin
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from model.Graph import Graph
from utils.Constants import COLOURS
from utils.Helpers import Helpers

label_style = '''
    QLabel {
        font-weight: bold;
        font-size: 14px;
        color: grey;
    }
'''

large_label_style = '''
    QLabel {
        font-weight: bold;
        font-size: 16px;
        color: red;
    }
'''


class ColouringWidget(QWidget):
    def __init__(self, parent, colouring: dict[int, int], graph: Graph) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle('Coloured Conflict Graph')
        self.setStyleSheet("background-color: white;")

        self.colouring = colouring
        self.graph = graph
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setTitle('Coloured Conflict Graph')
        self.plot_widget.setBackground('w')
        self.plot_widget.getPlotItem().hideAxis('bottom')
        self.plot_widget.getPlotItem().hideAxis('left')

        self.used_colours_label = QLabel()
        self.used_colours_label.setStyleSheet(label_style)
        details_label = QLabel(text='Details:')
        details_label.setStyleSheet(large_label_style)
        vertices_label = QLabel(text='Each vertex of the graph represents a course.')
        vertices_label.setStyleSheet(label_style)
        edges_label = QLabel(text='An edge connects two courses that cannot be scheduled at the same time.')
        edges_label.setStyleSheet(label_style)

        layout = QVBoxLayout()
        layout.addWidget(self.plot_widget)
        layout.addWidget(details_label)
        layout.addWidget(vertices_label)
        layout.addWidget(edges_label)
        layout.addWidget(self.used_colours_label)
        self.setLayout(layout)
    
    def clear(self):
        self.plot_widget.clear()

    def draw(self, colouring: dict[int, int], graph: Graph):
        self.colouring = colouring
        self.graph = graph
        cnt = len(Helpers.get_used_colours(self.colouring))
        self.used_colours_label.setText(f'Number of used colours: {cnt}.')
        self.__draw_vertices()
        self.__draw_edges()
    
    def __draw_vertices(self) -> None:
        if self.colouring is None:
            return
        radius = len(self.colouring)
        points = self.__get_points(radius)
        scatter = pg.ScatterPlotItem(pxMode=False)
        coloured_points = []
        for _, x, y, colour in points:
            point = {
                'pos': (x, y),
                'size': 2, 
                'pen': {'color': 'w', 'width': 2},
                'brush': QColor(COLOURS[colour])
            }
            coloured_points.append(point)
        scatter.addPoints(coloured_points)
        self.plot_widget.addItem(scatter)

    def __draw_edges(self) -> None:
        if self.graph is None:
            return
        points = self.__get_points(radius=len(self.colouring))
        for p1, a, b, _ in points:
            for p2, x, y, _ in points:
                if p1 != p2 and self.graph.check_edge(p1, p2):
                    line = pg.LineSegmentROI([[a, b], [x, y]], pen='k')
                    self.plot_widget.addItem(line)
    
    def __get_points(self, radius) -> List[Tuple[int, float, float, int]]:
        points = []
        angles = np.linspace(0, 360, radius, endpoint=False)
        for angle in angles:
            theta = radians(angle)
            x = radius * cos(theta)
            y = radius * sin(theta)
            points.append((x, y))
        idx = 0
        for course in self.colouring:
            points[idx] = (course, points[idx][0], points[idx][1], self.colouring[course])
            idx += 1
        return points
