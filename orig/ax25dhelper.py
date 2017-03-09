#! /usr/bin/env python

import sys
from logging import getLogger

log = getLogger(__name__)


class AX25dConnection(object):
    """
    AX25 Connection class
    Helps with IO on AX25 or
    console sessions
    """
    eol = "\r"


    def __init__(self, eol="\r"):
        self.eol = eol


    def send(self, msg, eol=True):
        sys.stdout.write(msg)
        if eol:
            sys.stdout.write(self.eol)


    def xmit(self):
        sys.stdout.flush()


    def recv(self, asblock=False):
        msg = ""
        line = ""
        while True:
            c = sys.stdin.read(1)
            if c == self.eol:
                if asblock:
                    if line == "/EX":
                        return msg
                    else:
                        line = ""
                else:
                    return msg
            msg = msg + c
            if c != self.eol:
                line = line + c

