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

cur_cond = wcr['current_conditions']
forcast = wcr['forecasts']
wind = cur_cond['wind']

sunrise = re.sub(r'[A-Z]', '', forcast[0]['sunrise']).split(':')
sunr_time = now.replace(hour=int(sunrise[0]), minute=int(sunrise[1]))
sunset = re.sub(r'[A-Z]', '', forcast[0]['sunset']).split(':')
suns_time = now.replace(hour=(int(sunset[0]) + 12), minute=int(sunset[1]))

forecasts_ready = []

# pp.pprint(wcr)

def isDay():
    if now >= suns_time or now <= sunr_time:
        return False
    elif sunr_time <= now <= suns_time:
        return True

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
    if val and size != '':
        return '${font ' + ffam + ':pixelsize=' + size + '}' + str(val) + '${font}'
    else:
        return str(val)
    return '${font' + ffam + size + '}'


wtr = {
        'TMP' : cur_cond['temperature'] + '°C',
        'HUM' : cur_cond['humidity'] + '%',
        'FLK' : cur_cond['feels_like'] + '°C',
        'TXT' : cur_cond['text'].lower().replace(' ', ''),
        'BAR' : cur_cond['barometer']['reading'] + 'mb',
        'DEW' : cur_cond['dewpoint'] + '°C',
        'WND' : wind['speed'] + ' km/h' + ' from ' + wind['text'],
        'BEU' : pywapi.wind_beaufort_scale(wind['speed']),
        'CPR' : forcast[0]['day']['chance_precip'] + '%'
        }

for elements in forcast:
    forecasts_ready.append(elements['day_of_week'][:3] + ' '\
            + elements['high'] + ' '\
            + elements['low'] + ' '\
            + elements['day']['brief_text'])
# pp.pprint(forecasts_ready)


def main():
    pp.pprint(wtr)

    # with open(curcond_file, '+w') as cf:
    #     for elem in wtr:
    #         cf.write(str(elem) + '\n')
    # with open(forecast_file, '+w') as ff:
    #     for elem in forecasts_ready:
    #         ff.write(str(elem) + '\n')

if __name__ == '__main__':
    main()
