import cv2 as cv
import numpy as np

# DISABLE FOR PC testing
import board
import neopixel as neo


class RGBController:

    def __init__(self, num_leds=150):
        self.NUM_LEDS = num_leds
        self.pixels = neo.NeoPixel(board.D18, self.NUM_LEDS, auto_write=False)
        # self.pixels = []
        self.STRAND_OFFSET = 0
        if type(self.pixels) == 'list':
            print('YOU FORGOT TO RE-ENABLE NEOPIXEL & BOARD LIBRARIES')

        # EDGE_ORDER MUST CONTAIN ALL VALUES: 'top', 'right', 'bottom', and 'left'.
        # Changing this order defines where the 'start' of your strip is.
        '''
            Example:
            If you say bottom, left, top, right...
            Then the strand MUST start at the bottom-right corner and go clockwise
            
            If you say bottom, right, top, left...
            Then the strand MUST start at the bottom-left corner and go counter-clockwise
            
            If you say top, right, bottom, left...
            Then the strand MUST start at the top-left and go clockwise 
        '''
        self.EDGE_ORDER = ['top', 'right', 'bottom', 'left']

    def update_strand(self, edges: dict):
        index = self.STRAND_OFFSET
        # Access edge names in correct order
        print(edges)
        for name in self.EDGE_ORDER:
            for pixel in edges[name]:
                if index > self.NUM_LEDS:
                    print('end of strand')
                    self.pixels.show()
                    return
                self.pixels[index] = pixel
                index += 1
        self.pixels.show()
