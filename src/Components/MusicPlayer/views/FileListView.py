from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QColor
from operator import attrgetter

import re
from ..settings.DataBase import Database

FILTER_REGEX = re.compile(r'\b(artist|album|aartist)\:"((?:[^"\\]|\\.)*)"', re.IGNORECASE)


def dropShadow():
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(15)
    effect.setXOffset(0)
    effect.setYOffset(3)
    effect.setColor(QColor(0, 0, 0, 30))
    return effect


def highlightText(text, sub):
    return re.sub("(%s)" % re.escape(sub), r"<b>\1</b>", text, flags=re.IGNORECASE)


# file list view
class FileListTableItemDelegate(QStyledItemDelegate):

    def paint(self, painter, option, index):
        option.state &= ~QStyle.State_HasFocus
        option.state &= ~QStyle.State_MouseOver
        if option.styleObject.hoverRow == index.row():
            option.state |= QStyle.State_MouseOver
        QStyledItemDelegate.paint(self, painter, option, index)

class FileListTableWidget(QTableWidget):
    # https://github.com/lowbees/Hover-entire-row-of-QTableView
    def __init__(self, parent=None, rows=1, cols=7):
        QTableView.__init__(self, rows, cols)
        self.parent_ = parent

        self.setMouseTracking(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.setHorizontalHeaderLabels(["Time", "Name", "Artist", "Album", "Album artist"])
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents) # dur
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents) # title
        self.horizontalHeader().setGraphicsEffect(dropShadow())
        self.horizontalHeader().sectionClicked.connect(self.headerClicked)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setShowGrid(False)
        self.setItemDelegate(FileListTableItemDelegate())

        self.hoverRow = -1
        self.nrows = 0
        self.sortKey = "title"
        self.sortRev = False
        self.filterText = ""
        self.specialFilter = False
        self.mediaRow = []
        
        self.mediaBatch = 0

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def selectPlaying(self):
        if not self.mediaRow: return
        try:
            i, _ = next(filter(lambda i: i[1] == self.parent_.mediaInfo, enumerate(self.mediaRow)))
            self.selectRow(i)
        except StopIteration:
            pass

    # add item
    def addMedia(self, mediaInfo, highlight=None):
        if not mediaInfo: return
        self.setRowCount(self.nrows+1)
        self.setItem(self.nrows, 0, QTableWidgetItem(mediaInfo.duration.strftime("%M:%S")))
        if highlight:
            self.setCellWidget(self.nrows, 1, QLabel(highlightText(mediaInfo.title, highlight)))
        else:
            self.setItem(self.nrows, 1, QTableWidgetItem(mediaInfo.title))
        self.setItem(self.nrows, 2, QTableWidgetItem(mediaInfo.artist))
        self.setItem(self.nrows, 3, QTableWidgetItem(mediaInfo.album))
        self.setItem(self.nrows, 4, QTableWidgetItem(mediaInfo.albumArtist))
        self.setRowHeight(self.nrows, 40)
        self.nrows += 1

    def mediasAdded(self, medias, append=True, highlight=None):
        if append:
          self.mediaRow += medias
        medias = iter(medias)
        self.mediaBatch += 1
        batchNo = self.mediaBatch
        def iteration():
            if self.mediaBatch != batchNo:
                return
            try:
                self.addMedia(next(medias), highlight)
                QTimer.singleShot(1, iteration)
            except:
                return
        # wait for the previous set of iteration
        # to finish before firing another one
        QTimer.singleShot(2, iteration)

    # data manip
    def sortAndFilter(self):
        if self.filterText:
            self.specialFilter = True
            matches = FILTER_REGEX.findall(self.filterText)
            
            if matches:
                matches = list(map(lambda m: (m[0], m[1].lower()), matches))
                def func(media):
                    for (key, value) in matches:
                        if key == "artist":
                            if value not in media.artist.lower():
                                return False
                    return True
                self.mediaRow = list(filter(func, self.parent_.medias))
            else:
                self.specialFilter = False
                self.mediaRow = list(filter(lambda media: self.filterText.lower() in media.title.lower(), self.parent_.medias))
        else:
            self.mediaRow = self.parent_.medias

        self.clearContents()
        self.nrows = 0
        self.setRowCount(0)
        if not self.mediaRow:
            self.mediaBatch += 1
            QTimer.singleShot(2, lambda: self.clearContents())
            return

        self.mediaRow.sort(key=attrgetter(self.sortKey), reverse=self.sortRev)
        self.mediasAdded(self.mediaRow, False, self.filterText)

    # events
    def headerClicked(self, index):
        if index == 0: key = 'duration'
        elif index == 1: key = 'title'
        elif index == 2: key = 'artist'
        elif index == 3: key = 'album'
        elif index == 4: key = 'albumArtist'
        else: return

        if key == self.sortKey:
            self.sortRev = not self.sortRev
        else:
            self.sortKey = key
            self.sortAsc = False

        self.sortAndFilter()

    def mouseMoveEvent(self, e):
        QTableWidget.mouseMoveEvent(self, e)
        index = self.indexAt(e.pos())
        if index.column() == self.columnCount()-1:
            self.hoverRow = -1
        else:
            self.hoverRow = index.row()

    # def leaveEvent(self, e):
    #     self.hoverRow = -1

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            e.accept()
        else:
            QTableWidget.mousePressEvent(self, e)
            if self.hoverRow == -1: return
            if  e.modifiers() & Qt.ControlModifier or \
                e.modifiers() & Qt.ShiftModifier:
                return
            index = self.indexAt(e.pos())
            mainWindow = self.parent_
            if self.mediaRow:
                if mainWindow.mediaInfo and self.mediaRow[index.row()] == mainWindow.mediaInfo:
                    return
                mainWindow.setSong(self.mediaRow[index.row()])
    
    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())
        if index.isValid():
            menu = QMenu(self)

            action_play_music = QAction("Play", self)
            action_play_music.triggered.connect(lambda: self.parent_.setSong(self.mediaRow[index.row()]))

            menu_export_accompany = QMenu("Export Accompany", self)
            
            for accompany_algorithm in Database.ACCOMPANY_ALGORITHM_LIST:
                variable_name = f'action_export_accompany_{accompany_algorithm}'
                locals()[variable_name] = QAction(accompany_algorithm, self)
                locals()[variable_name].triggered.connect(lambda: self.parent_.exportAccompany(self.parent_.medias[index.row()].path, accompany_algorithm))
                menu_export_accompany.addAction(locals()[variable_name])

            menu.addAction(action_play_music)
            menu.addMenu(menu_export_accompany)
            menu.exec_(self.viewport().mapToGlobal(event.pos()))


class FileListView(QWidget):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.parent_ = parent
        self.initUI()
        self.bindEvents()
        self.mpos = None

    def initUI(self):
        vboxLayout = QVBoxLayout()
        vboxLayout.setContentsMargins(0,0,0,0)
        vboxLayout.setSpacing(0)
        self.setLayout(vboxLayout)

        self.tableWidget = tableWidget = FileListTableWidget(self.parent_)
        tableWidget.resizeEvent = self.tableResizeEvent
        tableWidget.setAlternatingRowColors(True)
        vboxLayout.addWidget(tableWidget, 1)

        # self.scrollBar = tableWidget.verticalScrollBar()
        # self.scrollBar.setParent(self)
        # self.scrollBar.show()

        if self.parent_.medias:
            self.tableWidget.mediasAdded(self.parent_.medias)
            self.tableWidget.selectPlaying()

    # events
    def bindEvents(self):
        self.parent_.mediasAdded.connect(self.tableWidget.mediasAdded)
        self.parent_.mediasUpdated.connect(self.tableWidget.sortAndFilter)
        self.parent_.songInfoChanged.connect(self.tableWidget.selectPlaying)

    def tableResizeEvent(self, event):
        QTableWidget.resizeEvent(self.tableWidget, event)
        # WIDTH = self.scrollBar.sizeHint().width()
        # self.scrollBar.setGeometry(QRect(
        #     self.tableWidget.width()-WIDTH,
        #     self.tableWidget.y()+self.tableWidget.horizontalHeader().height(),
        #     WIDTH, self.tableWidget.height()-self.tableWidget.horizontalHeader().height()
        # ))
