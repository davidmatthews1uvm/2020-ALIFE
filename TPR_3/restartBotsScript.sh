sudo kill -9 `ps -ax | grep runForever | awk '{print $1}'`
sudo kill -9 `ps -ax | grep simulator  | awk '{print $1}'`

cd /Users/twitchplaysrobotics/Dropbox/JoshBongard/0_Code/Master_Vader_1_from_2019_02_11_to____________0916758/TPR_3

sudo nice -n -19 /usr/local/bin/python3 runForever.py 

