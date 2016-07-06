#! /usr/bin/python3
# vim: set fileencoding=UTF-8 :

# pycal is a calendar viewr made for being integratred with conky
import sys
import math
import os.path, time
import calendar
import datetime
import uuid
import json
try:
    import config
except ImportError:
    print('Could not find config file')
    sys.exit(1)

now = datetime.datetime.now()
year = now.year
month = now.month
day = now.day

#User configs grabbed from config.py
_grid = config.grid
_date_separator = config.date_separator
_date_format = config.date_format
_db_path = os.environ['HOME'] + config.db_path
_ignore_cache = config.ignore_cache
_note_length = config.note_length
_previous_notes = config.previous_notes
_max_notes = config.max_notes

_color_header = config.color_header if hasattr(config, 'color_header') else ''
_color_grid = config.color_grid if hasattr(config, 'color_grid') else ''
_color_currday = config.color_currday if hasattr(config, 'color_currday') else ''
_color_event = config.color_event if hasattr(config, 'color_event') else ''
_color_pevent = config.color_pevent if hasattr(config, 'color_pevent') else ''


#Routine that serves the purpose of checking if the cacheing is active or not.
def isCached(file_path):
    if _ignore_cache:
        return False
    try:
        timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime(_date_format)
        return now.strftime(_date_format) == timestamp
    except OSError:
        return False


# Date validation based on input, controlling if the elements forming the date are in the right order.

def validDate(date_string):
    try:
        datetime.datetime.strptime(date_string, _date_format)
    except ValueError:
        print("Date should be DD/MM/YYYY")
        return False
    return True


# Function that colors various elements in the stamp process.
def colorIt(color='', val=''):
    if val and color != '':
        return '${color ' + color + '}' + str(val) + '${color}'
    else:
        return str(val)
    return '${color'+color+'}'

# Given a date under the form of string '01/01/2000', transform it in a list ['01', '01', '2000']
def parseDate(date=''):
    return date.split(_date_separator)


# Tranforms a date under the form of a list ['01', '01', '2000'] into a unified, reverted string
# padding it with '0' if 'day' or 'month' are single digit numbers
def uniDate(dateList):
    return ''.join([str(v).rjust(2, '0') for v in dateList[::-1]])


# Self explanotory function :^)
def compareDates(actual_date, date_from_db):
    if len(actual_date) == len(date_from_db) == 3:
        for i in range(3):
            if str(actual_date[i]) != str(date_from_db[i]):
                return False
        return True
    return False


# Read the JSON database where the events are saved and return a list of objects from it.
def dbRead():
    try:
        with open(_db_path) as fileread:
            return json.load(fileread)
    except IOError:
        return []

today = uniDate([day, month, year])
# dblist will always be a list of objects now
dblist = dbRead()


# Calendar stamp routine. This fucntion takes month and year as arguments and stamps the calendar for
# the given 'm' and y'
def updateCalendar(m=month, y=year):
    m = int(m)
    y = int(y)
    # 'cal' returns a list[calendar of the month] of lists[weeks of the calendar]
    cal = calendar.monthcalendar(y, m)
    m_name = calendar.month_name[m]
    w_header = calendar.weekheader(2)

    # We use a string 'str_calendar' to manipulate the output from 'cal' because it is easier to elaborate
    # elements from a list and concatenate a string rather than appending to another list.
    str_calendar = ''
    str_calendar += colorIt(_color_header, '│' + str(y).center(20, ' ') + '│') + '\n'
    str_calendar += colorIt(_color_header, '│' + m_name.center(20, ' ').upper() + '│') + '\n'
    str_calendar += colorIt(_color_header, '│' + w_header.upper() + '│') + '\n'
    if _grid:
        str_calendar += colorIt(_color_grid, '├─ ┼  ┼  ┼  ┼  ┼  ┼ ─┤') + '\n'
    else:
        str_calendar += colorIt(_color_grid, '└────────────────────┘') + '\n'


    # We start parsing the [cal[we..][..ek]] calendar
    for rows, cols in enumerate(cal):
        l1 = []
        day = now.day
        current_date = [str(day), str(month), str(year)]
        for n in cols:
            n = '' if n==0 else n
            # Pad single digit dates
            n_pad = str(n).rjust(2)
            # Here we start checking for events in the database, to be displayed in the calendar
            for event in dblist:
                if not n:
                    break
                # At every cycle, we parse the [date] from the db into a 'date':
                # if the date is past, color it with the color chose by the user in the config file
                # if the date is the same as the current day (a.k.a event today) then mark it with a 'X'
                datel = parseDate(event['date'])
                if uniDate(datel) < uniDate(current_date):
                    n = colorIt(_color_pevent, n_pad) if compareDates([n,m,y], datel) else n
                if uniDate(datel) == uniDate(current_date):
                    n = colorIt(_color_pevent, 'X') if compareDates([n,m,y], datel) else n

                n = colorIt(_color_event, n_pad) if compareDates([n,m,y], datel) else n
            n = colorIt(_color_currday, n_pad) if n==day and m==month and y==year else n
            n = str(n).rjust(2)
            l1.append(n)

        if _grid:
            str_calendar += colorIt(_color_grid, '│') + ' '.join(map(str,l1)) + colorIt(_color_grid, '│') + '\n'
        else:
            str_calendar += ' ' + ' '.join(map(str,l1)) + '\n'

        if rows != (len(cal)-1) and _grid:
            str_calendar += colorIt(_color_grid, '├──┼──┼──┼──┼──┼──┼──┤') + '\n'
        elif not _grid:
            str_calendar += '\n'

    if _grid:
        str_calendar += colorIt(_color_grid, '╰──┴──┴──┴──┴──┴──┴──╯') + '\n'

    if not _ignore_cache:
        with open('/tmp/calendar', 'w+') as calendar_stamp:
            calendar_stamp.write(str_calendar)
    print(str_calendar)





def saveEvent(arguments, _flag = False):

    _date = _note = stringed_list = ''
    _id = str(uuid.uuid4())[:4]

    for i, arg in enumerate(arguments):
        if i == 0:
            _date = arg
            _date_array = parseDate(_date)
            _date_len = len(_date_array)

            if _date_len == 1:
                _date += _date_separator + str(month) + _date_separator + str(year)
            if _date_len == 2:
                _date += _date_separator + str(year)
            if not validDate(_date):
                sys.exit(2)

        elif i == 1:
            _note = arg
        elif i == 2:
            _id = arg
        else:
            print("Too many args")
            sys.exit(2)



    new_date = uniDate(_date.split(_date_separator))

    index = 0
    global dblist

    for obj in dblist:
        current_date = uniDate(obj["date"].split(_date_separator))
        if new_date < current_date:
            break

        index += 1

    event = { "date": _date, "note": _note, "id": _id}
    if _flag:
        event.update({"important": _flag})
    print("Insert to index: ", index)
    dblist.insert(index, event)


    json_list = json.dumps(dblist)
    with open(_db_path, 'w') as filesave:
        json.dump(dblist, filesave, sort_keys=True, indent=4, ensure_ascii=False)
        print("Saved to DB : " + '{0:}  {1:}  {2:}'.format(_date, _note, str(_id)))



def editEvent(changeid):
    global dblist
    index = 0
    for obj in dblist:
        current_date = uniDate(obj["date"].split(_date_separator))
        if changeid == obj['id']:
            edit_choice = input("Want to change this event's:\n"\
                    + '[1] Note: ' + str(obj['note'][:30]) + '....' + '\n'\
                    + '[2] Date: ' + str(obj['date']) + '\n'\
                    + '[3] Mark / Unmark as important: ' + '\n')
            if edit_choice == '1':
                notes = obj['note']
                new_note = str(input("Change old note:    « "\
                        + str(obj['note'][:30])\
                        + " »    to new note:\n"))
                obj['note'] = new_note
                print("New note updated")
                break

            elif edit_choice == '2':
                obj['date'] = input("Change old date    « "\
                        + str(obj['date'])\
                        + " »    into new date\n")
                if validDate(obj['date']):
                    temp_obj = dblist.pop(index)
                    saveEvent([obj['date'], obj['note'], obj['id']])
                    print("New date updated")
                    sys.exit(2)
            elif edit_choice == '3':
                if 'important' in obj:
                    obj.pop("important", None)
                else:
                    obj.update({"important": True})

        index += 1

    json_list = json.dumps(dblist)
    with open(_db_path, 'w') as filesave:
        json.dump(dblist, filesave, sort_keys=True, indent=4, ensure_ascii=False)


def rmEvent(id_mod):
    global dblist
    index = 0
    for event in dblist:
        if id_mod == event['id']:
            dblist.pop(index)
        index += 1
    with open(_db_path, 'w') as fileup:
        json.dump(dblist, fileup, sort_keys=True, indent=4, ensure_ascii=False)
        print("Updating DB")



# This method serves the purpose of calculating how long a 'note' of an event is, in order to break it into
# new lines, every '_note_length' characters, where '_note_length' is defined by the user.
def spezNote(note, first_note):

    n_rows = math.ceil(len(note) / _note_length)
    note_full = ''
    padder = 14

    for row_index in range(1, n_rows + 1):
        frm = (row_index - 1) * _note_length
        to = frm + _note_length
        note_partial = note[frm:to]
        if not (first_note and row_index == 1):
            padder = 23 if row_index > 1 else padder
            note_partial = '\n' + note_partial.rjust(padder + len(note_partial))
        note_full += note_partial

    return note_full


def updateEvents():

    eventlist = ''
    temp_notes = []
    note_count = 0

    for eventIndex, event in enumerate(dblist):

        willChange = False
        last = eventIndex == (len(dblist) - 1);
        if not last:
            willChange = uniDate(dblist[eventIndex + 1]["date"].split(_date_separator))\
                    > uniDate(event["date"].split(_date_separator))


        # printable IF is important AND in range, IF date is > today's date
        #valid_p stands for valid printable

        valid_p = eventIndex + _previous_notes
        printable = valid_p < len(dblist)\
                and uniDate(dblist[valid_p]["date"].split(_date_separator))\
                >= today and 'important' in event\
                and event['important'] == True\
                or uniDate(event["date"].split(_date_separator))\
                > today

        if printable:
            temp_notes.append('[ ' + event['id'] + ' ] ' + event["note"])
            note_count += 1

        # check if _max_notes is reached
        note_overflow = note_count >= _max_notes

        # added len(temp_notes) to check if there are things to display actually
        if (willChange or last or note_overflow) and len(temp_notes):
            note_full = ''
            for note in temp_notes:
                note_full += spezNote(note, note == temp_notes[0])
                if note != temp_notes[len(temp_notes) - 1]:
                    note_full += '\n'

            d_parse = parseDate(event['date'])
            d_parse = d_parse[0].rjust(2, '0')\
                    + _date_separator + d_parse[1].rjust(2, '0')\
                    + _date_separator + d_parse[2]

            eventlist += '[ ' + colorIt(_color_event, d_parse) + ' ]' + note_full


            if event != dblist[len(dblist) - 1]:
                eventlist += '\n'

            # break loop if _max_notes is reached
            if note_overflow:
                break;

            temp_notes = []



    if not _ignore_cache:
        try:
            with open('/tmp/eventlist', 'w+') as tmpfile:
                    tmpfile.write(eventlist)
        except IOError:
            return

    print(eventlist)




def main(argv):

    option = ''
    flag = False
    arguments = []

    for i, arg in enumerate(argv):
        if i == 0:
            option = arg
        else:
            arguments.append(arg)



    if option == '':
        option = '-c'

    if option == '-c':
        if len(arguments) == 0:

            if not isCached('/tmp/calendar'):
                updateCalendar()
            else:
                with open('/tmp/calendar', 'r') as calendar_stamp:
                    print(calendar_stamp.read())

            sys.exit(2)
        else:

            marg_array = arg.split(',')
            for marg in marg_array:
                my_array = marg.split(':')
                m = my_array[0]
                y = my_array[1] if len(my_array)==2 else year

                temp_date = '1' + _date_separator + str(m) + _date_separator + str(y);


                if(validDate(temp_date)):
                    updateCalendar(m,y)
            sys.exit(0)

    elif option == '-t':
        if not isCached('/tmp/eventlist'):
            updateEvents()
        else:
            with open('/tmp/eventlist', 'r') as eventlist_stamp:
                print(eventlist_stamp.read())

        sys.exit(2)

    elif option == '-e':
        if len(arguments) == 0:
            print('Please add an event in the form: DD/[MM]/[YYYY] "Note of the event"')
            sys.exit(0)
        if arguments[0] == '--important':
            flag = True
            arguments = arguments[1:]
        saveEvent(arguments, flag)
        updateEvents()
        updateCalendar()

    elif option == '-m':
        if len(arguments) == 0:
            sys.exit(0)
        else:
            id_mod = ''.join(arguments)
            editEvent(id_mod)

    elif option == '-d':
        yes = set(['yes', 'y', 'Y', 'ye', 'YES'])
        no = set(['n', 'N', 'No', 'NO', 'nope', ''])
        if len(arguments) == 0:
            choice = input('Remove entire DB?\n[y/N]')
            if choice in yes:
                os.remove(_db_path)
            elif choice in no:
                sys.exit(2)
            else:
                sys.stdout.write('Please answer with one of: ' + str(yes) + ' or ' + str(no) + '\n')
        else:
            id_parse = ''.join(arguments)
            rmEvent(id_parse)


    elif option == 'h' or '--help':
        print("\n\
        \n\
        Usage: pycal <option> [args]\n\
        \n\
        Also, consult the documented config file for more tunings.\n\
        \n\
        OPTIONS:\n\
        \n\
        -c :  Prints a calendar based on given arguments.\n\
              \n\
              arg <none>             Print the current month;\n\
              arg <month>            Print the calendar for <month> number;\n\
              arg <month>,<month>,.. Print a list of calendar for each <month> sepcified;\n\
              arg <month>:<year>,..  Print the calendar or list of calendars for specified <month> and <year>.\n\
                                          \n\
                                          \n\
        -e :  Save event in the database and add optional note to it.\n\
              \n\
              arg <date> Saves a day[/<month>/<year>] in the database, print it on the calendar\n\
                                                      and print it in the conky (if used);\n\
                  <date> [<comment>] Add note in the form [<date> 'COMMENT'] to the <date> you want to save;\n\
                  \n\
                  flag <--important> <date>[<comment>] Save the event as important. Important events\n\
                                                       will be always displayed in the [-t] option even if \n\
                                                       they are passed.\n\
              \n\
              \n\
        -m :  Wizard to modify an event based on it's ID.\n\
              arg <id>;\n\
              \n\
              \n\
        -d :  Remove event based on it's id or entire database.\n\
              arg <none> Remove entire db;\n\
              arg <id> Remove event[id].\n\
              \n\
              \n\
        -t :  Display the notes in the db.")

if __name__ == "__main__":
    main(sys.argv[1:])
