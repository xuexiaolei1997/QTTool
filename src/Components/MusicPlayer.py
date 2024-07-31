import os
import json
import datetime
from functools import total_ordering
import pickle

import taglib
from PyQt5.QtCore import Qt, QFileSystemWatcher, QMimeDatabase, QUrl, pyqtSignal, QThread, QSize
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
        return os.path.normpath(os.path.join(path[8:], ".."))
    return os.path.normpath(os.path.join(path, ".."))


def imageMimetypeToExt(mimetype):
    if mimetype == "image/jpg":    return ".jpg"
    elif mimetype == "image/jpeg": return ".jpeg"
    elif mimetype == "image/png":  return ".png"
    elif mimetype == "image/bmp":  return ".bmp"
    elif mimetype == "image/gif":  return ".gif"
    return ""


class Database:

    BASE = os.path.expanduser("~/.music")

    def getPath(filename):
        return os.path.join(Database.BASE, filename)

    # save
    def save(obj, filename, save_json=False):
        os.makedirs(Database.BASE, exist_ok=True)
        with open(Database.getPath(filename), ("w" if save_json else "wb")) as f:
            (json if save_json else pickle).dump(obj, f)

    def saveFile(obj, filename, path=""):
        path = os.path.join(Database.BASE, path)
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, filename), "wb") as f:
            f.write(obj)

    # load
    def load(filename, load_json=False, default=None):
        try:
            with open(Database.getPath(filename), ("r" if load_json else "rb")) as f:
                obj = (json if load_json else pickle).load(f)
                if default: return {**default, **obj}
                return obj
        except FileNotFoundError:
            print("can't load %s" % filename)
            return default

    def loadFile(filename, default=""):
        try:
            with open(Database.getPath(filename), "r") as f:
                return f.read()
        except:
            if not default: return ""
            dfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", default)
            with open(dfile, "r") as f:
                return f.read()


class Settings(object):

    # settings
    DEFAULT_SETTINGS = {
        "mediaLocation": os.path.normpath(os.path.expanduser("./Music")),
        "fileWatch": True,
        "redrawBackground": True,
        "disableDecorations": False,
        "darkTheme": False,
        "modules": {},
        "volume": 100,
        "accent": "#a9c5e4",
        "accentMid": "#7fa8d6",
        "accentDeep": "#7fa8d6",
    }
    SETINGS_FILE = "settings.json"

    # signals
    changed = pyqtSignal(tuple)

    def __init__(self):
        self._dict = Database.load(Settings.SETINGS_FILE, True,
                                   Settings.DEFAULT_SETTINGS)

    def __getattr__(self, attr):
        if attr == "_dict":
            return object.__getattribute__(self, "_dict")
        return self._dict[attr]

    def __setattr__(self, attr, value):
        if attr == "_dict":
            return object.__setattr__(self, "_dict", value)
        self._dict[attr] = value
        self.save()

    def save(self):
        Database.save(self._dict, Settings.SETINGS_FILE, True)


settings = Settings()


@total_ordering
class MediaInfo(object):
    IMAGE_CACHE = os.path.join("./", "cache")
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
    
    def searchImage(path, song=None):
        return None
        if song and song.picture:
            picture = song.picture
            ext = imageMimetypeToExt(picture.mimetype)
            dataHash = md5(picture.data).hexdigest()
            fpath = os.path.join(MediaInfo.IMAGE_CACHE, dataHash + ext)
            if os.path.isfile(fpath): return fpath
            Database.saveFile(picture.data, dataHash + ext, "cache")
            return fpath

        searchPath = pathUp(path)
        paths = list(filter(lambda path: getFileType(path) == "image", os.listdir(searchPath)))
        if paths:
            prioritize = ["Case Cover Back Outer", "Cover.", "cover.", "CD."]
            def find_path():
                for path in paths:
                    for priority in prioritize:
                        if path.startswith(priority):
                            return path
                return paths[0]
            return os.path.join(searchPath, find_path())
        else:
            return None

    def verify(self):
        if self.path.startswith("file://") and not os.path.isfile(self.path[8:]):
            return False
        if self.image and not os.path.isfile(self.image):
            self.image = MediaInfo.searchImage(self.path)
        return True
    
    def fromFile(path):
        try:
            song = taglib.File(path)
        except OSError:
            return MediaInfo(QUrl.fromLocalFile(path).toString(), 0, os.path.basename(path))
        artist = song.tags["ARTIST"][0] if "ARTIST" in song.tags else ""
        title = song.tags["TITLE"][0] if "TITLE" in song.tags else os.path.basename(path)

        pos = -1
        if "TRACKNUMBER" in song.tags:
            try:
                if "/" in song.tags["TRACKNUMBER"][0]:
                    pos = int(song.tags["TRACKNUMBER"][0].split("/")[0])
                else:
                    pos = int(song.tags["TRACKNUMBER"][0])
            except ValueError:
                pass

        try: album = song.tags["ALBUM"][0]
        except: album = ""

        try: albumArtist = song.tags["ALBUMARTIST"][0]
        except: albumArtist = artist

        try: year = int(song.tags["DATE"][0])
        except: year = -1

        return MediaInfo(QUrl.fromLocalFile(path).toString(), pos, title, artist,
                         album, albumArtist,
                         datetime.datetime.fromtimestamp(song.length),
                         MediaInfo.searchImage(path, song),
                         year)

    # comparators
    def __lt__(self, other):
        if not isinstance(other, MediaInfo):
            return False
        if self.album == other.album and self.pos != -1 and other.pos != -1:
            return self.pos < other.pos
        return self.title < other.title

    def __eq__(self, other):
        if not isinstance(other, MediaInfo):
            return False
        if self.path == other.path:
            return True
        return object.__eq__(self, other)


@total_ordering
class AlbumInfo(object):

    def __init__(self, info, populate=True):
        self.medias = []
        if isinstance(info, str):
            self.title = info
            self.path = info
            self.artist = self.image = None
        else:
            self.title = info.album
            self.path = pathUp(info.path)
            self.artist = info.albumArtist
            self.image = info.image

            if populate:
                for f in os.listdir(self.path):
                    fpath = os.path.join(self.path, f)
                    if os.path.isfile(fpath) and getFileType(fpath) == "audio":
                        mediaInfo = MediaInfo.fromFile(fpath)
                        self.medias.append(mediaInfo)
                self.medias.sort()

    def __lt__(self, other):
        return self.title < other.title


class MediaLocationSelectionDialog(QWidget):

    def __init__(self):
        QWidget.__init__(self)
        self.initUI()
        self.bindEvents()

    # ui
    def initUI(self):
        self.setWindowTitle("oopsie woopsie!")
        self.setWindowFlags(Qt.Dialog)
        self.resize(QSize(320, 120))
        self.setMinimumSize(self.size())

        layout = QGridLayout()
        self.setLayout(layout)

        layout.addWidget(QWidget(), 0, 0)
        layout.setRowStretch(0,1)

        label = QLabel("Please choose a valid music directory:")
        layout.addWidget(label, 1, 0, 1, 2)

        self.musicLocationInput = musicLocationInput = QLineEdit()
        musicLocationInput.setText(settings.mediaLocation)
        layout.addWidget(musicLocationInput, 2, 0)

        self.musicLocationBrowse = musicLocationBrowse = QPushButton("Browse...")
        layout.addWidget(musicLocationBrowse, 2, 1)
        layout.setColumnStretch(0, 1)

        layout.addWidget(QWidget(), 3, 0)
        layout.setRowStretch(3,1)

        self.okButton = QPushButton("OK")
        self.okButton.setEnabled(os.path.isdir(settings.mediaLocation))
        layout.addWidget(self.okButton, 4, 0, 1, 2, Qt.AlignRight)

    # events
    def bindEvents(self):
        self.musicLocationBrowse.clicked.connect(self.musicLocationBrowseClicked)

    def musicLocationBrowseClicked(self):
        self.fileDialog = dialog = QFileDialog()
        dialog.setDirectory(settings.mediaLocation)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        dialog.fileSelected.connect(self.refreshMedia)
        dialog.show()

    def refreshMedia(self, dpath):
        if os.path.isdir(dpath):
            settings.mediaLocation = dpath
            self.musicLocationInput.setText(dpath)
            self.okButton.setEnabled(True)
        else:
            self.okButton.setEnabled(False)


class MusicPlayer(Ui_MusicPlayer, QDialog):

    MEDIAS_FILE = "medias.pkl"

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setupUi(self)

        self.media = QMediaPlayer()
        self.mediaInfo = None
        self.album = None
        self.albums = {}
        self.albumPath = ""
        self.medias = [] # medias in scan directory

        self.setWatchFiles()

        self.setStyles()
        if settings.redrawBackground:
            # workaround for qt themes with transparent backgrounds
            self.setProperty("class", "redraw-background")
            self.style().unpolish(self)
        
        self.media.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.media.durationChanged.connect(self.durationChanged)
        self.media.volumeChanged.connect(self.volumeChanged)
        self.media.setVolume(settings.volume)

        try:
            medias = Database.load(self.MEDIAS_FILE)
        except:
            medias = None
        if medias:
            self.medias = list(filter(lambda media: media.verify(), medias))
            for mediaInfo in medias:
                dpath = pathUp(mediaInfo.path)
                if mediaInfo.album:
                    if dpath not in self.albums:
                        self.albums[dpath] = AlbumInfo(mediaInfo, False)
                    self.albums[dpath].medias.append(mediaInfo)
            self.sortAlbums()
            if len(medias) != len(self.medias):
                Database.save(self.medias, self.MEDIAS_FILE)
            if settings.fileWatch:
                for media in self.medias:
                    self.fsWatcher.addPath(pathUp(media.path))
                    self.fsWatcher.addPath(media.path)
        elif not os.path.isdir(settings.mediaLocation):
            self.hide()
            self.mediaSelectionDialog = MediaLocationSelectionDialog()
            def delMediaSelection():
                self.show()
                self.populateMediaThread()
                del self.mediaSelectionDialog
            self.mediaSelectionDialog.okButton.clicked.connect(delMediaSelection)
            self.mediaSelectionDialog.show()
        else:
            self.populateMediaThread()
    
    def populateMediaThread(self):
        class ProcessMediaThread(QThread):

            def run(self_):
                self.populateMedias(settings.mediaLocation)
                os.makedirs("./", exist_ok=True)
                Database.save(self.medias, self.MEDIAS_FILE)
                del self._thread

        self._thread = ProcessMediaThread()
        self._thread.start()
    
    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.nextSong()
    
    def durationChanged(self, duration):
        if duration:
            self.mediaInfo.duration = datetime.datetime.fromtimestamp(duration)
            self.songInfoChanged.emit(self.mediaInfo)

    def nextSong(self):
        self.navigateSong(1)
    def prevSong(self):
        self.navigateSong(-1)
    
    # song info
    songInfoChanged = pyqtSignal(MediaInfo)

    def setSong(self, info):
        if isinstance(info, str):
            self.setSongInfo(info)
        elif isinstance(info, MediaInfo):
            self.mediaInfo = info
            self.songInfoChanged.emit(self.mediaInfo)
        mediaContent = QMediaContent(QUrl(self.mediaInfo.path))
        self.media.setMedia(mediaContent)
        self.media.play()
        self.media.stateChanged.emit(self.media.state())

    def setSongInfo(self, path):
        if path.startswith("file://"):
            self.mediaInfo = MediaInfo.fromFile(path[8:])
        else:
            self.mediaInfo = MediaInfo(path)
        self.songInfoChanged.emit(self.mediaInfo)

    def durationChanged(self, duration):
        if duration:
            self.mediaInfo.duration = datetime.datetime.fromtimestamp(duration)
            self.songInfoChanged.emit(self.mediaInfo)

    # dnd
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/uri-list"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasUrls():
            url = e.mimeData().urls()[0].url()
            self.setSong(url)
        elif e.mimeData().hasText():
            text = e.mimeData().text()
            if text.startswith("file://"):
                self.setSong(text)

    # album
    albumChanged = pyqtSignal(AlbumInfo)
    def populateAlbum(self, info): # TODO
        if not info.path.startswith("file://"): return
        albumPath = pathUp(info.path)
        if albumPath in self.albums:
            newAlbum = self.albums[albumPath]
        else:
            newAlbum = AlbumInfo(info)
        if newAlbum != self.album:
            self.album = newAlbum
            self.albumChanged.emit(self.album)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.nextSong()

    # controls
    def songIndex(self, array):
        try:
            i, _ = next(filter(lambda i: i[1] == self.mediaInfo, enumerate(array)))
            return i
        except StopIteration:
            return -1
    def nextSongArray(self, array, delta):
        idx = self.songIndex(array)
        if idx == -1: return
        if 0 <= idx+delta < len(array):
            self.setSong(array[idx+delta])

    def navigateSong(self, num):
        if self.mode == MainWindow.FULL_MODE:
            mode = self.centralWidget().mode
            if mode == MediaPlayer.PLAYING_ALBUM_MODE:
                self.nextSongArray(self.album.medias, num)
            else:
                self.nextSongArray(self.centralWidget().view.tableWidget.mediaRow, num)
        elif self.album:
            self.nextSongArray(self.album.medias, num)

    def nextSong(self):
        self.navigateSong(1)
    def prevSong(self):
        self.navigateSong(-1)


    # volume
    def volumeChanged(self, volume):
        settings.volume = volume

    # files
    mediasAdded = pyqtSignal(list)
    mediasUpdated = pyqtSignal()
    def populateMedias(self, path):
        batch = []
        ls = list(map(lambda f: os.path.join(path, f), os.listdir(path)))
        if not ls: return
        if settings.fileWatch:
            self.fsWatcher.addPath(path)
            self.fsWatcher.addPaths(ls)
        for fpath in ls:
            if os.path.isdir(fpath):
                self.populateMedias(fpath)
            elif os.access(fpath, os.R_OK) and getFileType(fpath) == "audio":
                mediaInfo = MediaInfo.fromFile(fpath)
                dpath = pathUp(mediaInfo.path)
                if mediaInfo.album:
                    if dpath not in self.albums:
                        self.albums[dpath] = AlbumInfo(mediaInfo, False)
                    self.albums[dpath].medias.append(mediaInfo)
                batch.append(mediaInfo)
        self.sortAlbums()
        self.medias.extend(batch)
        self.mediasAdded.emit(batch)
    
    # albums
    def sortAlbums(self):
        for album in self.albums.values():
            album.medias.sort()
    
    def navigateSong(self, num):
        if self.mode == MainWindow.FULL_MODE:
            mode = self.centralWidget().mode
            if mode == MediaPlayer.PLAYING_ALBUM_MODE:
                self.nextSongArray(self.album.medias, num)
            else:
                self.nextSongArray(self.centralWidget().view.tableWidget.mediaRow, num)
        elif self.album:
            self.nextSongArray(self.album.medias, num)
    
    def volumeChanged(self, volume):
        settings.volume = volume

    def setStyles(self):
        stylesheet = Database.loadFile("css/style.css", "css/dark.css" if settings.darkTheme else "css/style.css")
        stylesheet = stylesheet.replace("ACCENTDEEP", settings.accentDeep) \
                      .replace("ACCENTMID", settings.accentMid)    \
                      .replace("ACCENT", settings.accent)
        self.setStyleSheet(stylesheet)
        # if self.checkBox_DarkTheme.checkState():
        #     self.centralWidget().backgroundLabel.setVisible(self.settings.darkTheme)

    def change_dir(self):
        pass

    def setWatchFiles(self):
        if settings.fileWatch:
            self.fsWatcher = QFileSystemWatcher()
            if self.medias:
                for media in self.medias:
                    self.fsWatcher.addPath(pathUp(media.path))
                    self.fsWatcher.addPath(media.path)
            self.fsWatcher.fileChanged.connect(self.watchFileChanged)
            self.fsWatcher.directoryChanged.connect(self.watchDirChanged)
        elif hasattr(self, "fsWatcher"):
            del self.fsWatcher
    
    def watchFileChanged(self, fpath):
        pass

    def watchDirChanged(self, dpath):
        # TODO: handle directories
        oldPaths = set(filter(lambda fpath: pathUp(fpath) == dpath,
            map(lambda info: info.path[8:], self.medias)))
        newPaths = set(map(lambda fpath: os.path.join(dpath, fpath),
                filter(lambda fpath: getFileType(fpath) == "audio", os.listdir(dpath))))

        fremoved = oldPaths.difference(newPaths)
        self.medias = list(filter(lambda media: media.path[8:] not in fremoved, self.medias))
        for added in newPaths.difference(oldPaths):
            try:
                self.medias.append(MediaInfo.fromFile(added))
            except OSError:
                return
        self.mediasUpdated.emit()
    