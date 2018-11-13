
import os
import re

import PIL.Image
import filetype

from datetime import datetime
from PIL import Image


# import time

def imgDate(fn):
    "returns the image date from image (if available)\nfrom Orthallelous"
    std_fmt = '%Y:%m:%d'
    # for subsecond prec, see doi.org/10.3189/2013JoG12J126 , sect. 2.2, 2.3
    tags = [(36867, 37521),  # (DateTimeOriginal, SubsecTimeOriginal)
            (36868, 37522),  # (DateTimeDigitized, SubsecTimeOriginal)
            (306, 37520), ]  # (DateTime, SubsecTime)
    exif = Image.open(fn)._getexif()

    for t in tags:
        dat_stmp = exif.get(t[0])

        # PIL.PILLOW_VERSION >= 3.0 returns a tuple
        dat_stmp = dat_stmp[0] if type(dat_stmp) == tuple else dat_stmp
        if dat_stmp != None: break

    if dat_stmp == None: return None

    T = datetime.strptime(dat_stmp[:10], std_fmt)

    # T = time.mktime(time.strptime(full, std_fmt)) + float('0.' + sub_stmp)
    return T


# Getting the current work directory (cwd)
# thisdir = os.getcwd()
thisdir = "/run/media/mateuszrusin/_arch/!foto"

# r=root, d=directories, f = files
for r, d, f in os.walk(thisdir):
    for file in f:
        fullfile = os.path.join(r, file)
        kind = filetype.guess(fullfile)

        if kind is None or kind.extension != 'jpg':
            print('Cannot guess file type!')
            continue

        print(fullfile + ' -> ' + imgDate(fullfile).strftime('%Y-%m-%d'))

        # img = PIL.Image.open(fullfile)
        # exif_data = img._getexif()
        #
        # print(fullfile)
        # print(exif_data[36867])

# print(glob.glob("/run/media/mateuszrusin/_arch/!foto/*.jpg"))