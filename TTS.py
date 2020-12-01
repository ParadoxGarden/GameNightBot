import pyttsx3


def init_voice():
    # SAPI5 for windows
    # espeak for ubuntu
    engine = pyttsx3.init(driverName="sapi5")
    return engine


def voice_testing():
    engine = pyttsx3.init(driverName="sapi5")  # object creation

    """ RATE"""
    rate = engine.getProperty('rate')  # current speaking rate
    print(rate)
    engine.setProperty('rate', 125)  # setting new voice rate

    """VOLUME"""
    volume = engine.getProperty('volume')  # current volume level (min=0 and max=1)
    print(volume)
    engine.setProperty('volume', 1.0)  # setting volume level

    """VOICE"""
    voices = engine.getProperty('voices')  # voices

    engine.setProperty('voice', voices[1].id)  # changing index, changes voices. o for male
    # engine.setProperty('voice', voices[1].id)  # changing index, changes voices. 1 for female

    engine.say("Hello")
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
