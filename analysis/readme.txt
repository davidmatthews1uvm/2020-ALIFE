This is a ReadMe for the analysis section of TPR:
Written by Eli Gitelman and Alex Ram.

If you have questions or concerns feel free to slack us in the MECLab slack or email either of us at egitelma@uvm.edu or aram1@uvm.edu


1. Data collection and analysis

	tensorcreator.py is a data organization and sanitization file. In order to run this file you’ll need to make sure you’ve done everything in the TPR developers manual that involves installing programs/models/APIs upto and including preparing your machine to run pyrosim and the database files. I recommend running TPR3/runForever.py first to see if your environment is running properly.

	Once you’ve done the above, you’ll need to source your data from the vader1 dropbox account. The information for this is in the TPR developers manual. You will want to save the data from vader1 in a folder named data in the main TPR folder. Once you have that data file, proceed into the database folder and run deleteNonReinforcedEvaluations.py and queryAll.py. This will delete any robots that are never reinforced, as well as showing you that you do in fact have data. 

	Now you are ready to run tensorcreator.py, included in the file are several methods for creating a reinforcement array, tensor of the robot sensor data that is of shape [sensors,timesteps,robots] and the vector for each unique command. There’s a Boolean variable NEW_DATABASE on line 13, this should be set true for the data collected from May 7th to June 18th and false otherwise. The variable unique_commands on line 36 is set to make a new reinforcement and sensordata array for each command but can be changed to just query a subset of commands. For example, by changing line 36 to unique_commands = [‘move’] you will only produce a reinforcement and sensordata pickle file on the word move. This will include all robots evaluated on the word move.

plot.py, Running this file will help show you whether there is some correlation between the reinforcements and the sensordata. In order to run this file make sure that you have first run tensorcreator.py, then make sure in plot.py the pickled files that you are opening are both correctly named and from the same command. 

2. Using the critic

	a. Run tensor creator (TPR3/analysis/tensorCreator.py) and collect the sensor data and reinforcements. 
		i. The tensorCreator file will produce sensor data for all robots that have been reinforced on a command. For example: 			if data on the move command is needed, use sensordata_move.p and Reinforcements_move.p
	
	b. Multiple databases have accumulated as updates have been made to TPR. These can be found on the dropbox (with links in the 		TPR manual). Sensor data and reinforcement pickle files can be produced for each database and merged using makeInput.py
		i. Filenames need to be changed for each database to match that of makeInput.py. For example: The oldest datasets sensor 		data for move is named sensordata_move1.p and the newest is named sensordata_move3.p. Run tensorcreator.py using each 			database and make the pickle file name changes so you have a sensordata and reinforcements pickle file for each 			database.
		ii. Don’t forget to change the NEW_DATABASE Boolean in tensorcreator based on which database is being used.
		iii. Run makeInput.py. This will output all_reinforcements.p and all_sensordata.p which will be used at input to the 			network.

	c. Install keras 
		i. Install anaconda on your machine, an installer can be found online
		ii. Type conda install scikit-learn
		iii. Type conda install keras
		iv. If on the VACC copy all_sensordata.p, all_reinforcements.p and TPR_critic.py to your directory. Also, you’ll need to 		keep in mind that some computers on the VACC have a hard time running keras so you can avoid using those machines by 			typing export OMP_NUM_THREADS=1
	
	d. Now run TPR_critic.py to get accuracies for the real data and for a control. These values will be stored in cvscores.p and 		cvscores_control.p, and will be used in manWhitneyU.py. cvscores_bool.p and cvscores_bool_control.p can also be generated, which 	will round the reinforcements to 1 or -1, leavings 0’s as 0.

	e. Once the above process is finished, run manWhitneyU.py to see if the critic is producing significantly better results on the 	real data than the shuffled control data. 
		i. You will need to run the critic on a minimum of 30 folds to use this test.
		ii. To see if everything is running for you like it did for me you can make a couple changes to the code that will make 		it run quickly, even on your local machine. Un-comment lines 32-37 in TPR_network.py to use just the first 50 data 			points in the dataset. Go to line 77 and set num_of_folds = 2, also on line 78 set num_of_epochs = 2.
		iii. This should take about 5 minutes. Once it’s done you can run manWhitneyU.py. The output that is printed to the 			console should match:
			With reinforcements between -1 and 1
			0.18% (+/- 0.02%)
			And control:
			0.24% (+/- 0.08%)
			With reinforcements that are rounded to -1 or 1
			0.18% (+/- 0.02%)
			And control:
			0.24% (+/- 0.08%)
			Mann Whitney with reinforcements between -1 and 1
			Statistics=1.500, p=0.500
			Same distribution (fail to reject H0)
			Man Whitney with reinforcements that are rounded to -1 or 1
			Statistics=1.500, p=0.500
			Same distribution (fail to reject H0)
		iv. This is obviously bad results because there was not enough data, folds or training epochs.
