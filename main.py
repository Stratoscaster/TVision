SCALE = 0.025
width = int(1920 * SCALE)
height = int(1080 * SCALE)
print(f'Capturing Camera @ {width}x{height}')
import cv2 as cv
import sys
from camera_capture import CameraCapture
from frame_controller import FrameController
import numpy as np
from numpy import random as rand

cap = CameraCapture(width, height)


# print(frame)
# cv.imshow('frame', frame)
#
# while cv.waitKey(1) != ord('q'):
#     pass

# for item in frame:
#     print(item)

frame_con = FrameController()
result = None

# cv.imwrite('test_result.jpg', frame)
frame = cap.next_frame()
# frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
keypressed = cv.waitKey(1)
while keypressed != ord('q'):

    if isinstance(frame, np.ndarray):
        # grab first row of pixels
        frame = cap.next_frame()
        # frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        result = frame_con.process_frame_and_update_rgb(frame)
        cv.imshow('resultant frame', frame)

        if keypressed == ord('s'):
            print('Saving frame as JPG.')
            cv.imwrite(f'test_result{rand.randint(1,1000000)}.jpg', frame)

        if keypressed == ord('r'):
            print('Toggling rectangle.')
            frame_con.toggle_rect()

    keypressed = cv.waitKey(1)


cv.destroyAllWindows()

########### NOTES ##########

# TV Dims: 37.5" width x 21.5" height
# Required strand length: 118" total or 9.83'
