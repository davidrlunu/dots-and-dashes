Yeah, right

This is a conky interface  with a bit of py and sh here and there.
Got inspo from various vidya and films for creating this and it's projected to be rendered on a 1920x1080 display.
If you have greater or lower resolution, please feel free to adapt it for your needs.

It uses a color scheme of a maximum of three colors (including all the images) so it is easy to change it as you prefer  with a maximum of three lines of bash.
 
Please explore the directories and even read carefuly *ALL* the configuration files. 

Features:

1. Calendar... One day i felt like re-inventig hot-water so there it is. What is so special about this calendar? The fact that you can mark days to be displayed in the calendar and the option to associate notes to them;

2. A weather widget full of info and forecast. For this one you will need to «pip install pywapi»; 

3. Speedtest infos, which you will need to 'pip install speedtest-cli' in order to make it work.

4. A dbus-monitor i made in python ( reinventing hot-water yet again ) which serves the purpose of collecting notifications from "whatsie" - a WhatsApp Web client for Desktop, created by talented https://github.com/Aluxian/Whatsie - and pipe the «Sender» to the conky.

5. Awesome wallpaper and awesome HUD designed by me :) 


How it werks: 

Everything inside 'conky_OPSAT' directory, should go into '/home/youruser/.conky/' and you are ready to go.
If you encounter conky files not working with the default settings, try exporting your $USER to the enviornment as every path in the conky files has '/home/$USER/..' as path.


Let's talk about the reddundant / optional features: 

a. Images inside 'conky_OPSAT' directory (except the conky_weather_icons ) serve the sole purpose of ricing. If you feel like you don't mind a less than awesome desktop, feel free to get rid of them.

b. The spinning gif in the middle of the screen, it'salso 100% eye-candy and fireworks. If you have a low end machine i strongly recommend you to make less than using '.gifbg' script.

c. The calendar per se, it just werks but if you don't want all the unicode-art, please read the documentation of it. I like to think that i covered pretty much every customization preference. 

d. The whatsapp notification counter. I think this is the most optional feature.

e. inside the CPU histogram ring, there is a 2 pixel thin ring which serves *ME* to know the aproximative level of the sound volume. It resides in the 'cpu_rings.lua' file, just in case you want to get rid of it or find it odd.

That's it, enjoy! 

