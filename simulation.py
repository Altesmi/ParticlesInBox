from typing import Tuple
import numpy as np
import pandas as pd
from itertools import combinations
from particle import Particle


class Simulation:
    """Simulation class for particles in a box. Simulations are carried inside a unit rectangle.

        Args:
            numParticles (int): number of particles to be created
            radii (np.ndarray): Radius of each particle
            outputfile (str): name of the outputfile
        Attributes:
            particles (np.ndarray): collection of all the particles
            time (float): time in the simulation (s)
            outputfile (str): name of the outputfile
            results (pd.DataFrame): results dataframe where the particle positions and velocities are recorded
    """

    def __init__(self, numParticles: int, radii: np.ndarray, outputfile: str):
        self.particles: np.ndarray = np.array([], dtype=object)
        self.numParticles = numParticles
        self.time: float = 0.0
        self.outputfile: str = outputfile
        self.results: pd.DataFrame = pd.DataFrame(columns=['time', 'nParticle', 'radius', 'x', 'y', 'velx', 'vely'])

        for i in range(numParticles):

            while True:
                x, y = np.random.uniform(size=(2,))*(1-2*radii[i])+radii[i]  # random number between [rad, 1-rad]
                vr = 0.02*np.random.uniform()+0.001
                velphi = 2.0*np.pi*np.random.uniform()
                velx, vely = vr*np.cos(velphi), vr*np.sin(velphi)
                p = Particle(x, y, velx, vely, radii[i])
                collidesFlag = False
                for p2 in self.particles:
                    if p2.collidesParticle(p):
                        collidesFlag = True
                        break
                if collidesFlag:
                    continue
                else:
                    self.particles = np.append(self.particles, p)
                    break

    def handleParticleCollision(self, p1: Particle, p2: Particle) -> Tuple:
        """Changes velocity of particles that have collided.

        Args:
            p1 (Particle): First particle
            p2 (Particle): Second particle

        Returns:
            Tuple: First element is p1 and second p2, whose velocity has been updated following collision

        References:
            https://en.wikipedia.org/wiki/Elastic_collision
        """
        v1 = p1.vel
        v2 = p2.vel
        m1 = p1.r**2
        m2 = p2.r**2
        dSquared = np.linalg.norm(p1.coordinates-p2.coordinates)**2
        u1 = p1.vel - 2*m2 * np.dot(p1.vel - p2.vel, p1.coordinates-p2.coordinates) \
            * (p1.coordinates-p2.coordinates)/(m1+m2)/dSquared
        u2 = p2.vel - 2*m1 * np.dot(p2.vel - p1.vel, p2.coordinates - p1.coordinates)\
            * (p2.coordinates-p1.coordinates) / (m1+m2) / dSquared
        p1.vel = u1
        p2.vel = u2
        print(v1)
        print(v2)
        print(u1)
        print(u2)
        print(np.abs(np.sum(np.sum(v1**2)+np.sum(v2**2))-np.sum(np.sum(u1**2)+np.sum(u2**2))))

        return (p1, p2)

    def checkAndHandleParticleCollisions(self):
        pairs = combinations(range(self.numParticles), 2)
        for i, j in pairs:
            if self.particles[i].collidesParticle(self.particles[j]):
                self.particles[i], self.particles[j] = self.handleParticleCollision(self.particles[i],
                                                                                    self.particles[j])

    def run(self, timeStart: float, timeEnd: float, dt: float) -> None:
        """Advcances particles in box simulation from timeStart to timeEnd with time step dt

        Args:
            timeStart (float): Starting time of the simulation
            timeEnd (float): Ending time of the simulation
            dt (float): Simulation time step
        """
        time = timeStart

        while time <= timeEnd:
            for i, p in enumerate(self.particles):
                p.run(dt)
            self.checkAndHandleParticleCollisions()
            time = time + dt
            self.updateResults(time)

    def updateResults(self, time: float) -> None:
        """Appends current position and velocity of particles to results dataframe

        Args:
            time (float): Current time in the simulation. Will be included in results dataframe
        """
        ind = self.results.shape[0]

        for i, p in enumerate(self.particles):
            self.results.loc[ind] = [time, i, p.r, p.x, p.y, p.velx, p.vely]
            ind = ind+1

    def writeOut(self) -> None:
        """Saves the results to csv file. The filename is speciefied in outputfile when creating the simulation object.

        """
        self.results.to_csv(self.outputfile)
