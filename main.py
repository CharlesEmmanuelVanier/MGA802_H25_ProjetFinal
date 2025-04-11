"""
Main module for rocket simulation application.
Coordinates GUI input collection, wind data formatting, and OpenRocket simulation execution.
"""

import gui
import orhelper_sim as orhs
from data_formater import WindDataFormatter

if __name__ == '__main__':
    # Get user input from GUI
    gui_data = gui.buildGui()
    
    # Format wind data
    formatter = WindDataFormatter(gui_data)
    wind_data = formatter.format_data()
    
    # Run the simulation
    Sim = orhs.OpenRocketSimulation(wind_data, gui_data.ork_file)
    Sim.simulation()
    Sim.print_stats()