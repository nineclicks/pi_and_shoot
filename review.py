from display import show
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def get_images():
    return sorted(list(Path('out').glob('*.jpg')))

w = 480
h = 320

delete_button_coords = [
        int(w / 3),
        int(h / 6 * 5),
        int(w / 3 * 2),
        int(h-2),
        ]

class Review:

    i = 0
    image_len = 0
    confirm = False
    image_list = []

    def __init__(self):
        self.image_list = get_images()
        self.image_len = len(self.image_list)
        self.i = self.image_len - 1
        self.refresh()

    def press(self, x, y):
        if self.image_len == 0:
            return

        elif x >= delete_button_coords[0] and x <= delete_button_coords[2] and y >= delete_button_coords[1] and y <= delete_button_coords[3]:
            if not self.confirm:
                self.confirm = True
                self.refresh()

            else:
                self.delete()
                self.confirm = False
                self.refresh()

        elif x < w / 2:
            self.nav(-1)
            self.confirm = False

        else:
            self.nav(1)
            self.confirm = False

    def nav(self, n):
        self.i = (self.i + n) % self.image_len
        self.refresh()

    def delete(self):
        self.image_list[self.i].unlink()
        self.image_list = get_images()
        self.image_len = len(self.image_list)
        if self.i > len(self.image_list) - 1:
            self.i -= 1

    def refresh(self):
        fnt = ImageFont.truetype("Roboto-Thin.ttf", 26)

        if self.image_len == 0:
            image = Image.new('RGB', (w, h))
            draw = ImageDraw.Draw(image)
            draw.rectangle((0,0,w-1, h-1), outline=(255,255,255), fill=(0,0,0))
            txt = 'No Images!'
            txtw, txth = draw.textsize(txt,font=fnt)
            draw.text((
                w / 2 - txtw / 2,
                h / 2 - txth / 2
                ), txt,font=fnt, fill=(255,255,255))

        else:
            image = Image.open(str(self.image_list[self.i]))
            image = image.resize((480,320), Image.NEAREST)
            draw = ImageDraw.Draw(image)
            draw.rectangle((0,0,image.size[0]-1, image.size[1]-1), outline=(255,255,255))
            txt = '{}/{}'.format(self.i+1, self.image_len)
            txtw, txth = draw.textsize(txt,font=fnt)
            draw.rectangle((1,1,txtw+1,txth+1), fill=(0,0,0))
            draw.text((1,1), txt,font=fnt, fill=(255,255,255))

            txt = 'Confirm' if self.confirm else 'Delete'
            txtw, txth = draw.textsize(txt,font=fnt)
            draw.rectangle(delete_button_coords, fill=(0,0,0), outline=(255,255,255))
            draw.text((
                (delete_button_coords[2] + delete_button_coords[0]) / 2 - txtw / 2,
                (delete_button_coords[3] + delete_button_coords[1]) / 2 - txth / 2
                ), txt,font=fnt, fill=(255,255,255))

        show(image)

