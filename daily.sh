#!/bin/bash

/usr/bin/python3 /home/kiran/code/RetailProject/DailyDataGen.py
sleep 1s
/usr/bin/python3 /home/kiran/code/RetailProject/LoadCsvDaily.py
sleep 1s
/usr/bin/python3 /home/kiran/code/RetailProject/Analytic.py