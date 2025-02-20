import pygame as pg
from matrix_functions import *
from numba import njit

@njit(fastmath=True)
def any_function(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    def __init__(self, render, vertexes, faces):
        self.render = render
        self.vertexes = vertexes
        self.faces = faces
        self.vertex_color = 'white'
        self.edge_color = 'orange'
        self.draw_vertices = False

    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 3) | (vertexes < -3)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for face in self.faces:
            polygon = vertexes[face]
            if not any_function(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, pg.Color(self.edge_color), polygon, 1)

        if self.draw_vertices is False:
            return

        for vertex in vertexes:
            if not any_function(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.circle(self.render.screen, pg.Color(self.vertex_color), vertex, 1)

    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)
