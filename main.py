import gui
import orhelper_sim as orhs

#Pas certain de cette ligne (?)
if __name__ == '__main__':

    wind_data = gui.buildGui()
    Sim = orhs.OpenRocketSimulation(wind_data.wind_data, wind_data.orkfile)

   # points = orhelperdriver.LandingPoints()
   # points.print_stats()