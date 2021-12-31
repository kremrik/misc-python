from copy import copy
from os import walk
from os.path import getmtime, join


class WatchDir:
    def __init__(self, path = None) -> None:
        self.tracker = Tracker.create()
        self.path = path if path else "."

    def event_detected(self):
        all = list(list_files(self.path))
        new = new_files(self.tracker, all)
        mod = modified_files(self.tracker, all)
        rmd = removed_files(self.tracker, all)

        for file in new:
            self.tracker = Tracker.add(self.tracker, file)
        for file in mod:
            self.tracker = Tracker.update(self.tracker, file)
        for file in rmd:
            self.tracker = Tracker.remove(self.tracker, file)

        if new or mod:
            return True
        return False


# ---------------------------------------------------------
def list_files(path = None):
    if not path:
        path = "."

    for root, dirs, files in walk(path):
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        
        yield from (join(root, file) for file in files)


# ---------------------------------------------------------
def new_files(tracker, all):
    tracked_files = Tracker.files(tracker)
    return list(set(all) - set(tracked_files))


def removed_files(tracker, all):
    tracked_files = Tracker.files(tracker)
    return list(set(tracked_files) - set(all))


def existing_files(tracker, all):
    tracked_files = Tracker.files(tracker)
    return list(set(tracked_files) & set(all))


def modified_files(tracker, all):
    existing = existing_files(tracker, all)

    modified = []
    for file in existing:
        cur_mtime = _mod_ts(file)
        trk_mtime = Tracker.get_mtime(tracker, file)
        
        if cur_mtime != trk_mtime:
            modified.append(file)
    
    return modified


# ---------------------------------------------------------
# using class and static methods just to act like a 
# file-local "namespace" to keep everything in one module

class Tracker:
    @staticmethod
    def create():
        return {}

    @staticmethod
    def files(tracker):
        return list(tracker)

    @staticmethod
    def add(tracker, file):
        return Tracker.update(tracker, file)

    @staticmethod
    def remove(tracker, file):
        tracker = copy(tracker)
        del tracker[file]
        return tracker

    @staticmethod
    def update(tracker, file):
        tracker = copy(tracker)
        modts = _mod_ts(file)
        tracker[file] = modts
        return tracker

    @staticmethod
    def get_mtime(tracker, file):
        return tracker[file]


# ---------------------------------------------------------
def _mod_ts(file):
    return int(getmtime(file))
