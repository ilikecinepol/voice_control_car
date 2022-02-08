import time
import speech_recognition as sr
from fuzzywuzzy import fuzz
import pyttsx3
import datetime
from weather import *

# настройки
opts = {
    "alias": ('буханка', 'газ', 'матрос'),
    "tbr": ('скажи', 'расскажи', 'покажи', 'сколько', 'произнеси'),
    "cmds": {
        "ctime": ('текущее время', 'сейчас времени', 'который час'),
        "radio": ('включи музыку', 'воспроизведи радио', 'включи радио'),
        "stop": ('стой', 'тормоз', 'на месте', 'стоп'),
        'weather': ('Погода', "температура", "градусов", "одеться", "что одеть", 'обстановка', "за бортом"),
        'forward': ('шагом марш', 'иди', 'вперёд', 'двигайся')
    }
}


def callback(recognizer):
    try:
        with m as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        voice = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("[log] Распознано: " + voice)

        if voice.startswith(opts["alias"]):
            # обращаются к буханке
            # print('Обращаются ко мне')
            cmd = voice
            # print('Команда 1: ', cmd)

            for x in opts['alias']:
                cmd = cmd.replace(x, "").strip()

            for x in opts['tbr']:
                cmd = cmd.replace(x, "").strip()

            # print('Команда: ', cmd)

            # распознаем и выполняем команду
            cmd = recognize_cmd(cmd)
            execute_cmd(cmd['cmd'])

    except sr.UnknownValueError:
        print("[log] Голос не распознан!")
    except sr.RequestError as e:
        print("[log] Неизвестная ошибка, проверьте интернет!")


def recognize_cmd(cmd):
    print('Запущено распознавание команды')
    RC = {'cmd': '', 'percent': 0}
    for c, v in opts['cmds'].items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > RC['percent']:
                RC['cmd'] = c
                RC['percent'] = vrt
    print(RC)

    return RC


def execute_cmd(cmd):
    if cmd == 'ctime':
        # сказать текущее время
        now = datetime.datetime.now()
        speak("Сейчас " + str(now.hour) + ":" + str(now.minute))
    elif cmd == 'stop':
        # рассказать анекдот
        speak("Есть стоп")
    elif cmd == 'weather':
        try:
            speak(weather_coords())
        except:
            speak('Не могу получить данные о погоде. Всё равно синоптики врут')
    elif cmd == 'weather':
        speak(weather_coords())

    else:
        print('Команда не распознана, повторите!')


def speak(what):
    print(what)
    speak_engine.say(what)
    speak_engine.runAndWait()
    speak_engine.stop()


def takeCommand():
    # Принимает на входе аудио от микрофона, возвращает строку с нашими словами
    # r = sr.Recognizer()
    with m as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='ru-RU')  # Используем google для распознания голоса.
            print(f"User said: {query}\n")  # Запрос пользователя выведен.

        except Exception as e:
            print(e)  # используйте только если хотите видеть ошибку!
            print("Say that again please...")  # будет выведено, если речь не распознаётся
            return "None"  # вернётся строка "Пусто"
    return query


speak_engine = pyttsx3.init()
voices = speak_engine.getProperty('voices')
speak_engine.setProperty('voice', voices[0].id)

speak('Матрос буханка на связи')
r = sr.Recognizer()
m = sr.Microphone()

with m as source:
    r.adjust_for_ambient_noise(source)
# stop_listening = r.listen_in_background(m, callback(r))
if __name__ == "__main__":
    # wishMe()
    while True:
        try:
            callback(r)
        except:
            pass
        time.sleep(0.1)
