import gui
import orhelper_sim as orhs

#Pas certain de cette ligne (?)
if __name__ == '__main__':

    wind_data = gui.buildGui()
    Sim = orhs.OpenRocketSimulation(wind_data.wind_data, wind_data.ork_file)
    Sim.simulation()
    Sim.print_stats()
   # points = orhelperdriver.LandingPoints()
   # points.print_stats()