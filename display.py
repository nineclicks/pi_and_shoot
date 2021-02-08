import subprocess

from PIL import Image
from io import BytesIO

show_cmd = (
        'ffmpeg -hide_banner -loglevel error -vcodec png '
        '-i /dev/shm/tmp.png -vcodec rawvideo -f rawvideo '
        '-pix_fmt rgb565 /dev/fb1 -y'
        )

image_temp = '/dev/shm/tmp.png'


def show(x):
    if isinstance(x, Image.Image):
        x.save(image_temp, format='png')

    elif isinstance(x, BytesIO):
        x.seek(0)
        with open(image_temp, 'wb') as f:
            f.write(x.getbuffer())

    subprocess.run(show_cmd.split(' '))
