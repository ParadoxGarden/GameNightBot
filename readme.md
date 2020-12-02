Game Night Bot
=====

### Warning: This bot was designed to run on a very specific setup be prepared to ask "why would anybody do it like that"


For use:

- Replace anything in examplesettings.json with a $ in the line

- Rename it to settings.json

- deploy on a raspberry pi running ubuntu server

- cron job all the scripts to when you want functionality

Communication.py allows for per channel messaging through the terminal in this format
```
python3 Communication.py "$CHANNELNAME" "$MESSAGETOSEND"
```




uses many libraries, here are some links

[discord.py docs](https://discordpy.readthedocs.io/en/latest/index.html)

[discord.py api guide](https://discordpy.readthedocs.io/en/latest/api.html)

[pyttsx3](https://pyttsx3.readthedocs.io/en/latest/)

[ffmpeg](https://ffmpeg.zeranoe.com/builds/)

[espeak](http://espeak.sourceforge.net/)