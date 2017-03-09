#! /usr/bin/env python

import sys
import time
import feedparser

from ax25dhelper import AX25dConnection

def getnews(con):
    feed = feedparser.parse("http://www.kswo.com/category/216452/kpho-newstream?clienttype=rss")
    con.send("KSWO Local News - Latest 5 Headlines")
    for i in feed["items"][0:5]:
        con.send(i["title"])
    con.xmit()

def mainloop(con):
    while True:
        cmd = con.recv()
        if cmd == "quit":
            sys.exit()
        if cmd == "help":
            con.send("quit    - exit and disconnect")
            con.send("news    - display headlines")
            con.send("help    - display this help text")
            con.xmit()
        if cmd == "news":
            getnews(con)


if __name__ == "__main__":
    EOL = "\r"
    if sys.stdin.isatty():
        EOL = "\n"
    con = AX25dConnection(eol=EOL)
    con.send("hamshell v.1a")
    con.send("use the help command if you need it, quit to disconnect")
    con.xmit()
    mainloop(con)


