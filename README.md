# MGA802_H25_ProjetFinal

A Python application for rocket flight simulation using OpenRocket, with wind data integration and Monte Carlo analysis.

## Description

This project provides a graphical interface to run multiple OpenRocket simulations with real wind data. It allows users to:
- Select an OpenRocket (.ork) design file
- Choose the number of simulations to run
- Select a date range for wind data sampling
- Visualize landing distributions and flight statistics

## Project Structure

The project consists of three main components:

1. **GUI Interface** (`gui.py`)
   - Provides user input interface
   - Handles file selection and simulation parameters
   - Date range selection for wind data

2. **Data Formatter** (`data_formater.py`)
   - Processes wind data from JSON files
   - Handles random and sequential sampling
   - Formats data for OpenRocket compatibility

3. **Simulation Manager** (`orhelper_sim.py`)
   - Manages OpenRocket simulations
   - Processes simulation results
   - Generates statistical analysis and visualizations

## Requirements

- Python 3.x
- Java Runtime Environment (JRE)
- OpenRocket JAR file (included)
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Ensure Java is properly installed and JAVA_HOME is set.

## Usage

1. Run the main script:
```bash
python main.py
```

2. In the GUI:
   - Select your .ork rocket design file
   - Enter the desired number of simulations
   - Select start and end dates for wind data
   - Click "Confirm" to run simulations

3. View Results:
   - Landing distribution plot
   - Statistical analysis of landing points
   - Flight apogee data

## Data Files

- Rocket designs should be placed in the `Rockets/` directory
- Wind data is stored in `data/CYYU.upper_winds.json`

## Output

The program provides:
- Landing zone statistics (distance and bearing from launch site)
- Mean flight apogee
- Confidence ellipses for landing distribution
- Optional KDE heatmap visualization

## License

Free

## Contributors

Charles

## Test Case

To verify the system is working correctly, you can run this specific test case:

1. Launch the application:
```bash
python main.py
```

2. In the GUI interface:
   - Click "Browse" and select `Rockets/Arrow 1.ork`
   - Set "Number of simulations" to 10 # Doesn't really matter
   - Set both Start Date and End Date to March 8, 2025 # To test a range of data you can use March 6, 2025 to March 8, 2025.
   - Click "Confirm"

Expected Results:
- The simulation will run with the Arrow 1 rocket design
- Using wind data for a single day (March 8, 2025)
- Will display landing points distribution
- Will show confidence circles for 80%, 90%, and 99% landing zones
- Will print statistics including mean landing zone distance and bearing

This test case uses a single day of wind data, which helps verify the basic functionality of the wind data processing and simulation systems.
