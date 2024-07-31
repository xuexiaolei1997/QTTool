import os
import datetime
from functools import total_ordering
from PyQt5.QtCore import Qt, QFileSystemWatcher, QMimeDatabase
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from PyQt5.QtMultimedia import *
from UI.UI_MusicPlayer import Ui_MusicPlayer


mimeDatabase = QMimeDatabase()
def getFileType(f):
    mime = mimeDatabase.mimeTypesForFileName(f)
    if not mime: return ""
    return mime[0].name().split("/")[0]


def pathUp(path):
    if path.startswith("file://"):
        return os.path.normpath(os.path.join(path[7:], ".."))
    return os.path.normpath(os.path.join(path, ".."))


@total_ordering
class MediaInfo(object):
    IMAGE_CACHE = os.path.join(Database.BASE, "cache")
    def __init__(self, path,
                       pos=0,
                       title="", artist="",
                       album="", albumArtist="",
                       duration=datetime.datetime.fromtimestamp(0),
                       image=None, year=0):
        self.path = path
        self.pos = pos
        self.title = title if title else path
        self.artist = artist
        self.album = album
        self.albumArtist = albumArtist
        self.year = year
        self.duration = duration
        self.image = image

class MusicPlayer(Ui_MusicPlayer, QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setupUi(self)

        self.music_directory = "/"
        self.media = QMediaPlayer()
        self.mediaInfo = None
        self.medias = [] # medias in scan directory

        self.fsWatcher = QFileSystemWatcher()

        self.pushButton_ChangeDir.clicked.connect(self.change_dir)

    def change_dir(self):
        pass

    def setWatchFiles(self):
        if self.medias:
            for media in self.medias:
                self.fsWatcher.addPath(pathUp(media.path))
                self.fsWatcher.addPath(media.path)
        self.fsWatcher.fileChanged.connect(self.watchFileChanged)
        self.fsWatcher.directoryChanged.connect(self.watchDirChanged)
    
    def watchFileChanged(self, fpath):
        pass

    def watchDirChanged(self, dpath):
        # TODO: handle directories
        oldPaths = set(filter(lambda fpath: pathUp(fpath) == dpath,
            map(lambda info: info.path[7:], self.medias)))
        newPaths = set(map(lambda fpath: os.path.join(dpath, fpath),
                filter(lambda fpath: getFileType(fpath) == "audio", os.listdir(dpath))))

        fremoved = oldPaths.difference(newPaths)
        self.medias = list(filter(lambda media: media.path[7:] not in fremoved, self.medias))
        for added in newPaths.difference(oldPaths):
            try:
                self.medias.append(MediaInfo.fromFile(added))
            except OSError:
                return
        self.mediasUpdated.emit()