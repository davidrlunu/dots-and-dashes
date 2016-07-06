#! /usr/bin/python3
# vim: set fileencoding=UTF-8 :

#Set True or False if you want grid calendar or plain text view.
grid = True
# grid = False

#Set colors you want to display in your calendar; You can use either hex codes or color names.
color_header = '494a5b'  #This is the color of the header containing year, month name and week day names
color_grid = '494a5b'    #This is the color of the grid elements (border and inner row separators
color_currday = 'a5adff' #This is the color of the current day to be displayed in the calendar
color_event = 'af2445' #This is the color of FUTURE events to come, to be displayed in the calendar
color_pevent = 'sienna'  #This is the color of PAST events to be shown on the calendar

#This variable sets the date separator in the context 01/01/2001 where "/" is the separator
date_separator = "/"

#The date format you prefer to use in the saving and viewing of the date
date_format = '%d' + date_separator + '%m' + date_separator + '%Y'

#The path to the database of events (preferably $HOME/.conky/calendar/event_db.json since this script
#is made for being integrated with conky
db_path = '/.conky/calendar/event_db.json'

#This variable determins whether the calendar view is cached or not.
#Recomended only in the case of multiple calendar months display (e.g. an entire year calendar)
ignore_cache = True

#The length of the note to display in the conky, based on the width of the conky window
# since conky is ignorant of the newline escape character
note_length = 40

#Previous notes and number of max notes to display.
# Hypothesis: You have previous notes of past events that by default are not displayed,
# unless the "important" flag is set at the moment of saving or editing of the event's date
# and you don't want to occupie reddundant space in the display of the notes with previous notes.
# In this case you would have a total of 5 notes to be displayed, which of, 2 are past «important» events.
previous_notes = 2
max_notes = 5
