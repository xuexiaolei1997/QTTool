import os
import json
import pickle

class Database:

    # BASE = os.path.expanduser("~/.music")
    BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    # Algorithm of Export Accompany from Music
    ACCOMPANY_ALGORITHM_LIST = ["Spleeter", "Demucs"]

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