import os
import re
import json
import datetime
from functools import total_ordering
import pickle
import subprocess

import taglib
from PyQt5 import Qt
from PyQt5.QtCore import Qt, QFileSystemWatcher, QMimeDatabase, QUrl, pyqtSignal, QThread, QSize, QObject
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import QIcon, QPixmap

from .UI_MusicPlayer import Ui_MusicPlayer
from .views.FileListView import FileListView
from .settings.Settings import Settings
from .settings.DataBase import Database

mimeDatabase = QMimeDatabase()
def getFileType(f):
    mime = mimeDatabase.mimeTypesForFileName(f)
    if not mime: return ""
    return mime[0].name().split("/")[0]


def remove_file_prefix(path):
    """ Remove file:// in path """
    path = re.sub(r"^file:\/+", "", path)
    return path


def pathUp(path):
    if path.startswith("file://"):
        return os.path.normpath(os.path.join(remove_file_prefix(path), ".."))
    return os.path.normpath(os.path.join(path, ".."))


def imageMimetypeToExt(mimetype):
    if mimetype == "image/jpg":    return ".jpg"
    elif mimetype == "image/jpeg": return ".jpeg"
    elif mimetype == "image/png":  return ".png"
    elif mimetype == "image/bmp":  return ".bmp"
    elif mimetype == "image/gif":  return ".gif"
    return ""


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget():
            child.widget().deleteLater()

settings = Settings()


@total_ordering
class MediaInfo(object):
    
    def __init__(self, path,
                       pos=0,
                       title="", artist="",
                       album="", albumArtist="",
                       duration=datetime.datetime.fromtimestamp(0)):
        self.path = path
        self.pos = pos
        self.title = title if title else path
        self.artist = artist
        self.album = album
        self.albumArtist = albumArtist
        self.duration = duration

    def verify(self):
        if self.path.startswith("file://") and not os.path.isfile(remove_file_prefix(self.path)):
            return False
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

        return MediaInfo(QUrl.fromLocalFile(path).toString(), pos, title, artist,
                         album, albumArtist,
                         datetime.datetime.fromtimestamp(song.length))

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
            settings.mediaLocation = dpath  # update settings.json
            self.musicLocationInput.setText(dpath)
            self.okButton.setEnabled(True)
        else:
            self.okButton.setEnabled(False)


class MusicPlayer(Ui_MusicPlayer, QDialog):

    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setAcceptDrops(True)
        # self.setWindowFlags(Qt.Tool | Qt.X11BypassWindowManagerHint |
        #                     Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setupUi(self)

        self.media = QMediaPlayer()
        self.mediaInfo = None
        self.medias = [] # medias in scan directory

        # Set ffmpeg path: Ensure running in virtural environment
        os.environ["PATH"] += os.pathsep + settings.ffmpeg_path

        # Thread: Used 2 Export Accompany
        self.exportAccompanyThread = QThread()

        self.setWatchFiles()

        self.setStyles()
        if settings.redrawBackground:
            # workaround for qt themes with transparent backgrounds
            self.setProperty("class", "redraw-background")
            self.style().unpolish(self)
        
        # load file
        if not os.path.isdir(settings.mediaLocation):
            self.change_dir()
        else:
            self.populateMediaThread()
        
        # Init extra UI
        self.tableView_Music = FileListView(self)
        self.verticalLayout_tablelist.addWidget(self.tableView_Music)
        self.horizontalSlider_volume.setValue(settings.volume)
        
        # Change directory
        self.pushButton_ChangeDir.clicked.connect(self.change_dir)

        # Control media
        self.media.stateChanged.connect(self.stateChanged)
        self.media.mediaStatusChanged.connect(self.mediaStatusChanged)
        
        self.media.durationChanged.connect(self.mediaDurationChanged)
        self.media.positionChanged.connect(self.mediaPositionChanged)
        self.media.volumeChanged.connect(self.mediaVolumeChanged)
        self.media.mutedChanged.connect(self.mutedChanged)
        self.media.setVolume(settings.volume)

        # Control songs
        self.pushButton_pause.clicked.connect(self.playPause)
        self.pushButton_previous.clicked.connect(self.prevSong)
        self.pushButton_next.clicked.connect(self.nextSong)

        # Control process
        self.horizontalSlider_song_duration.valueChanged.connect(self.positionSliderChanged)

        # Control volume
        self.horizontalSlider_volume.valueChanged.connect(self.volumeSliderChanged)
        self.pushButton_volume.clicked.connect(self.volumeButtonClicked)

        # Search
        self.lineEdit_SearchMusic.textChanged.connect(self.searchMusic)
    
    def searchMusic(self, text):
        self.tableView_Music.tableWidget.filterText = text
        self.tableView_Music.tableWidget.sortAndFilter()
        if self.tableView_Music.tableWidget.specialFilter:
            return

    def setWatchFiles(self):
        """ Watch file and dir """
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

    def setStyles(self):
        """ Set css """
        stylesheet = Database.loadFile("style.css")
        self.setStyleSheet(stylesheet)

    def change_dir(self):
        """ Change music directory """
        self.hide()
        self.mediaSelectionDialog = MediaLocationSelectionDialog()
        def delMediaSelection():
            self.show()
            self.populateMediaThread()
            del self.mediaSelectionDialog
        self.mediaSelectionDialog.okButton.clicked.connect(delMediaSelection)
        self.mediaSelectionDialog.show()

    def populateMediaThread(self):
        """ Search music thread """
        class ProcessMediaThread(QThread):

            def run(self_):
                self.populateMedias(settings.mediaLocation)
                del self._thread

        self._thread = ProcessMediaThread()
        self._thread.start()
    
    # files
    mediasAdded = pyqtSignal(list)
    mediasUpdated = pyqtSignal()
    def populateMedias(self, path):
        """ Search music from path """
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
                batch.append(mediaInfo)
        # self.sortAlbums()
        self.medias.extend(batch)
        self.mediasAdded.emit(batch)
    
    # Current Music
    # song info
    songInfoChanged = pyqtSignal(MediaInfo)

    def setSong(self, info):
        """ Set play song """
        if isinstance(info, str):
            self.setSongInfo(info)
        elif isinstance(info, MediaInfo):
            self.mediaInfo = info
            self.songInfoChanged.emit(self.mediaInfo)
        mediaContent = QMediaContent(QUrl(self.mediaInfo.path))
        self.media.setMedia(mediaContent)

        self.media.play()
        self.label_song_name.setText(self.mediaInfo.title)
        self.media.stateChanged.emit(self.media.state())

    def setSongInfo(self, path):
        """ Set song info 2 media info """
        if path.startswith("file://"):
            self.mediaInfo = MediaInfo.fromFile(remove_file_prefix(path))
        else:
            self.mediaInfo = MediaInfo(path)
        self.songInfoChanged.emit(self.mediaInfo)
    
    def mediaDurationChanged(self, duration):
        if duration:
            self.mediaInfo.duration = datetime.datetime.fromtimestamp(duration)
            self.songInfoChanged.emit(self.mediaInfo)
            self.horizontalSlider_song_duration.setMaximum(duration)
            self.horizontalSlider_song_duration.setPageStep(duration // 10)
    
    def mediaPositionChanged(self, position):
        self.horizontalSlider_song_duration.blockSignals(True)
        self.horizontalSlider_song_duration.setValue(position)
        self.horizontalSlider_song_duration.blockSignals(False)

    def mediaVolumeChanged(self, volume):
        self.horizontalSlider_volume.blockSignals(True)
        self.horizontalSlider_volume.setValue(volume)
        self.horizontalSlider_volume.blockSignals(False)
        if volume != 0:
            settings.volume = volume
    
    def volumeSliderChanged(self, volume):
        self.media.setVolume(volume)

    def mediaStatusChanged(self, status):
        """ Auto play next song """
        if status == QMediaPlayer.EndOfMedia:
            self.nextSong()
    
    # controls
    def stateChanged(self, state):
        if state == QMediaPlayer.PlayingState:
            pause_icon = QIcon()
            pause_icon.addPixmap(QPixmap(":/icons/icons/media-playback-pause.svg"), QIcon.Normal, QIcon.Off)
            self.pushButton_pause.setIcon(pause_icon)
        else:
            start_icon = QIcon()
            start_icon.addPixmap(QPixmap(":/icons/icons/media-playback-start.svg"), QIcon.Normal, QIcon.Off)
            self.pushButton_pause.setIcon(start_icon)

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
        self.nextSongArray(self.tableView_Music.tableWidget.mediaRow, num)
    
    # pause
    def playPause(self):
        """ Control play & pause """
        if self.media.state() == QMediaPlayer.PlayingState:
            self.media.pause()
        else:
            self.media.play()

    def nextSong(self):
        self.navigateSong(1)

    def prevSong(self):
        self.navigateSong(-1)
    
    # volume
    def positionSliderChanged(self, position):
        self.media.setPosition(position)
    
    def volumeButtonClicked(self):
        self.media.setMuted(not self.media.isMuted())
    
    def mutedChanged(self, muted):
        if muted:
            muted_icon = QIcon()
            muted_icon.addPixmap(QPixmap(":/icons/icons/audio-volume-muted.svg"), QIcon.Normal, QIcon.Off)
            self.pushButton_volume.setIcon(muted_icon)
            self.horizontalSlider_volume.setValue(0)
        else:
            unmuted_icon = QIcon()
            unmuted_icon.addPixmap(QPixmap(":/icons/icons/audio-volume-high.svg"), QIcon.Normal, QIcon.Off)
            self.pushButton_volume.setIcon(unmuted_icon)
            self.horizontalSlider_volume.setValue(settings.volume)

    # export accompany
    def exportAccompany(self, fpath, method, sub_model=None):
        if method not in Database.ACCOMPANY_ALGORITHM_LIST:
            return
        fpath = remove_file_prefix(fpath)
        our_dir = QFileDialog.getExistingDirectory(self, "Open Folder", "./")
        if our_dir == "":
            return

        class SperateMusicAccompanyWorker(QObject):
            success = pyqtSignal(bool)
            finished = pyqtSignal()

            def __init__(self, method, mp3_path, output_dir):
                super().__init__()
                self.method = method
                self.mp3_path = mp3_path
                self.output_dir = output_dir
                self.sub_model = sub_model

            def run(self):
                try:
                    if self.method == 'Spleeter':
                        res = self.export_with_spleeter()
                    elif self.method == 'Demucs':
                        res = self.export_with_demucs()
                    self.success.emit(res)
                except Exception as e:
                    print(str(e))
                    self.success.emit(False)
                finally:
                    self.finished.emit()

            def export_with_spleeter(self):
                from spleeter.separator import Separator
                separator = Separator('spleeter:2stems')
                separator.separate_to_file(self.mp3_path, self.output_dir)
                return True

            def export_with_demucs(self):
                if not self.check_ffmpeg():
                    return
                res = subprocess.run(['demucs', '-o', self.output_dir, "--two-stems", "vocals", self.mp3_path])
                return True if res.returncode == 0 else False

            def check_ffmpeg(self):
                try:
                    subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    return True
                except FileNotFoundError:
                    QMessageBox.critical(None, "FFmpeg Not Found", "FFmpeg is required for Demucs. Please install FFmpeg and try again.")
                    return False
        
        def exec_result(res: bool):
            if res:
                QMessageBox.information(self, "Export Success", "The instrumental track has been successfully exported.")
            else:
                QMessageBox.critical(self, "Export Fail", "The instrumental exported failed.")
        
        if hasattr(self, "exportAccompanyThread") and self.exportAccompanyThread.isRunning():
            QMessageBox.critical(self, "Error", "Current export task is executing.")
            return

        self.worker = SperateMusicAccompanyWorker(method, fpath, our_dir)
        self.worker.moveToThread(self.exportAccompanyThread)

        self.exportAccompanyThread.started.connect(self.worker.run)
        self.worker.success.connect(exec_result)
        self.worker.finished.connect(self.exportAccompanyThread.quit)
        self.worker.finished.connect(self.worker.deleteLater)

        self.exportAccompanyThread.start()


    def watchFileChanged(self, fpath):
        pass

    def watchDirChanged(self, dpath):
        self.medias = []
        newPaths = set(map(lambda fpath: os.path.join(dpath, fpath),
                filter(lambda fpath: getFileType(fpath) == "audio", os.listdir(dpath))))

        for added in newPaths:
            try:
                self.medias.append(MediaInfo.fromFile(added))
            except OSError:
                return
        self.mediasUpdated.emit()
    