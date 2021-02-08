from io import BytesIO
import picamera
import threading
from PIL import Image, ImageDraw
from time import sleep
from display import show


class Preview:

    running = False
    camera_preview_thread = None
    camera = None
    lock = None
    snap_path = None
    resolution = (480,320)
    screen = (480, 320)
    review_time = 3

    def __init__(self, resolution, review_time=3, camera=None):
        if camera is None:
            camera = picamera.PiCamera()
            camera.start_preview()
        self.resolution = resolution
        self.review_time = review_time
        self.lock = threading.Lock()
        self.camera = camera

    def camera_preview(self):
        show_cmd = (
                'ffmpeg -hide_banner -loglevel error -vcodec png '
                '-i /dev/shm/tmp.png -vcodec rawvideo -f rawvideo '
                '-pix_fmt rgb565 /dev/fb1 -y'
                )

        stream = BytesIO()

        while self.running:
            try:
                self.lock.acquire()
                path = self.snap_path
                self.snap_path = None
            finally:
                self.lock.release()

            if path is None:
                self.camera.resolution = (480, 320)
                self.camera.capture(stream, format='png')
                stream.truncate()
                show(stream)
            else:
                self.camera.resolution = self.resolution
                self.camera.capture(stream, format='jpeg')
                stream.seek(0)
                with open(path, 'wb') as f:
                    f.write(stream.getbuffer())
                stream.seek(0)
                image = Image.open(stream)
                image = image.resize((480,320), Image.NEAREST)
                draw = ImageDraw.Draw(image)
                draw.rectangle((0,0,image.size[0]-1, image.size[1]-1), outline=(255,255,255))
                show(image)
                sleep(self.review_time)

    
    def start(self):
        self.running = True
        self.camera_preview_thread = threading.Thread(target=self.camera_preview)
        self.camera_preview_thread.daemon = True
        self.camera_preview_thread.start()

    def stop(self):
        self.running = False
        self.camera_preview_thread.join()

    def snap(self, path):
        try:
            self.lock.acquire()
            self.snap_path = path
        finally:
            self.lock.release()
