from simulation import Simulation
import numpy as np
from plotting.animation import createAnimation

numParticles = 40
radii = np.random.uniform(size=(40,))*0.02+0.01
outputfile = 'results_200s.csv'

sim = Simulation(numParticles, radii, outputfile)

sim.run(0, 200, 0.1)
sim.writeOut()

createAnimation(outputfile, 'results200s.gif', 200)
