import re


# from PIL import Image
# from PIL.ExifTags import TAGS


def ReplacePolishCharacters(text):
    polishChars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ż', 'ź']
    replaceChar = ['a', 'c', 'e', 'l', 'n', 'o', 's', 'z', 'z']
    i = 0
    while i < 9:
        text = text.replace(polishChars[i], replaceChar[i])
        i = i + 1
    return text


def RemoveSpecialCharacters(text):
    text = re.sub('[^A-Za-z0-9ąćęłńóśżź]+', ' ', text)
    return text


def TextInputCleanup(text):
    text = re.sub('[^A-Za-z0-9ąćęłńóśżź.,?!-%@*/+]+', ' ', text)
    return text


# function takes an opened pillow image and returns dictionary of main EXIF Tags
# EXIF, see exif specification at http://www.exiv2.org/tags.html
# and https://en.wikipedia.org/wiki/Exposure_value#EV_and_APEX

def GetExifData(im):
    exif_tags = im._getexif()
    if exif_tags != None:
        picture_exif = {}
        date_taken = exif_tags[36867]
        k = date_taken.rfind(" ")
        date = date_taken[:k]
        time = date_taken[k:]
        date = date.replace(":", "-")
        date_taken = date + time
        picture_exif["date_taken"] = date_taken

        camera_make = exif_tags[271].lower()
        picture_exif["camera_make"] = camera_make
        camera_model = exif_tags[272].lower()
        picture_exif["camera_model"] = camera_model
        try:
            picture_exif["lens"] = exif_tags[42036]
        except Exception:
            picture_exif["lens"] = "n/a"
        try:
            picture_exif["focal_lenght"] = round(exif_tags[37386][0] / exif_tags[37386][1])
        except Exception:
            picture_exif["focal_lenght"] = None
        try:
            picture_exif["iso"] = exif_tags[34855]
        except Exception:
            picture_exif["iso"] = None
        picture_exif["exposure_time"] = round((exif_tags[33434][1] / exif_tags[33434][0]), 4)

        if picture_exif["exposure_time"] > 1:
            picture_exif["exposure_time"] = "1/" + str(round(picture_exif["exposure_time"]))
        else:
            picture_exif["exposure_time"] = round(1 / picture_exif["exposure_time"], 1)

        picture_exif["f_stop"] = exif_tags[33437][0] / exif_tags[33437][1]
    else:
        picture_exif = {
            "camera_make": "n/a",
            "camera_model": "n/a",
            "lens": "n/a",
            "focal_lenght": None,
            "date_taken": None,
            "iso": None,
            "f_stop": None,
            "exposure_time": None,
        }
    return picture_exif
