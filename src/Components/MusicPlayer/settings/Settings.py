import os
from PyQt5.QtCore import pyqtSignal
from .DataBase import Database


class Settings(object):

    # settings
    DEFAULT_SETTINGS = {
        "mediaLocation": os.path.normpath(os.path.expanduser("~/.tool/MusicPlayer")),
        "fileWatch": False,
        "redrawBackground": True,
        "volume": 100,
        "ffmpeg_path": ""
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