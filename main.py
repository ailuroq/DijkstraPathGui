import sys
from math import sqrt
from random import randint

import matplotlib.pyplot as plt
import networkx as nx
import numpy
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, QSizePolicy, \
    QPushButton, QFileDialog, QGridLayout, QInputDialog, QMessageBox, QTextEdit, QLabel, QTableWidget, QLineEdit, \
    QTableWidgetItem, QTextBrowser
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from pip._vendor.msgpack.fallback import xrange


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.title = 'test'
        self.left = 0
        self.top = 0
        self.width = 1920
        self.height = 1080
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('Ready')

        widget = QWidget(self)
        self.setCentralWidget(widget)
        vlay = QVBoxLayout(widget)
        hlay = QHBoxLayout()
        vlay.addLayout(hlay)

        m = WidgetPlot(self)
        vlay.addWidget(m)


class WidgetPlot(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setLayout(QGridLayout())
        self.canvas = PlotCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.pybutton = QPushButton('Задать граф', self)
        # self.pybutton_2 = QPushButton('Добавить вершину', self)
        # self.pybutton_3 = QPushButton('Соединить вершины', self)
        self.pybutton_4 = QPushButton('Алгоритм Дейкстры', self)
        font = QFont()
        font.setPointSize(11)
        self.pybutton.setFont(font)
        # self.pybutton_2.setFont(font)
        # self.pybutton_3.setFont(font)
        self.pybutton_4.setFont(font)
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.pybutton, 0, 1, 1, 1)
        # self.layout().addWidget(self.pybutton_2, 0, 2, 1, 1)
        # self.layout().addWidget(self.pybutton_3, 0, 3, 1, 1)
        self.layout().addWidget(self.pybutton_4, 0, 2, 1, 1)
        self.layout().addWidget(self.toolbar, 1, 1, 1, 4)
        self.layout().addWidget(self.canvas, 2, 1, 4, 4)
        # self.layout().addWidget(self.textEdit, 20, 1, 4, 4)
        self.pybutton.clicked.connect(self.show_choose_dialog)
        # self.pybutton_2.clicked.connect(self.canvas.add_nodes)
        self.pybutton_4.clicked.connect(lambda: self.show_dijkstra_dialog(self.textEdit))
        # self.pybutton_3.clicked.connect(self.show_nodes_dialog)

    def show_choose_dialog(self):
        items = ("Неориентированный граф", "Ориентированный граф")
        item, ok = QInputDialog.getItem(self, "Вид графа", "Выберите вид графа", items, 0, False)
        if ok and item:
            if item == "Неориентированный граф":
                self.canvas.read_graph_from_file(False)
            else:
                self.canvas.read_graph_from_file(True)

    def show_nodes_dialog(self):
        if self.canvas.graph is None:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Graph error")
            error_dialog.setText("Сначала нужно задать граф")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()
        else:
            first_node = self.get_int()
            second_node = self.get_int()
            weight = self.get_weight()
            if (first_node is not False or second_node is not False or weight is not False):
                self.canvas.link_nodes(first_node, second_node, weight)
            else:
                pass

    def show_dijkstra_dialog(self, model):
        if self.canvas.graph is None:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Graph error")
            error_dialog.setText("Сначала нужно задать граф")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()
        else:
            first_node = self.get_int()
            second_node = self.get_int()
            if (first_node is not False or second_node is not False):
                self.canvas.dijkstra1(first_node, second_node, model)
            else:
                pass

    def get_int(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer", "Введите вершину", 0, 0,
                                           self.canvas.graph.number_of_nodes() - 1, 1)
        if okPressed:
            return i
        else:
            return False

    def get_weight(self):
        i, okPressed = QInputDialog.getInt(self, "Get integer", "Введите вес ребра", 1)
        if okPressed:
            return i
        else:
            return False


class AnotherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 0
        self.width = 1320
        self.height = 980
        self.flag = False
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.pushButton = QPushButton('Построить граф с данной матрицы', self)
        self.pushButton.setGeometry(QRect(10, 20, 361, 41))
        font = QFont()
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton('Выбрать граф с файла', self)
        self.pushButton_2.setGeometry(QRect(390, 20, 201, 41))
        font = QFont()
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QRect(10, 80, 1301, 861))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setGeometry(QRect(730, 20, 101, 31))
        font = QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.label = QLabel('Кол-во строк и столбцов', self)
        self.label.setGeometry(QRect(610, 20, 111, 31))
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton_3 = QPushButton('Принять', self)
        self.pushButton_3.setGeometry(QRect(850, 20, 191, 31))
        font = QFont()
        font.setPointSize(11)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.rows = 0
        self.matrix_data = []
        self.pushButton_3.clicked.connect(self.apply_rows)
        self.pushButton.clicked.connect(self.build_plot)
        self.pushButton_2.clicked.connect(self.read_graph_from_file)

    def apply_rows(self):
        test_rows = self.lineEdit.text()
        if test_rows.isdigit():
            self.rows = int(self.lineEdit.text())

            self.tableWidget.setColumnCount(self.rows)
            self.tableWidget.setRowCount(self.rows)
            self.set_default_values()
        else:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Input error")
            error_dialog.setText("Размер матрицы должен быть числом")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()

    def set_default_values(self):
        for i in range(0, self.rows):
            for j in range(0, self.rows):
                self.tableWidget.setItem(i, j, QTableWidgetItem("0"))

    def read_data_from_table(self):
        for row in range(self.rows):
            tmp = []
            for col in range(self.rows):
                try:
                    if not self.tableWidget.item(row, col).text().isdigit():
                        return False
                    tmp.append(self.tableWidget.item(row, col).text())
                except:
                    tmp.append(0)
            self.matrix_data.append(tmp)
        for i in self.matrix_data: print(i)

    def read_graph_from_file(self):
        try:
            file_name = QFileDialog.getOpenFileName()
            path = file_name[0]
            self.matrix_data = numpy.loadtxt(path, unpack=True)
            self.rows = int(sqrt(self.matrix_data.size))
            self.matrix_data = self.matrix_data.tolist()
            self.tableWidget.setColumnCount(self.rows)
            self.tableWidget.setRowCount(self.rows)
            labels = []
            for i in range(self.rows):
                labels.append(str(i))
            self.tableWidget.setHorizontalHeaderLabels(labels)
            self.tableWidget.setVerticalHeaderLabels(labels)
            for i in range(self.rows):
                for j in range(self.rows):
                    self.matrix_data[i][j] = str(int(self.matrix_data[i][j]))
            print(self.matrix_data)
            for i in range(0, self.rows):
                for j in range(0, self.rows):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(self.matrix_data[i][j])))
            self.write_to_temp_file()
        except:
            pass

    def build_plot(self):
        self.matrix_data = []
        self.read_data_from_table()
        self.write_to_temp_file()

    def write_to_temp_file(self):
        try:
            if self.rows != 0:
                flag = self.read_data_from_table()
                if flag is not False:

                    temp_file = open('temp.txt', 'w')
                    for i in range(self.rows):
                        for j in range(self.rows):
                            temp_file.write(self.matrix_data[i][j] + ' ')
                        temp_file.write('\n')

                    self.flag = True
                else:
                    error_dialog = QMessageBox()
                    error_dialog.setWindowTitle("Input error")
                    error_dialog.setText("В таблицу можно вводить только цифры")
                    error_dialog.setIcon(QMessageBox.Critical)
                    error_dialog.exec_()
            else:
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Input error")
                error_dialog.setText("Сначала нужно задать таблицу")
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.exec_()
        except:
            pass


class PlotCanvas(FigureCanvas):
    matrix = None
    graph = None
    booleanGraph = None
    path = None
    all_paths = []
    file = open('output.txt', 'w')

    def __init__(self):
        figure = plt.figure()
        FigureCanvas.__init__(self, figure)
        self.setParent(None)
        self.w = AnotherWindow()
        self.wind = OutputWindow()
        self.weight = 0
        self.new_all_paths=[]
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def read_graph_from_file(self, booleanGraph):
        try:
            self.w.show()
            self.w.pushButton.clicked.connect(lambda: self.help_func(booleanGraph))

        except:
            pass

    def help_func(self, booleanGraph):
        flag = self.w.read_data_from_table()
        if flag is not False and self.w.rows != 0:
            path = "temp.txt"
            self.matrix = numpy.loadtxt(path)
            if booleanGraph:
                self.booleanGraph = True
                self.graph = nx.DiGraph(self.matrix)
            else:
                self.booleanGraph = False
                self.graph = nx.Graph(self.matrix)
            # self.graph = nx.fast_gnp_random_graph(100,0.1,None,False)
            self.plot()
            return self.graph
        else:
            pass

    def plot(self, node_color_map=[], edge_color_map=[]):
        self.figure.clear()
        pos = nx.circular_layout(self.graph)
        edge_labels = dict([((u, v,), d['weight'])
                            for u, v, d in self.graph.edges(data=True)])
        if not node_color_map:
            if self.graph.number_of_nodes() < 50:
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
                nx.draw(self.graph, pos, with_labels=True, node_size=550,node_color='lightgreen')
            else:
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
                nx.draw(self.graph, pos, with_labels=True, node_size=300,node_color='lightgreen')
        else:
            if self.graph.number_of_nodes() < 50:
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
                nx.draw(self.graph, pos, node_size=550,
                        edge_color=edge_color_map, with_labels=True,node_color='lightgreen')
            else:
                nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
                nx.draw(self.graph, pos, node_size=300, node_color='lightgreen',
                        edge_color=edge_color_map, with_labels=True,)
        self.draw_idle()

    def output_info(self, model, path):
        model.append(str("Количество вершин графа:"))
        model.append(str(self.graph.number_of_nodes()))
        model.append(str("Вершины:"))
        model.append(str(self.graph.nodes))
        model.append(str("Алгоритм Дейкстры:"))
        for i in path:
            model.append(str(i))
        model.append(str("Вес кратчайшего пути:"))
        path = path[0]
        dijkstra_weight = nx.dijkstra_path_length(self.graph, path[0], path[-1])
        model.append(str(dijkstra_weight))

    def dijkstra1(self, fro, to, model):
        try:
            self.all_paths = nx.all_shortest_paths(self.graph, fro, to, weight='weight')
            self.weight = nx.dijkstra_path_length(self.graph, fro, to)
            print(self.all_paths)
            self.new_all_paths = []
            for i in self.all_paths:
                self.new_all_paths.append(i)
            print(self.weight)
            self.wind.show_all_paths(self.new_all_paths, self.weight)
            self.wind.show()
            self.dijkstra_path(self.graph, fro, to)

        except:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Dijkstra error")
            error_dialog.setText("Для введенных вершин путь не найден")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()

    def dijkstra(self, fro, to, model):
        try:
            self.path = nx.dijkstra_path(self.graph, fro, to)
            all_paths = nx.all_shortest_paths(self.graph, fro, to)

            for i in all_paths:
                print(i)
            self.dijkstra_path(self.graph, fro, to)
            node_color_map = []
            for node in self.graph:
                if node in self.path:
                    node_color_map.append('red')
                else:
                    node_color_map.append('blue')
            edges = self.graph.edges()
            for e in edges:
                self.graph[e[0]][e[1]]['color'] = 'black'
            for i in xrange(len(self.path) - 1):
                self.graph[self.path[i]][self.path[i + 1]]['color'] = 'red'

            edge_color_map = [self.graph[e[0]][e[1]]['color'] for e in edges]
            self.plot(node_color_map, edge_color_map)
            self.output_info(model, self.path)
        except:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Dijkstra error")
            error_dialog.setText("Для введенных вершин путь не найден")
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.exec_()

    def backtrace(self, parent, start, end):
        path = [end]
        while path[-1] != start:
            path.append(parent[path[-1]])
        path.reverse()
        return path

    def dijkstra_path(self, graph, source, target):
        file = open('output.txt', 'a')
        queue = []
        visited = {}
        distance = {}
        shortest_distance = {}
        parent = {}

        for node in range(len(graph)):
            distance[node] = None
            visited[node] = False
            parent[node] = None
            shortest_distance[node] = float("inf")

        queue.append(source)
        distance[source] = 0
        while len(queue) != 0:
            current = queue.pop(0)
            visited[current] = True
            if current == target:
                print(self.backtrace(parent, source, target))
                # break
            for neighbor in graph[current]:
                if visited[neighbor] == False:
                    distance[neighbor] = distance[current] + 1
                    if distance[neighbor] < shortest_distance[neighbor]:
                        shortest_distance[neighbor] = distance[neighbor]
                        parent[neighbor] = current
                        queue.append(neighbor)
        file.write('dijkstra paths: ' + '\n')
        for i in self.new_all_paths:
            file.write(str(i) + '\n')
        file.write('dijkstra weight: ' + str(self.weight) + '\n'
                   + 'shortest_distance to others degrees:' + str(shortest_distance) + '\n'
                   + 'parent degree:' + str(parent) + '\n'
                   + 'target:' + str(target) + '\n')

    def add_nodes(self):
        if self.graph is None:
            self.graph = nx.Graph()
        nodes = self.graph.number_of_nodes()
        self.graph.add_node(nodes)
        self.plot()

    def link_nodes(self, number1, number2, w):
        self.graph.add_edge(number1, number2, weight=w)
        self.plot()


class OutputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.left = 700
        self.top = 270
        self.width = 500
        self.height = 500
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.textBrowser = QTextBrowser(self)
        self.textBrowser.setGeometry(QRect(50, 50, 400, 400))
        font = QFont()
        font.setPointSize(11)
        self.textBrowser.setFont(font)
        self.textBrowser.setObjectName("lineEdit")

    def show_all_paths(self, all_paths, weight):
        self.textBrowser.append(str("Все маршруты: "))
        for i in all_paths:
            self.textBrowser.append(str(i))
        for i in all_paths:
            print(i)
        self.textBrowser.append(str("Вес маршрута:"))
        self.textBrowser.append(str(weight))
        self.textBrowser.append(str("----------------------"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
