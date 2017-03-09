#! /usr/bin/env python

import os, sys
from ax25dhelper import AX25dConnection
import logging
import logging.handlers
import json

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')

formatter = logging.Formatter('%(module)s.%(funcName)s: %(message)s')
handler.setFormatter(formatter)

log.addHandler(handler)

msgp = os.path.expanduser("~/PBBS.json")

msgd = dict(
    serial=0,
    messages=[]
    )

def mainloop(con, lcall, rcall):
    while True:
        if lcall == rcall:
            con.send("ENTER COMMAND:  B,K,L,R,S, or Help> ", eol=False)
        else:
            con.send("ENTER COMMAND:  B,S, or Help> ", eol=False)
        con.xmit()
        cmd = con.recv().lower()
        if cmd == "b":
            sys.exit()
        if cmd == "h" or cmd == "help":
            con.send("H               - display help")
            con.send("B               - exit and disconnect")
            con.send("S <callsign>    - send a message")
            if rcall == lcall:
                con.send("L               - list messages")
                con.send("K <msg number>  - delete message")
                con.send("R <msg number>  - read message")
            con.send("")
            con.xmit()
        if cmd == "s" or cmd == "s %s" % lcall.lower():
            send_message(con, rcall)
        if cmd == "l" and rcall == lcall:
            list_messages(con)
        if cmd.startswith("r ") and rcall == lcall:
            parts = cmd.split(" ")
            if len(parts) == 2:
                read_message(con, int(parts[1]))
        if cmd.startswith("k ") and rcall == lcall:
            parts = cmd.split(" ")
            if len(parts) == 2:
                kill_message(con, int(parts[1]))


def kill_message(con, msgnum):
    d = load_data()
    new_msglist = list()
    for m in d['messages']:
        if m['serial'] != msgnum:
            new_msglist.append(m)
    d['messages'] = new_msglist
    write_data(d)


def read_message(con, msgnum):
    d = load_data()
    for m in d['messages']:
        if m['serial'] == msgnum:
            con.send("From: %s" % m['rcall'])
            con.send("Subject: %s" % m['subject'])
            con.send("")
            message = ""
            if sys.stdin.isatty():
                message = m['msg'].replace("\r", "\n")
            else:
                message = m['msg'].replace("\n", "\r")
            con.send(message)
            con.xmit()


def list_messages(con):
    d = load_data()
    for m in d['messages']:
        con.send("%s %s: %s" %(str(m['serial']), m['rcall'], m['subject']))
    con.xmit()


def send_message(con, rcall):
    con.send("Subject: ", eol=False)
    con.xmit()
    subject = con.recv()
    con.send("Enter message - enter /EX on it's own line to end the message")
    con.xmit()
    message = con.recv(asblock=True)
    save_message(rcall, subject, message)
    con.send("Message Saved.")


def setup():
    if not os.path.exists(msgp):
        write_data(msgd)


def load_data():
    f = open(msgp, "r")
    d = json.loads(con.eol.join(f.readlines()))
    f.close()
    return d


def write_data(d):
    f = open(msgp, "w")
    f.write(json.dumps(d))
    f.close()


def save_message(rcall, subject, msg):
    d = load_data()
    d['serial'] = d['serial'] + 1
    d['messages'].append(dict(
        serial = d['serial'],
        rcall = rcall,
        subject = subject,
        msg = msg
        ))
    write_data(d)


if __name__ == "__main__":
    log.debug(sys.argv)
    if not len(sys.argv) > 3:
        log.fatal("Not enough arguments")
        sys.exit(1)
    lcall = sys.argv[1].upper()
    rcall = sys.argv[2].upper()
    descr = " ".join(sys.argv[3:])

    EOL = "\r"
    if sys.stdin.isatty():
        EOL = "\n"

    setup()

    con = AX25dConnection(eol=EOL)
    con.send("pbbs.py v0.1a")
    con.send(descr)
    con.xmit()
    mainloop(con, lcall, rcall)

