#!/usr/bin/env python

import os, sys, hashlib

BUF_SIZE = 1024*8

class DirScanner(object):
    def __init__(self, path=None, absolute=False, stripdot=False):
        if not path: path = '.'
        if not os.path.exists(path): raise IOError('path %s doesn\'t exist' % path)
        self.path = os.path.abspath(path) if absolute else path
        self.absolute = absolute
        self.stripdot = stripdot
        return

    def md5sum(self, f):
        ''' md5sums a file, returning the hex digest

            Parameters:
                - f     filename string
        '''
        m = hashlib.md5()
        fh = open(f, 'r')
        while 1:
            chunk = fh.read(BUF_SIZE)
            if not chunk: break
            m.update(chunk)
        fh.close()
        return m.hexdigest()

    def iteritems(self, path=None, want_files=True, want_dirs=True, func=None, filt=None):
        ''' streaming item iterator that can optionally run a function / filter function on each item (files/dirs)

            Parameters:
                - path          path to iterate on (note: this is called recursively)
                - want_files    True if you want file results in the iteration, False if you don't
                - want_dirs     True if you want directory results in the iteration, False if you don't
                - func          function to run on each (this will cause the return output to expand to a list of tuples)
                - filt          filter function - only iterates on files when filt(absolute_filename) == True
        '''
        if path is None: iter_path = self.path
        else:            iter_path = path

        for f in os.listdir(iter_path):
            if f[0] == '.': continue

            ## f (filename) -> af (absolute filename)
            if self.absolute: af = os.path.abspath( os.path.join(iter_path, f) )
            else:             af = os.path.join(iter_path, f)

            ## filter out stuff we don't want
            if filt and not filt(af): continue

            ## detect broken path strings
            if not os.path.exists(af): raise IOError('bad path: %s' % af)

            ## return our main response
            if ( os.path.isfile(af) and want_files ) or ( os.path.isdir(af) and want_dirs ):
                if self.stripdot and af[:2] == './': af = af[2:]
                if func: yield ( func(af), af )
                else:    yield af

            ## recurse & return for sub-dirs
            if os.path.isdir(af):
                for x in self.iteritems(path       = af,
                                        want_files = want_files,
                                        want_dirs  = want_dirs,
                                        func       = func,
                                        filt       = filt): yield x

    def iterdupes(self, compare=None, filt=None):
        ''' streaming item iterator with low overhead duplicate file detection

            Parameters:
                - compare       compare function between files (defaults to md5sum)
        '''
        if not compare: compare = self.md5sum
        seen_siz = {}       ## store size   -> first seen filename
        seen_sum = {}       ## store chksum -> first seen filename
        size_func = lambda x: os.stat(x).st_size
        for (fsize, f) in self.iteritems(want_dirs=False, func=size_func, filt=filt):
            if fsize not in seen_siz:    ## state 1: no previous size collisions
                seen_siz[fsize] = f
                continue
            else:
                if seen_siz[fsize]:      ## state 2: defined key => str (initial, unscanned path)
                    chksum = compare(seen_siz[fsize])
                    if chksum in seen_sum:  yield (chksum, seen_siz[fsize])
                    else:                   seen_sum[chksum] = seen_siz[fsize]
                    seen_siz[fsize] = None

                ## state 3: defined key => None (already scanned path, no-op)
                chksum = compare(f)
                if chksum in seen_sum:
                    ## if it's a dupe, check if the first one was ever yielded then yield
                    if seen_sum[chksum]:
                        yield (chksum, seen_sum[chksum])
                        seen_sum[chksum] = None
                    yield (chksum, f)
                else:
                    ## if not, set the initial filename
                    seen_sum[chksum] = f


if __name__ == '__main__':
    ls = DirScanner()
    for item in ls.iteritems(): print(item)
