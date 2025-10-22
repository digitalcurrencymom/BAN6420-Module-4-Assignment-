Netflix Shows & Movies — Analysis

Files:
- analyze_netflix.py — Python script that reads the provided CSV, cleans data, generates two plots (top genres, ratings distribution), saves cleaned CSV and plots, and creates a zip file.
- plot_r.R — R script that recreates the top genres plot using ggplot2.
- Netflix_shows_movies.zip — Output ZIP containing cleaned CSV, plots and original CSV (created by running the Python script).

How to run (Python):
1. Ensure Python 3.8+ is installed and packages pandas, matplotlib, seaborn are available.
   You can install them with:

pip install pandas matplotlib seaborn

2. Place the source CSV at:
C:\Users\HP\Downloads\netflix_data (1).csv

3. Run the script from PowerShell:

& C:/Path/To/Python/python.exe C:/Users/HP/Downloads/Netflix_shows_movies/analyze_netflix.py

How to run (R):
1. Ensure R is installed with packages ggplot2, dplyr, readr, tidyr.
2. From R or RStudio run the script:

source('C:/Users/HP/Downloads/Netflix_shows_movies/plot_r.R')

Outputs will be placed in:
C:\Users\HP\Downloads\Netflix_shows_movies

R notes (what I ran on your machine):
- R version found: R-4.5.1
- Command used to run the R script (PowerShell):
   & 'C:\Program Files\R\R-4.5.1\bin\x64\Rscript.exe' 'C:\Users\HP\Downloads\Netflix_shows_movies\plot_r.R'

Final submission zip:
- A final ZIP named `Netflix_shows_movies_submission.zip` can be created which contains the cleaned CSV, Python plots, the R plot, the original CSV, scripts and README. I created this in your Downloads folder as part of the requested steps.

