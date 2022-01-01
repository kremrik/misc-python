from copy import copy
from fnmatch import fnmatch
from os import walk
from os.path import getmtime, join


class Watch:
    def __init__(
        self,
        path=".",
        ignore_dirs=(),
        ignore_files=(),
    ) -> None:
        self.path = path if path else "."
        self.ignore_dirs = ignore_dirs
        self.ignore_files = ignore_files

        self._tracker = self._make_tracker(
            self.path, self.ignore_dirs, self.ignore_files
        )
        self._created = []
        self._modified = []
        self._removed = []

    @property
    def files(self):
        return Tracker.files(self._tracker)

    @property
    def created(self):
        new = new_files(self._tracker, self._all_files())
        self._created = new
        return self._created

    @property
    def modified(self):
        mod = modified_files(self._tracker, self._all_files())
        self._modified = mod
        return self._modified

    @property
    def removed(self):
        rmd = removed_files(self._tracker, self._all_files())
        self._removed = rmd
        return self._removed

    def ack(self):
        for file in self._created:
            self._tracker = Tracker.add(self._tracker, file)
            self._created = []
        for file in self._modified:
            self._tracker = Tracker.update(self._tracker, file)
            self._modified = []
        for file in self._removed:
            self._tracker = Tracker.remove(self._tracker, file)
            self._removed = []

    @staticmethod
    def _make_tracker(path, ignore_dirs, ignore_files):
        tracker = Tracker.create()
        all = list_files(path, ignore_dirs, ignore_files)
        for file in all:
            tracker = Tracker.add(tracker, file)
        return tracker

    def _all_files(self):
        return list_files(
            self.path, self.ignore_dirs, self.ignore_files
        )


# ---------------------------------------------------------
def list_files(
    path=".", ignore_dirs=(), ignore_files=()
):
    for root, dirs, files in walk(path):
        dirs_c = copy(dirs)
        for dir in dirs_c:
            for patt in ignore_dirs:
                if fnmatch(dir, patt):
                    dirs.remove(dir)
        files_c = copy(files)
        for file in files_c:
            for patt in ignore_files:
                if fnmatch(file, patt):
                    files.remove(file)

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
