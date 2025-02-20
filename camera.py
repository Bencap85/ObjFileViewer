import pygame as pg
from matrix_functions import *


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0, 0, 1, 1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 4.0
        self.rotation_speed = 0.1

    def control(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_p]:
            if keys[pg.K_LEFT]:
                self.position -= self.right * self.moving_speed
            elif keys[pg.K_RIGHT]:
                self.position += self.right * self.moving_speed
            elif keys[pg.K_UP]:
                self.position += self.up * self.moving_speed
            elif keys[pg.K_DOWN]:
                self.position -= self.up * self.moving_speed


        elif keys[pg.K_r]:
            if keys[pg.K_LEFT]:
                self.camera_yaw(-self.rotation_speed)
            elif keys[pg.K_RIGHT]:
                self.camera_yaw(self.rotation_speed)
            elif keys[pg.K_UP]:
                self.camera_pitch(self.rotation_speed)
            elif keys[pg.K_DOWN]:
                self.camera_pitch(-self.rotation_speed)

        elif keys[pg.K_UP]:
            self.position += self.forward * self.moving_speed

        elif keys[pg.K_DOWN]:
            self.position -= self.forward * self.moving_speed

        elif keys[pg.K_i]:
            self.camera_roll(-self.rotation_speed)
        elif keys[pg.K_u]:
            self.camera_roll(self.rotation_speed)


    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate


    def camera_roll(self, angle):
        rotate = rotate_z(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
        pitch = rotate_x(angle)

        self.forward = self.forward @ pitch
        self.right = self.right @ pitch
        self.up = self.up @ pitch


    def translate_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()

