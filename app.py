from simulation import Simulation
import numpy as np
from plotting.animation import createAnimation

numParticles = 15
radii = np.random.uniform(size=(15,))*0.02+0.01
outputfile = 'results_50s.csv'

sim = Simulation(numParticles, radii, outputfile)

sim.run(0, 50, 0.01)
sim.writeOut()

createAnimation(outputfile, 'results50s.gif', 200)
