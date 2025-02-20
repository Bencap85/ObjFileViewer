import pygame as pg
from object_3d import *
from camera import *
from projection import *
from file_parser import *
import sys
class SoftwareRender:

    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 1200, 600
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.objects = []
        self.create_camera()
        self.create_projection()


    def create_camera(self):
        self.camera = Camera(self, [0.1, 8, -60])

    def create_projection(self):
        self.projection = Projection(self)


    def draw(self):
        self.screen.fill(pg.Color('darkslategrey'))
        for object in self.objects:
            object.draw()

    def draw_instructions(self):
        font = pg.font.SysFont('Arial', 30)

        instructions = [
            "Controls:",
            "p + Arrow Keys: Pan Camera",
            "r + Arrow Keys: Rotate Camera",
            "u/i: Roll Camera Left/Right",
            "Arrow Up/Down: Move Forward/Backward"
        ]

        y_offset = 10
        for line in instructions:
            text_surface = font.render(line, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += 30

    def run(self):

        while True:
            self.draw()
            self.camera.control()
            self.draw_instructions()
            [ exit() for i in pg.event.get() if i.type == pg.QUIT ]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: main.py <filename>")
        exit(1)

    file_name = sys.argv[1]
    if file_name[len(file_name) - 4:] != ".obj":
        print("Only able to read .obj files")
        exit(1)

    app = SoftwareRender()

    fp = FileParser(app)
    try:
        fp.create_object_from_file(file_name)

    except FileNotFoundError:
        print("File not found")
        exit(1)

    except IOError as e:
        print(f"Error reading file: {e}")
        exit(1)

    app.run()
