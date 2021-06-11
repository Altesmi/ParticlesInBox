import pytest
import numpy as np
from ..simulation import Simulation


@pytest.fixture(scope="function")
def test_simulation():
    numParticles = 2
    radii = np.repeat([0.05], repeats=numParticles)
    outputfile = 'test.csv'
    sim = Simulation(numParticles=numParticles, radii=radii, outputfile=outputfile)
    # Change the two particles so that they collide
    sim.particles[0].x = 0.1
    sim.particles[0].y = 0.1
    sim.particles[0].velx = 0.1
    sim.particles[0].vely = 0.0

    sim.particles[1].x = 0.19
    sim.particles[1].y = 0.1
    sim.particles[1].velx = -0.1
    sim.particles[1].vely = 0.0

    return sim


@pytest.fixture(scope="function")
def test_large_simulation():
    numParticles = 20
    radii = np.repeat([0.05], repeats=numParticles)
    outputfile = 'test.csv'
    return Simulation(numParticles=numParticles, radii=radii, outputfile=outputfile)


def test_checkAndhandleParticleCollision(test_simulation):
    test_simulation.checkAndHandleParticleCollisions()
    assert pytest.approx(test_simulation.particles[0].velx, rel=1e-10) == -0.1
    assert pytest.approx(test_simulation.particles[1].velx, rel=1e-10) == 0.1


def test_momentum_conservation(test_large_simulation):
    momentum_start = np.sum(np.array([np.sqrt(np.sum(p.vel**2)) for p in test_large_simulation.particles]))
    test_large_simulation.run(0, 1, 0.1)
    momentum_end = np.sum(np.array([np.sqrt(np.sum(p.vel**2)) for p in test_large_simulation.particles]))

    assert pytest.approx(momentum_start, rel=1e-10) == pytest.approx(momentum_end, rel=1e-10)
