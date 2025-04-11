"""
OpenRocket simulation module using orhelper.
Manages rocket simulations through OpenRocket, including setup, execution,
and results processing.
"""

from orhelper import FlightDataType
import orhelper
from orhelper import FlightDataType, FlightEvent
from matplotlib import pyplot as plt
from matplotlib import patches
import math
import numpy as np
from scipy import stats

class OpenRocketSimulation:
    """
    Manages OpenRocket simulations using wind data and rocket design files.
    
    Handles:
    - Simulation setup and execution
    - Wind data application
    - Results collection and analysis
    - Statistical analysis and visualization
    
    Attributes:
        ork_file (str): Path to OpenRocket design file
        wind_data (list): Formatted wind data for simulations
        ranges (list): Landing ranges from launch site
        bearings (list): Landing bearings from launch site
        apogee (list): Apogee heights for each simulation
        stability (list): Stability data for each simulation
        flightdata (dict): Flight data from simulations
        landingpoints (list): Landing point data for each simulation
    """

    def __init__(self, wind_data, ork_file):
        """
        Initialize OpenRocket simulation manager.
        
        Args:
            wind_data (list): Formatted wind data for simulations
            ork_file (str): Path to OpenRocket design file
        """
        self.ork_file = ork_file
        self.wind_data = wind_data
        self.ranges = []
        self.bearings = []
        self.apogee = []
        self.stability = []
        self.flightdata = dict()
        self.landingpoints = []

    def simulation(self):
        """
        Run OpenRocket simulations with specified wind conditions.
        
        For each simulation:
        - Sets up wind model
        - Runs simulation
        - Collects flight data
        - Records apogee and landing points
        """
        i = 0
        try:
            with orhelper.OpenRocketInstance() as instance:
                orh = orhelper.Helper(instance)
                doc = orh.load_doc(self.ork_file)
                sim = doc.getSimulation(3)
                opts = sim.getOptions()

                for data in self.wind_data:
                    print('Running simulation ', i+1)
                    print(f"First wind point: {data[0]}")

                    opts.setWindModelType(instance.wind.WindModelType.MULTI_LEVEL)
                    model = opts.getWindModel()
                    model.clearLevels()
                    
                    for wind in data:
                        model.addWindLevel(wind[0],wind[1],wind[2],0.2)

                    airstarter = AirStart(0)
                    lp = LandingPoint(self.ranges, self.bearings)
                    orh.run_simulation(sim, listeners=(airstarter, lp))

                    self.flightdata = orh.get_timeseries(sim, [FlightDataType.TYPE_TIME, FlightDataType.TYPE_STABILITY, FlightDataType.TYPE_ALTITUDE])
                    self.apogee.append(max(self.flightdata[FlightDataType.TYPE_ALTITUDE]))
                    self.landingpoints.append(lp)
                    i += 1

        except Exception as e:
            print(f"Error during simulation: {e}")
            raise e

    def print_stats(self):
        """
        Print and visualize simulation statistics.
        
        Displays:
        - Average landing zone distance and bearing
        - Standard deviations
        - Mean flight apogee
        - Confidence ellipses for landing points
        """
        print(
            'Rocket landing zone %3.2f m +- %3.2f m bearing %3.2f deg +- %3.4f deg from launch site. Based on %i simulations.' % \
            (np.mean(self.ranges), np.std(self.ranges), np.degrees(np.mean(self.bearings)),
             np.degrees(np.std(self.bearings)), len(self.landingpoints)))
        print('Mean flight Apogee', np.mean(self.apogee), 'm')

        x = self.ranges * np.cos(self.bearings)
        y = self.ranges * np.sin(self.bearings)
        data = np.column_stack((x,y))
        mean = np.mean(data, axis=0)

        confidences = [0.80, 0.90, 0.99]
        chisq_vals = [np.sqrt(stats.chi2.ppf(i, df=2)) for i in confidences]

        fig, ax = plt.subplots()
        ax.scatter(x, y, label='Landing points')
        colors = ['blue', 'green', 'red']

        for i, k in enumerate(chisq_vals):
            radius = k * np.std(self.ranges)
            circle = patches.Circle(xy=mean, radius=radius,
                               edgecolor=colors[i],
                               facecolor='none', label=f'{int(confidences[i] * 100)}% landing zone')
            ax.add_patch(circle)

        ax.legend()
        ax.set_title('Confidence Ellipses')
        plt.grid(True)
        plt.show()

class LandingPoint(orhelper.AbstractSimulationListener):
    """
    Listener for tracking landing points during simulations.
    
    Attributes:
        ranges (list): Collection of landing distances
        bearings (list): Collection of landing bearings
    """
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
    """
    Listener for setting initial conditions for air-started simulations.
    
    Attributes:
        start_altitude (float): Starting altitude for the simulation
    """
    def __init__(self, altitude):
        self.start_altitude = altitude

    def startSimulation(self, status):
        position = status.getRocketPosition()
        position = position.add(0.0, 0.0, self.start_altitude)
        status.setRocketPosition(position)

METERS_PER_DEGREE_LATITUDE = 111325
METERS_PER_DEGREE_LONGITUDE_EQUATOR = 111050

def range_flat(start, end):
    """
    Calculate flat-earth distance between two points.
    
    Args:
        start: Starting position with getLatitudeDeg() and getLongitudeDeg() methods
        end: Ending position with getLatitudeDeg() and getLongitudeDeg() methods
        
    Returns:
        float: Distance in meters between the two points
    """
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.sqrt(dy * dy + dx * dx)

def bearing_flat(start, end):
    """
    Calculate flat-earth bearing between two points.
    
    Args:
        start: Starting position with getLatitudeDeg() and getLongitudeDeg() methods
        end: Ending position with getLatitudeDeg() and getLongitudeDeg() methods
        
    Returns:
        float: Bearing in radians from start to end point
    """
    dy = (end.getLatitudeDeg() - start.getLatitudeDeg()) * METERS_PER_DEGREE_LATITUDE
    dx = (end.getLongitudeDeg() - start.getLongitudeDeg()) * METERS_PER_DEGREE_LONGITUDE_EQUATOR
    return math.atan2(dy, dx)






