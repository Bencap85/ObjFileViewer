from object_3d import *


class FileParser:

    def __init__(self, render):
        self.render = render
    def create_object_from_file(self, file):

        vertexes = []
        faces = []
        try:
            with open(file, 'r') as f:
                for line in f:
                    if line.startswith('v '):
                        vertexes.append([float(i) for i in line.split()[1:]] + [1])

                    elif line.startswith('f '):
                        faces_ = line.split()[1:]
                        faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])

        except FileNotFoundError:
            raise FileNotFoundError
        except IOError:
            raise IOError

        self.render.objects.append(Object3D(self.render, vertexes, faces))
