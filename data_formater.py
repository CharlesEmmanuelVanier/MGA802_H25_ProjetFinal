"""
Data formatting module for rocket simulation wind data.
Processes and formats wind data from JSON files for use in OpenRocket simulations.
Handles both random and sequential sampling of wind data based on user parameters.
"""

import json
from datetime import datetime, timedelta
from random import randrange

class WindDataFormatter:
    """
    Formats wind data for OpenRocket simulations based on GUI inputs.
    
    Handles processing of wind data from JSON files, including:
    - Random sampling
    - Sequential sampling
    - Data formatting for OpenRocket compatibility
    
    Attributes:
        wind_data_range (list): List of dates for wind data collection
        num_simulations (int): Number of simulations to run
        wind_data (list): Processed wind data for simulations
    """

    def __init__(self, gui_data):
        """
        Initialize the wind data formatter with GUI data.
        
        Args:
            gui_data: GUI class instance containing wind_data_range and num_simulations
        """
        self.wind_data_range = gui_data.wind_data_range
        self.num_simulations = gui_data.num_simulations
        self.wind_data = []
        
    def format_data(self):
        """
        Format wind data based on the date range and number of simulations.
        
        Processes wind data according to sampling rate:
        - If sample_rate > 1: Use random sampling
        - If sample_rate <= 1: Use sequential sampling with possible random fill
        
        Returns:
            list: Formatted wind data ready for OpenRocket simulations
        """
        sample_rate = len(self.wind_data_range) / self.num_simulations
        
        if sample_rate > 1:
            self.wind_data.extend(self.get_random_wind_data(self.num_simulations))
        else:
            sample_rate = 1/sample_rate
            sure_sim, random_sim = divmod(sample_rate, 1)
            
            with open("data/CYYU.upper_winds.json", 'r', encoding="utf-8") as f:
                wind_database = json.load(f)
            
            periode_cible = "AM"
            for day in self.wind_data_range:
                resultats = []
                for entry in wind_database:
                    datetime_str = entry.get("datetime", "")[:10]
                    if datetime_str == day and periode_cible in entry and "data" in entry[periode_cible]:
                        resultats.extend(entry["AM"]["data"])
                self.wind_data.extend(self.wind_data_to_or_input(resultats, int(sure_sim)))
                
            if self.num_simulations - len(self.wind_data) != 0:
                self.wind_data.extend(self.get_random_wind_data(self.num_simulations - len(self.wind_data)))
        
        return self.wind_data

    def get_random_wind_data(self, num_sim_restant):
        """
        Get random wind data for the remaining simulations needed.
        
        Args:
            num_sim_restant (int): Number of remaining simulations needing wind data
            
        Returns:
            list: Randomly selected and formatted wind data
        """
        periode_cible = "AM"
        data_to_return = []
        
        with open("data/CYYU.upper_winds.json", 'r', encoding="utf-8") as f:
            wind_database = json.load(f)
        
        for _ in range(num_sim_restant):
            resultats = []
            random_number = randrange(0, len(self.wind_data_range))
            day = self.wind_data_range[random_number]
            for entry in wind_database:
                datetime_str = entry.get("datetime", "")[:10]
                if datetime_str == day and periode_cible in entry and "data" in entry[periode_cible]:
                    resultats.extend(entry["AM"]["data"])
                    data_to_return.extend(self.wind_data_to_or_input(resultats, 1))
        
        return data_to_return

    @staticmethod
    def wind_data_to_or_input(wind_data, duplicates):
        """
        Convert wind data to OpenRocket input format.
        
        Args:
            wind_data (list): Raw wind data points
            duplicates (int): Number of times to duplicate the data
            
        Returns:
            list: Formatted wind data in OpenRocket-compatible format
                 [altitude, wind_speed, direction, deviation]
        """
        wind_data_good_format_to_append = []
        result = []
        
        for data in wind_data:
            wind_data_good_format_to_append.append([
                data["altitude"],
                data["wind"],
                data["heading"],
                0
            ])
        
        for _ in range(duplicates):
            result.append(wind_data_good_format_to_append)
        
        return result 