from copy import copy
from fnmatch import fnmatch
from typing import Dict
from os import walk
from os.path import abspath, getmtime, join


FileName = str
ModTS = int
Files = Dict[FileName, ModTS]


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

        self._tracker = self._all_files()
        self._created: Files = {}
        self._modified: Files = {}
        self._removed: Files = {}

    @property
    def files(self):
        return list(self._tracker)

    @property
    def created(self):
        new = new_files(self._tracker, self._all_files())
        self._created = new
        return list(self._created)

    @property
    def modified(self):
        mod = modified_files(
            self._tracker, self._all_files()
        )
        self._modified = mod
        return list(self._modified)

    @property
    def removed(self):
        rmd = removed_files(
            self._tracker, self._all_files()
        )
        self._removed = rmd
        return list(self._removed)

    def ack(self):
        for file, ts in self._created.items():
            self._tracker[file] = ts
            self._created = {}
        for file, ts in self._modified.items():
            self._tracker[file] = ts
            self._modified = {}
        for file, ts in self._removed.items():
            del self._tracker[file]
            self._removed = {}

    def _all_files(self):
        all = all_files(
            self.path, self.ignore_dirs, self.ignore_files
        )
        return all


# ---------------------------------------------------------
def new_files(tracker: Files, all: Files) -> Files:
    return {
        file: ts
        for file, ts in all.items()
        if file not in tracker
    }


def removed_files(tracker: Files, all: Files) -> Files:
    return {
        file: ts
        for file, ts in tracker.items()
        if file not in all
    }


def modified_files(tracker: Files, all: Files) -> Files:
    modified = {}
    for file, trk_ts in tracker.items():
        cur_ts = all[file]
        if cur_ts != trk_ts:
            modified[file] = cur_ts
    return modified


# ---------------------------------------------------------
def all_files(
    path=".", ignore_dirs=(), ignore_files=()
) -> Files:
    def _list_gen():
        nonlocal path
        for root, dirs, files in walk(path):
            # TODO: needs some DRYing up
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

            for file in files:
                path = abspath(join(root, file))
                modts = _mod_ts(path)
                yield (path, modts)

    return dict(_list_gen())


# ---------------------------------------------------------
def _mod_ts(file):
    return int(getmtime(file))
