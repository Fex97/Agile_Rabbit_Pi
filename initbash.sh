#!/bin/bash

clear
echo "
 __          __  _                            _______      _____       _     _     _ _     _____ _ 
 \ \        / / | |                          |__   __|    |  __ \     | |   | |   (_) |   |  __ (_)
  \ \  /\  / /__| | ___ ___  _ __ ___   ___     | | ___   | |__) |__ _| |__ | |__  _| |_  | |__) | 
   \ \/  \/ / _ \ |/ __/ _ \|  _   _ \ / _ \    | |/ _ \  |  _  // _  |  _ \|  _ \| | __| |  ___/ |
    \  /\  /  __/ | (_| (_) | | | | | |  __/    | | (_) | | | \ \ (_| | |_) | |_) | | |_  | |   | |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|    |_|\___/  |_|  \_\__,_|_.__/|_.__/|_|\__| |_|   |_|
                                                                                                   
                                                                                                   
"
sudo poff fona

python /home/pi/programs/git/Agile_Rabbit_Pi/onstartupV2.py
echo "done..."

