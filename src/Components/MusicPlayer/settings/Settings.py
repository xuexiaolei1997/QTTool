import os
from PyQt5.QtCore import pyqtSignal
from .DataBase import Database


class Settings(object):

    # settings
    DEFAULT_SETTINGS = {
        "mediaLocation": os.path.normpath(os.path.expanduser("~/.music")),
        "fileWatch": False,
        "redrawBackground": True,
        "disableDecorations": False,
        "darkTheme": False,
        "modules": {},
        "volume": 100,
        "accent": "#a9c5e4",
        "accentMid": "#7fa8d6",
        "accentDeep": "#7fa8d6",
        "ffmpeg_path": "D:\\Software\\ffmpeg-7.0.2-full_build-shared\\bin"
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