#!/bin/sh
# Uses xwinwrap to display given animated .gif in the center of the screen

if [ $# -ne 1 ]; then
echo 1>&2 Usage: $0 image.gif
exit 1
fi

#get screen resolution
#SCRH=`xrandr | awk '/current/ { print $8 }'`
SCRH=1920
SCRW=1080
SCRW=${SCRW%\,}

#get gif resolution
IMGHW=`gifsicle --info $1 | awk '/logical/ { print $3 }'`
IMGH=${IMGHW%x*}
IMGW=${IMGHW#*x}

#calculate position
POSH=$((($SCRH/2)-($IMGH/2)))
POSW=$((($SCRW/2)-($IMGW/2)))

xwinwrap -g ${IMGHW}+${POSH}+${POSW} -ov -ni -s -nf -b -sh circle -- gifview -w WID $1 -a

exit 0
