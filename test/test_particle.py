import pytest
from ..particle import Particle


@pytest.fixture(scope="function")
def test_particle():
    return Particle(x=1.0, y=3.0, velx=0.0, vely=0.0, radius=0.1)


@pytest.fixture(scope="function")
def another_particle():
    return Particle(x=5.0, y=2.0, velx=0.0, vely=0.0, radius=0.1)


def test_collidesparticle(test_particle, another_particle):

    assert not test_particle.collidesParticle(another_particle)


def test_handlewallcollision(test_particle):
    test_particle.checkAndHandleWallCollision()
    assert test_particle.x == 0.9
    assert test_particle.y == 0.9
