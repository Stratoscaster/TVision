import cv2 as cv


class CameraCapture:

    def __init__(self, width=1920, height=1080):
        self.width = width
        self.height = height
        self.cam = cv.VideoCapture(0)
        if not self.cam.isOpened():
            print('Camera cannot be opened!')
            exit()

        self.cam.set(cv.CAP_PROP_FRAME_WIDTH, self.width)
        self.cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.height)

    def next_frame(self):
        ret, frame = self.cam.read()
        if not ret:
            print('Cannot receive frame! End of stream.')
            return None
        return frame

    def release(self):
        self.cam.release()
