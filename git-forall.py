#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import locale
import sys
import os
import subprocess


def _execute(cmd, cwd=None, env=os.environ.copy()):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=cwd, env=env)
    return p.stdout.read().decode(locale.getdefaultlocale()[1])

def get_git_dirs():
    dirs = list()
    for d in _execute('find . -type d -name ".git"').split('\n'):
        if len(d) < 3:
            continue
        dirs.append(d[2:len(d)-5])
    return dirs

def usage():
    print('usage:\n{} ARGS...'.format(__file__.split('/')[-1]), file=sys.stdout)

def main():
    if len(sys.argv) < 2:
        usage()
        return

    rootdir = os.getcwd()
    git_dirs = get_git_dirs()

    for d in git_dirs:
        env = os.environ.copy()
        env['REPO_PATH'] = d.encode()
        bufs = _execute(sys.argv[1:], cwd=os.path.join(rootdir, d),
                env=env).split('\n')
        if len(bufs) > 1:
            print('\n'.join(bufs[:len(bufs)-1]))

if __name__ == '__main__':
    main()
