import numpy as np
import matplotlib.pyplot as plt
import imageio
import io


class Recorder: 
    def __init__(self, fps=10, path="animation.gif"):
        self.frames = []
        self.fps = fps
        self.path = path

    def save_frame(self):
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image = imageio.imread(buf)
        self.frames.append(image)
        buf.close()

    def save_movie(self):
        imageio.mimsave(self.path, self.frames, fps=self.fps, loop=0)


def draw_glider(t, x, param):
    xd = param["xd"]

    # x: [x, z, theta, phi, ... , vx, vz]
    sc = 2
    lw = -0.15 * sc
    lh = 0.45 * sc
    le = 0.04 * sc
    mac = 0.1145 * sc

    ct = np.cos(x[2])
    st = np.sin(x[2])
    ctp = np.cos(x[2] + x[3])
    stp = np.sin(x[2] + x[3])

    plt.figure(25)
    #plt.clf()
    plt.gca().set_aspect('equal')
    plt.title(f"time: {t:.2f} s")
    plt.xlabel("x (m)")
    plt.ylabel("z (m)")

    # --- Wind velocity field ---
    Xl = -4 + x[0]
    Xu = 1 + x[0]
    Yl = -1.0
    Yu = 1.0
    dx = 0.5
    dy = 0.5

    X = np.arange(Xl, Xu + dx, dx)
    Y = np.arange(Yl, Yu + dy, dy)
    XX, YY = np.meshgrid(X, Y)

    #Us = x[7] * np.ones_like(XX) #+ param["vx0"]
    #Vs = x[8] * np.ones_like(XX)

    #plt.quiver(XX, YY, Us, Vs, color='blue')

    # --- CG ---
    plt.plot(x[0], x[1], 'r.', markersize=10)

    # --- Fuselage ---
    if lw < 0:
        plt.plot([x[0], x[0] - lh * ct],
                 [x[1], x[1] - lh * st],
                 linewidth=1, color='black')
    else:
        plt.plot([x[0] + (lw + mac/2) * ct, x[0] - lh * ct],
                 [x[1] + (lw + mac/2) * st, x[1] - lh * st],
                 linewidth=1, color='black')

    # --- Wing ---
    plt.plot([x[0] + (lw + mac/2) * ct, x[0] + (lw - mac/2) * ct],
             [x[1] + (lw + mac/2) * st, x[1] + (lw - mac/2) * st],
             linewidth=3, color=[0, 0.2, 1])

    # --- Elevator ---
    plt.plot([x[0] - lh * ct, x[0] - lh * ct - 2 * le * ctp],
             [x[1] - lh * st, x[1] - lh * st - 2 * le * stp],
             linewidth=3, color=[0, 0.2, 1])

    # --- Axis limits ---
    plt.xlim([-4 + x[0], 1 + x[0]])
    plt.ylim([-1, 1.75])
    if("fixed_axis" in param):
        plt.xlim([-0.1, 4])
        plt.ylim([-1, 1.75])
    
    if("yline" in param):
        plt.axhline(param["yline"], color='gray', linestyle='--')

    # --- Perch ---
    plt.plot(xd[0], xd[1], 'ko', markersize=5)

    #plt.pause(0.001)  # for animation
