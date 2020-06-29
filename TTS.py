import pyttsx3


def init_voice():
    # SAPI5 for windows
    # espeak for ubuntu
    engine = pyttsx3.init(driverName="sapi5")
    return engine


def voice_testing():
    engine = pyttsx3.init(driverName="sapi5")  # object creation

    """ RATE"""
    rate = engine.getProperty('rate')  # getting details of current speaking rate
    print(rate)  # printing current voice rate
    engine.setProperty('rate', 125)  # setting up new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')  # getting to know current volume level (min=0 and max=1)
    print(volume)  # printing current volume level
    engine.setProperty('volume', 1.0)  # setting up volume level  between 0 and 1

    """VOICE"""
    voices = engine.getProperty('voices')  # getting details of current voice
    print(voices)
    engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
    # engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    engine.say("Hello World!")
    engine.say('My current speaking rate is ' + str(rate))
    engine.runAndWait()
    engine.stop()


def print_voice_info():
    engine = pyttsx3.init()  # object creation
    voices = engine.getProperty('voices')  # getting details of current voice
    for voice in voices:
        print(voice.name)


if __name__ == '__main__':
    print_voice_info()
    voice_testing()
