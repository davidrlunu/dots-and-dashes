#! /bin/env/python

from gi.repository import GLib
import subprocess
import dbus
import datetime
import threading
import time
from dbus.mainloop.glib import DBusGMainLoop

messages = []
messages_map = {}
counter = 1
cco = 1

def curTime():
    ts =  datetime.datetime.timestamp(datetime.datetime.now())
    return ts


def timestampTodate(ts):
    return datetime.datetime.fromtimestamp(ts).strftime(' %H:%M ')

def winFocus():
    global cco
    global messages
    global messages_map

    while True:
        win_f = subprocess.Popen(['xdotool', 'getwindowfocus'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')[:-1]

        win_p = subprocess.Popen(['xdotool', 'getwindowpid', win_f], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')[:-1]

        path = '/proc/' + str(win_p) + '/comm'
        win_title = subprocess.Popen(['cat', path], stdout=subprocess.PIPE).communicate()[0].decode('utf-8')[:-1]
        # print(win_title)
        if win_title == 'whatsie':
            with open('/tmp/wa_notifications', 'w+') as f:
                print('TOTAL 0', file=f, flush=True)
            cco = 1
            messages = []
            messages_map = {}
        time.sleep(1)

def notifs(bus, message):
    global messages
    global messages_map
    global cco
    if message.get_member() == 'Notify':
        sender = message.get_args_list()[3][0:]

        if sender not in messages_map:
            messages_map.update({sender : len(messages)})
            messages.append({'sender' : sender, 'counter' : counter, 'date' : curTime()})
        else:
            m = messages[messages_map[sender]]
            m['counter'] += 1
            m['date'] = curTime()

        with open('/tmp/wa_notifications', 'w+') as f:
            print('TOTAL ' + str(cco), file=f, flush=True)
            for m in messages:
                print(
                        m['sender'][:10].ljust(10),\
                        m['counter'],\
                        '${color1}' + str(timestampTodate(m['date'])) + '${color}',\
                        file=f,\
                        flush=True
                        )

        cco += 1


if __name__ == '__main__':
    DBusGMainLoop(set_as_default=True)

    loop = GLib.MainLoop()

    bus = dbus.SessionBus()
    bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications'")
    bus.add_message_filter(notifs)

    threading.Thread(target=winFocus).start()
    loop.run()

