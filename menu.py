from PIL import Image, ImageDraw, ImageFont
import subprocess
from display import show

class Menu:

    w = 480
    h = 320
    
    btn_w = int(w / 3)
    btn_h = int(h / 2)

    img = None

    items = []

    def __init__(self):
        self.render_menu()

    def render_menu(self):
        self.img = Image.new("RGB", (self.w, self.h)) 
        draw = ImageDraw.Draw(self.img)   
        draw.rectangle((0,0,self.w-1,self.h-1), fill=(0,0,0)) 

        for n in range(len(self.items)):
            self.render_btn(n)

        show(self.img)

    def render_btn(self, n):
        fnt = ImageFont.truetype("Roboto-Thin.ttf", 26)
        btn = Image.new("RGB", (self.btn_w, self.btn_h)) 
        draw = ImageDraw.Draw(btn)
        draw.rectangle((0,0,self.btn_w-1,self.btn_h-1), fill=(0,0,0), outline=(255,255,255))
        txtw, txth = draw.textsize(self.items[n][0](),font=fnt)
        draw.text((int(self.btn_w/2-txtw/2),int(self.btn_h/2-txth/2)), self.items[n][0](),font=fnt, fill=(255,255,255))
        self.img.paste(btn, (self.btn_w * (n % 3), self.btn_h * int(n / 3)))

    def press(self, x, y):
        y = y
        bx = int(x / self.btn_w)
        by = int(y / self.btn_h)

        b_num = bx + by * 3
        try:
            self.items[b_num][1]()
        except Exception as e:
            print(str(e))

