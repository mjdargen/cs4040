import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

files = os.listdir(DIR_PATH)

wavs = [f for f in files if f.endswith(".wav")]


for wav in wavs:
    os.rename(f"{DIR_PATH}/{wav}", f"{DIR_PATH}/{wav.replace('_', '')}")

files = os.listdir(DIR_PATH)
wavs = [f for f in files if f.endswith(".wav")]

for wav in wavs:
    new_name = ""
    for letter in wav.split(".")[0]:
        if letter.islower() or letter == "_" or letter.isdigit() or not new_name:
            new_name += letter.lower()
        else:
            new_name += "_" + letter.lower()
    os.rename(f"{DIR_PATH}/{wav}", f"{DIR_PATH}/{new_name + '.wav'}")
