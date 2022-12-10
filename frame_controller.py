import cv2 as cv
import numpy as np

from rgb_controller import RGBController
from time import sleep


class FrameController:

    def __init__(self):
        self.strand = []
        self.representation = []
        self.draw_rect = False
        self.NUM_LEDS = 150
        self.rgb = RGBController(self.NUM_LEDS)

    # Take our 96x54x96x54 edge and convert to the LED edge lengths 48x27x48x27 (half length)
    # Note, to generalize this, the algorithm will need to be rewritten
    def condense_frame_edge(self, edges: dict):
        condensed = {}
        for edge_name in edges.keys():
            edge = edges[edge_name]
            condensed_edge = []
            for i in range(0, len(edge) - 1, 2):
                pix1 = edge[i]
                pix2 = edge[i + 1]
                condensed_edge.append(self.lab_color_space_average(pix1, pix2))
            condensed[edge_name] = condensed_edge
        return condensed

    # According to color theory you cannot just regular average RGB values, you must do it according to the following formula (quadratic mean)
    # NewColor = sqrt((R1^2+R2^2)/2),sqrt((G1^2+G2^2)/2),sqrt((B1^2+B2^2)/2)
    def lab_color_space_average(self, pixel1, pixel2):
        r1, g1, b1 = pixel1
        r2, g2, b2 = pixel2
        return int(np.sqrt((r1 ** 2 + r2 ** 2) / 2)), int(np.sqrt((g1 ** 2 + g2 ** 2) / 2)), int(
            np.sqrt((b1 ** 2 + b2 ** 2) / 2))

    def process_frame_and_update_rgb(self, frame):
        # print(frame)
        # Step 1: Grab each frame edge
        edges = self.process_frame(frame)
        # Step 2: Condense each array of pixels into led values matching the led edge length
        condensed_edges = self.condense_frame_edge(edges)
        self.rgb.update_strand(condensed_edges)

        # Old debug code don't use it
        # index = 0
        # arr = None
        # for edge in condensed_edges.values():
        #     if arr is None:
        #         arr = np.ndarray((len(edge), 4, 3))
        #     arr.put(index, edge)
        #     index += 1

        # print(arr)
        #
        # cv.imshow('condensed edges', arr)
        # Step 2: Copy RGB values from strand into our rgb pixels

    def get_img_representation(self):
        pass

    def toggle_rect(self):
        self.draw_rect = not self.draw_rect

    def process_frame(self, frame: list):
        height, width = frame.shape[:2]
        rectPos = {
            'x1': 1,
            'y1': 1,
            'x2': width - 2,
            'y2': height - 2
        }
        # print(rectPos)
        if self.draw_rect:
            cv.rectangle(frame, (rectPos['x1'], rectPos['y1']), (rectPos['x2'], rectPos['y2']), (0, 0, 0), -1)

        TOP = 0
        LEFT = 0
        BOTTOM = height - 1
        RIGHT = width - 1

        # Here the edge is broken up into 4 sections
        '''
                top 3
                TTT
        mid1    M@R     right 2
                BBR
                bottom 2
            
        strand is then composed of [TOP, RIGHT, BOTTOM, MID_LEFT] to create an edge chain
            '''

        # get top edge
        top_edge = []
        for x in range(0, width):
            top_edge.append(self.get_frame_pixel(frame, x, TOP))

        # get right edge
        right_edge = []
        for y in range(1, height):
            right_edge.append(self.get_frame_pixel(frame, RIGHT, y))

        # get bottom edge
        bottom_edge = []
        for x in range(0, width - 1):
            bottom_edge.append(self.get_frame_pixel(frame, x, BOTTOM))

        # get left edge
        left_edge = []
        for y in range(1, height - 1):
            left_edge.append(self.get_frame_pixel(frame, LEFT, y))

        actual_length = len(top_edge) + len(right_edge) + len(bottom_edge) + len(left_edge)
        expected_length = (width) + (height - 1) + (width - 1) + (height - 2)
        # print('expected strand length:', expected_length)
        # print('actual strand length:', actual_length)

        edges = {
            'top': top_edge,
            'right': right_edge,
            'bottom': bottom_edge,
            'left': left_edge
        }
        return edges

    def get_frame_pixel(self, frame: list, x: int, y: int):
        return frame[y, x]

    def set_frame_pixel(self, frame: list, pixel: list, x: int, y: int):
        frame[y, x] = pixel
