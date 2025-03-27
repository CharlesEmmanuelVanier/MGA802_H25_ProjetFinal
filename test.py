import os
import numpy as np
import orhelper
from random import gauss
import math
import gui


class LandingPoints(list):
    "A list of landing points with ability to run simulations and populate itself"

    def __init__(self):
        self.ranges = []
        self.bearings = []

    def add_simulations(self, num):
        with orhelper.OpenRocketInstance() as instance:

            # Load the document and get simulation
            orh = orhelper.Helper(instance)
            doc = orh.load_doc(os.path.join('Rockets/simple.ork'))
            sim = doc.getSimulation(3)

            # Access to various parameters
            opts = sim.getOptions()
            rocket = doc.getRocket()

            # Run num simulations and add to self
            for p in range(num):
                print('Running simulation ', p)

                opts.setWindModelType(instance.wind.WindModelType.MULTI_LEVEL)  # Set multi-level winds
                model = opts.getWindModel()
                model.clearLevels()

                #Loop here to add all the wind levels
                model.addWindLevel(500, 1,90,0)
                model.addWindLevel(750, 5,90,0)

                airstarter= AirStart(0)
                lp = LandingPoint(self.ranges, self.bearings)
                orh.run_simulation(sim, listeners=(airstarter, lp))
                self.append(lp)

    def print_stats(self):
        print(
            'Rocket landing zone %3.2f m +- %3.2f m bearing %3.2f deg +- %3.4f deg from launch site. Based on %i simulations.' % \
            (np.mean(self.ranges), np.std(self.ranges), np.degrees(np.mean(self.bearings)),
             np.degrees(np.std(self.bearings)), len(self)))


class LandingPoint(orhelper.AbstractSimulationListener):
    def __init__(self, ranges, bearings):
        self.ranges = ranges
        self.bearings = bearings

    def endSimulation(self, status, simulation_exception):
        worldpos = status.getRocketWorldPosition()
        conditions = status.getSimulationConditions()
        launchpos = conditions.getLaunchSite()

        self.ranges.append(range_flat(launchpos, worldpos))
        self.bearings.append(bearing_flat(launchpos, worldpos))


class AirStart(orhelper.AbstractSimulationListener):

    def __init__(self, altitude):
        self.start_altitude = altitude


METERS_PER_DEGREE_LATITUDE = 111325
METERS_PER_DEGREE_LONGITUDE_EQUATOR = 111050


def range_flat(start, end):
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.sqrt(dy * dy + dx * dx)


def bearing_flat(start, end):
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.pi / 2 - math.atan(dy / dx)


if __name__ == '__main__':
    points = LandingPoints()
    points.add_simulations(20)
    points.print_stats()