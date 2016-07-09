#! /bin/bash

if ! pgrep -f "whatsie" >/dev/null 2>&1
then
  ps -ef | awk '/conky_notifs/{print $2}' | xargs kill
  ps -ef | awk '/dbus-mon.py/{print $2}' | xargs kill
fi
