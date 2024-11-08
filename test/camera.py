# camera.py
import numpy as np

class Camera:
    def __init__(self, position, target, up):
        self.position = position
        self.target = target
        self.up = up

    def get_view_matrix(self):
        f = (self.target - self.position)
        f = f / np.linalg.norm(f)
        r = np.cross(f, self.up)
        r = r / np.linalg.norm(r)
        u = np.cross(r, f)

        view = np.identity(4, dtype=np.float32)
        view[:3, :3] = np.array([r, u, -f])
        view[:3, 3] = -np.dot(view[:3, :3], self.position)
        return view

    def get_projection_matrix(self, fov, aspect, near, far):
        tan_half_fov = np.tan(np.radians(fov) / 2)
        proj = np.zeros((4, 4), dtype=np.float32)
        proj[0, 0] = 1 / (aspect * tan_half_fov)
        proj[1, 1] = 1 / tan_half_fov
        proj[2, 2] = -(far + near) / (far - near)
        proj[2, 3] = -(2 * far * near) / (far - near)
        proj[3, 2] = -1
        return proj
