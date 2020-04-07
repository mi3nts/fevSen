Fever Sensor

Running the Sensor 
1) Right Click and Open a Terminal
2) Run the following command on the terminal:
cd ~/gitHubRepos/Lakitha/fevSen/firmware/ && sudo ./runAll.sh
Enter the PW 'teamlary' if prompted 


Halting the sensor 
1) Right Click on the Desktop and Open a Terminal  
2) Run the following command on the terminal:
cd ~/gitHubRepos/Lakitha/fevSen/firmware/ && sudo ./stopAll.sh
Enter the PW 'teamlary' if prompted

Data Storage
1)Since a single data frame for all 3 layes(Visual:RGB Image, 
Thermal: Celcius, and Distance:cm) is 6 mb. All data which is 
10 minutes or older is deleted. Make sure to synce the data to 
your server @ line 87 of 
~/gitHubRepos/Lakitha/fevSen/firmware/jetsonReaderMarch20.py
or run a crontab to synce the following folder:
/home/teamlary/mintsData/val


Data Visualization/Validation 
1) Right Click on the Desktop and Open a Terminal  
2) Run the following command on the terminal:
cd ~/gitHubRepos/Lakitha/fevSen/firmware/ && python3 jetsonVeiwerMarch20.py
Enter the PW 'teamlary' if prompted

To visualize an example data set please uncomment line 26 of 
~/gitHubRepos/Lakitha/fevSen/firmware/jetsonVeiwerMarch20.py
and repeat instructions on Data Visualization/Validation









 



