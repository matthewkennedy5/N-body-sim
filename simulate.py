from graphics import *
import time
import numpy as np
import pdb

X, Y, VX, VY, MASS = range(5)
WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000
PARTICLES = 30
TIME_DELAY = 0
REPULSION = 1
VELOCITY_STD = 1

class Simulator:

    def __init__(self, n_particles):
        self.init_physics(n_particles)
        self.init_graphics()

    def init_physics(self, n_particles):
        self.physics = np.zeros([n_particles, 5])
        self.physics[:, X] = np.random.uniform(WINDOW_WIDTH/4, 3*WINDOW_WIDTH/4, size=n_particles)
        self.physics[:, Y] = np.random.uniform(WINDOW_HEIGHT/4, 3*WINDOW_HEIGHT/4, size=n_particles)
        self.physics[:, VX] = np.random.normal(scale=VELOCITY_STD, size=n_particles)
        self.physics[:, VY] = np.random.normal(scale=VELOCITY_STD, size=n_particles)
        self.physics[:, MASS] = 2 ** np.random.normal(size=n_particles)

    def init_graphics(self):
        self.win = GraphWin('Simulation', WINDOW_WIDTH, WINDOW_HEIGHT)
        self.win.setBackground('black')
        self.particles = []
        for i in range(self.physics.shape[0]):
            point = Point(self.physics[i, X], self.physics[i, Y])
            particle = Circle(point, 5 * self.physics[i, MASS])
            particle.setFill('blue')
            particle.draw(self.win)
            self.particles += [particle]

    def start(self):
        while True:
            self.update()
            time.sleep(TIME_DELAY)

    def update(self):
        # Update position based on velocity
        for i in range(self.physics.shape[0]):
            self.physics[i, X] += self.physics[i, VX]
            self.physics[i, Y] += self.physics[i, VY]

        # # Fully vectorized attempt:
        # masses = self.physics[:, MASS]
        # # accels = np.sum(np.outer(masses))
        # x = self.physics[:, X]
        # y = self.physics[:, Y]

        # Update velocity based on acceleration
        for i in range(self.physics.shape[0]):
            # Update each particle's velocity based on the acceleration due to gravity
            # Naive implementation: TODO - vectorize`
            xi = self.physics[i, X]
            yi = self.physics[i, Y]
            mass1 = self.physics[i, MASS]
            dV = np.zeros(2)
            for j in range(self.physics.shape[0]):
                if i == j:
                    continue
                xj = self.physics[j, X]
                yj = self.physics[j, Y]
                r = np.array([xj - xi, yj - yi])
                mass2 = self.physics[j, MASS]
                distance = np.linalg.norm(r)
                accel = mass2 / (distance ** 2)

                # Repulsion
                # if distance < 10:
                #     accel -= REPULSION
                dV += accel * r

            self.physics[i, VX] += dV[0]
            self.physics[i, VY] += dV[1]

        # Move the particles on the screen
        for i, particle in enumerate(self.particles):
            pos = particle.getCenter()  # Position on the screen, which might be
                                        # rounded from the theoretical position
            dx = self.physics[i, X] - pos.getX()
            dy = self.physics[i, Y] - pos.getY()
            particle.move(dx, dy)


if __name__ == '__main__':

    s = Simulator(PARTICLES)
    s.start()
