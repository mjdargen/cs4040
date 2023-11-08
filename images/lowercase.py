import os

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

files = os.listdir(DIR_PATH)

pngs = [f for f in files if f.endswith(".png")]

for png in pngs:
    new_name = ""
    for letter in png.split(".")[0]:
        if letter.islower() or letter == "_" or letter.isdigit():
            new_name += letter
        else:
            new_name += "_" + letter.lower()
    os.rename(f"{DIR_PATH}/{png}", f"{DIR_PATH}/{new_name + '.png'}")
