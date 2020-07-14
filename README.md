
## Instructions for setting up and running TPR

Please view the Dependencies.md file for a list of dependencies you will need to have installed. These dependences are also included in this document however you may prefer to pre-install all of the software you will need.

Instructions for getting TPR v3.0 up and running.


1. Install ODE with assertions turned off.

    1. Navigate into the ode-0.12 directory (./pyrosim/pyrosim/simulator/ode-0.12).

    1. Type ./configure --disable-asserts --enable-double-precision

    1. Type make -jx (Replace x with number of cores. If unsure use 2.)

    1. Return to the main directory.

2. Make Pyrosim
    1. Go up to the ./pyrosim/pyrosim/simulator directory and...

    1.  If on linux, install build-essential and freeglut3-dev

        1. Ex. sudo apt-get install build-essential freeglut3-dev

    1. Type make -jx (Replace x with number of cores. If unsure use 2.)

3. Install GraphViz and Pygraphviz

    1. If on mac...
        1. google: 'install homebrew' and follow the instructions.

        1. brew install graphviz

        1. pip3 install pygraphviz

        or, if that doesn't work,

        1. pip3 install --install-option="--include-path=/usr/local/include/graphviz/" --install-option="--library-path=/usr/local/lib/graphviz" pygraphviz

    2. If on Linux
        1. Install graphviz

            1. Ex. sudo apt-get install graphviz libgraphviz-dev pkg-config

        1. pip3 install pygraphviz

1. Create or download word2vec vector space database.
    1. If you are a member of the MECLab, visit the TPR_3 developers manual (pinned in TPR channel of slack) for details about where to download a prebuilt word2vec vector space database from. Continue to either 4.iii or 4.ii (If you want to rebuild the word 2 vec database from scratch.)
    1. If you are not a member of the MECLab, or if you want to build your own, follow the below instructions at 4.ii.a.
        1. In order to generate a word2vec databse, you will need to have word2vec embedding file. Go to https://code.google.com/archive/p/word2vec/ to either download a prebuilt word2vec embedding file, or to download the code to build your own. If you choose to build your own, follow Google's instructions on the above linked website.
        2. After you have your word2vec embeddings, you will need to install gensim (pip3 install gensim). Next, move the word2vec embeddings file into the database directory and run python3 word2vecDatabase.py. Follow the on-screen instructions to create your own word2vec vector space database. Please note that the current implementation of converting a vector encoding file into a vector space database uses a lot of RAM. It would be possible to load part of the file in order to reduce the RAM load, however this has not been implemented.
    1. Please move your word2vec vector space database into the database directory (if it is not already there).

1. Please create an empty directory called 'data' in the main TPR directory. All data files, as well as the tpr database, will be stored in here.

    1. Now, whenever you want to simulate the robots, do the following.

    1. cd into TPR_3 directory

    1. python3 runForever.py. If you are setting up TPR for the first time, or upgrading from a previous version, please see 5.iii.a for initialzation instructions.
        1. Run python3 reset.py to reset and initialize the database. This script will also initialize the data directory with robots to prepare for running python3 runForever or python3 chatbot.py (See Section 5 for more about the chatbot).

    1. Pause the simulation by hitting ctrl-p

1. Start up the chatbot
    1. If you are installing TPR for the first time, or upgrading from a previous version, please run the python3 reset.py script found in the TPR_3 subfolder of TPR.
        1. If you have already run in this in Section 4, you do not need to run it again.
        
    1. Get a Twitch oauth password at https://twitchapps.com/tmi/

    1. Create a credentials.credentials text file in the root directory of your TPR_3 project. On the first line put your oauth password. On the second line put your channel name. Do not include the # character in front of either line.

    1. The channel name is case sensitive, so make sure you use the actual name of the channel.
    
    1. Navigate to the chatbot folder and type python3 chatbot.py

    1. If you are deploying TPR, do the following. Periodically the chat bot can go down. To kill and restart it every minute...

        1. Check that the path in restartScript.sh is correct.

        1. Type tty

        1. Get the result (something like /dev/ttys002) and paste it to the end of this string...
        ```
        * * * * * /Users/twitchplaysrobotics/Dropbox/JoshBongard/0_Code/TPR_3/TPR_3/restartScript.sh > /dev/ttys002
        ```
        1. (make sure the path above is correct.)

        1. ...and insert this string into a cron job using crontab -e

1. Start up other recurring jobs by adding these to your cron job using crontab -e:

    ```
    * * * * * ~/Dropbox/JoshBongard/0_Code/TPR_3/passiveGame/scripts/unlockBotsScript.sh
    ```

    ```
    * * * * * ~/Dropbox/JoshBongard/0_Code/TPR_3/passiveGame/scripts/unlockEnvsScript.sh 
    ```

1. Start broadcasting to your Twitch channel using OBS.

    1. Download and install OBS.

    1. Get the stream key from your twitch channel.

    1. Insert the stream key into OBS.

    1. Click 'start streaming' on OBS.

1. If you want to train interesting robots to show to the crowd...

    1. cd into school directory

    1. python3 createFirstGrade.py

    1. Let it run continuously

1. Performance issues:

    1. This code uses the Samantha voice on Mac. 

        1. To update the quality of her voice, go to Apple > System Preferences > Accessibility > Speech 

        1. Click on the speaker's name in the top right, and click on Customize...

        1. Deselect all names except Samantha, and click 'update'.

        1. If you do not see 'update', that's because Samantha's voice is up to date.

    1. You may notice that the simulation pauses for a few seconds. This can be interrupted by moving the mouse. If you see this, go to Apple > System Preferences > Energy Saver and unlick 'Automatic graphics switching'.

