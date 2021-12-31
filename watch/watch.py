from copy import copy
from os import walk
from os.path import getmtime, join


IGNORE_PREFIXES = ["_", "."]


class Watch:
    def __init__(self, path = None) -> None:
        self.path = path if path else "."
        self.tracker = self._make_tracker(self.path)
        self._created = []
        self._modified = []
        self._removed = []

    @property
    def created(self):
        all = list(list_files(self.path))
        new = new_files(self.tracker, all)
        self._created = new
        return self._created

    @property
    def modified(self):
        all = list(list_files(self.path))
        mod = modified_files(self.tracker, all)
        self._modified = mod
        return self._modified

    @property
    def removed(self):
        all = list(list_files(self.path))
        rmd = removed_files(self.tracker, all)
        self._removed = rmd
        return self._removed

    def ack(self):
        for file in self._created:
            self.tracker = Tracker.add(self.tracker, file)
        for file in self._modified:
            self.tracker = Tracker.update(self.tracker, file)
        for file in self._removed:
            self.tracker = Tracker.remove(self.tracker, file)

    @staticmethod
    def _make_tracker(path):
        tracker = Tracker.create()
        all = list(list_files(path))
        for file in all:
            tracker = Tracker.add(tracker, file)
        return tracker


# ---------------------------------------------------------
def list_files(path = None):
    if not path:
        path = "."

    for root, dirs, files in walk(path):
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
