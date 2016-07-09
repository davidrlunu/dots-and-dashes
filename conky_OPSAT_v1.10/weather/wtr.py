#! /bin/env/python3
# vim: set fileencoding=UTF-8 :
import pywapi
import pprint as pp
import os
import re
import datetime

now = datetime.datetime.now()
wcr = pywapi.get_weather_from_weather_com('ITUM1307')
curcond_file = os.environ['HOME'] + '/.conky/weather/current_condition'
forecast_file = os.environ['HOME'] + '/.conky/weather/forecast'
icons_path = os.environ['HOME'] + '/.conky/weather/weather_icons/'
_icons_path = os.environ['HOME'] + '/.conky/weather/weather_icons/'

cur_cond = wcr['current_conditions']
forcast = wcr['forecasts']
wind = cur_cond['wind']

sunrise = re.sub(r'[A-Z]', '', forcast[0]['sunrise']).split(':')
sunr_time = now.replace(hour=int(sunrise[0]), minute=int(sunrise[1]))
sunset = re.sub(r'[A-Z]', '', forcast[0]['sunset']).split(':')
suns_time = now.replace(hour=(int(sunset[0]) + 12), minute=int(sunset[1]))

forecasts_ready = {}
days = []
high = []
lows = []
cond = []

# pp.pprint(wcr)

def isDay():
    if sunr_time <= now <= suns_time:
        return True
    return False

if isDay():
    icons_path += 'day/'
else:
    icons_path += 'night/'


def colorIt(color='', val=''):
    if val and color != '':
        return '${color ' + color + '}' + str(val) + '${color}'
    else:
        return str(val)
    return '${color' + color + '}'

def fontIt(ffam='', size='', val=''):
    if ffam != '':
        return '${font ' + ffam + ':pixelsize=' + size + '}' + str(val) + '${font}'
    else:
        return str(val)
    return '${font' + ffam + size + '}'

def imageIt(img='', posx='', posy='', sizew='', sizeh=''):
    if img != '':
        return '${image ' + img \
                + ' -p ' + str(posx) \
                + ',' + str(posy) \
                + ' -s ' + str(sizew) \
                + 'x' + str(sizeh) \
                + ' -n' + '}'


wtr = {
        'TMP' : cur_cond['temperature'] + '°',
        'HUM' : cur_cond['humidity'] + '%',
        'FLK' : cur_cond['feels_like'] + '°',
        'TXT' : cur_cond['text'].lower().replace(' ', ''),
        'BAR' : cur_cond['barometer']['reading'] + 'mb',
        'DEW' : cur_cond['dewpoint'] + '°C',
        'WND' : (wind['speed'] + ' km/h from ' + wind['text']) if wind['speed'] != 'calm' else wind['text'],
        'BEU' : pywapi.wind_beaufort_scale(wind['speed']),
        'CPR' : forcast[0]['day']['chance_precip'] + '%'
        }
wtr['ICO'] = icons_path + wtr['TXT'] + '.png'

for elements in forcast:
    days.append(elements['day_of_week'].upper()[:2])
    high.append(elements['high'] + '°')
    lows.append(elements['low'])
    cond.append(os.environ['HOME'] + '/.conky/weather/weather_icons/day/' + elements['day']['text'].lower().replace(' ', '') + '.png')
    cond[0] = os.environ['HOME'] + '/.conky/weather/weather_icons/day/' + wtr['TXT'] + '.png'


forecasts_ready.update({'days': days, 'highs': high, 'lows': lows, 'cond': cond})


def main():
    print('${color3}┌┈─                ─┈┐${color}')
    print('${voffset -5}' + '${goto 10}' + fontIt('DIN', '60', wtr['TMP']), imageIt(wtr['ICO'], 90, 30, 60, 60), \
            imageIt(_icons_path + 'temperature.png', 10, 103, 20, 20), \
            imageIt(_icons_path + 'humidity.png', 10, 130, 20, 20), \
            imageIt(_icons_path + 'barometer.png', 10, 160, 20, 20), \
            imageIt(_icons_path + 'dewpoint.png', 10, 185, 20, 20), \
            imageIt(_icons_path + 'chance_precip.png', 10, 215, 20, 20), \
            imageIt(_icons_path + 'wind_direction.png', 10, 245, 20, 20), \
            imageIt(_icons_path + 'sunrise.png', 10, 275, 20, 20), \
            imageIt(_icons_path + 'sunset.png', 10, 300, 20, 20))

    print('${goto 60}' + '${voffset 25}' + fontIt('Monospace', '12', wtr['FLK'] +\
            '\n' +\
            '\n' + '${goto 60}' + wtr['HUM'] +\
            '\n' +\
            '\n' + '${goto 60}' + wtr['BAR'] +\
            '\n' +\
            '\n' + '${goto 60}' + wtr['DEW'] +\
            '\n' +\
            '\n' + '${goto 60}' + wtr['CPR'] +\
            '\n' +\
            '\n' + '${goto 60}' + wtr['WND'] +\
            '\n' +\
            '\n' + '${goto 60}' + forcast[0]['sunrise'] +\
            '\n' +\
            '\n' + '${goto 60}' + forcast[0]['sunset'] +\
            '\n' +\
            '\n' +\
            '${color3}├─     FORECAST     ─┤' +\
            '\n' +\
            '\n' + '${goto 20}' + str('  '.join(forecasts_ready['days'])) +\
            '\n' +\
            '\n' + '${goto 20}' + str(' '.join(forecasts_ready['highs'])) + '${color}') +\
            '\n' +\
            # imageIt(forecasts_ready['cond'][0], 15, 270, 15, 15) +\
            imageIt(forecasts_ready['cond'][0], 15, 410, 15, 15) +\
            imageIt(forecasts_ready['cond'][1], 43, 410, 15, 15) +\
            imageIt(forecasts_ready['cond'][2], 72, 410, 15, 15) +\
            imageIt(forecasts_ready['cond'][3], 101, 410, 15, 15) +\
            imageIt(forecasts_ready['cond'][4], 129, 410, 15, 15) +\
            '\n')
    print('${color3}└┈─                ─┈┘${color}')



if __name__ == '__main__':
    main()
