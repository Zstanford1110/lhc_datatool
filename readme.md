Minimal Path to Awesome:

1. Clone the Github repo with command: git clone https://github.com/Zstanford1110/lhc_datatool.git
2. Navigate into the /lhc_datatool folder
3. Place the Aptabase generated .csv into the /input folder. Only the .csv you want to load should be in there, delete old .csv files if present
4. Navigate to /lhc_datatool/src directory
5. Run the command 'python main.py' to execute the script
6. Look for the report.pdf output file in the /src directory
7. Rinse and repeat for any sample of LHC data as long as the events have not been modified in the C# code.

Note: If any new event types are added or existing event types are modified in the game code, the script will have to be updated to account for that change. It has been built with the existing event structure in mind. 