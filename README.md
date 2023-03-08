# DistributedSystemModel
This project simulates a small asynch distributed system


## How to use
Run `python simulate.py` in the terminal, and the log files will be generated with the logs corresponding to the specs. Each log will have a port number associated with it in the filename. The main terminal will also output the rate of the macbhine associated with each port for ease of understanding and analysis. 


## Testing
To test our code, run `pytest --cov=./ test_simulate.py`. Note that since we were given the skeleton code
for setting up the connections between sokcets, the tests only test our clock logic. 

