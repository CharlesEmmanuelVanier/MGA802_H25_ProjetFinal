import gui
import orhelperdriver
import monte_carlo
import json
from datetime import datetime

#Pas certain de cette ligne (?)
if __name__ == '__main__':

    wind_data = gui.buildGui()
    print(wind_data.wind_data)

   # points = orhelperdriver.LandingPoints()
   # points.print_stats()