![alt text](https://raw.githubusercontent.com/gabeleibo/sc_net/master/graphs/network_layer1.jpeg)

*Nodes with a sum of followers and following over 800 are considered "celebrities" and are not shown.*

### How to run the Scraper
*Running the script*
1. Install [Anaconda](https://anaconda.org/anaconda/python) and create a new environment
```
conda create -n sc_env python=3.5 anaconda
source activate sc_env
pip install -r requirements.txt
```
2. Download the Chrome Web Driver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads)
3. Move the Chrome Driver to the environment bin (ROOTUSER/anaconda/envs/sc_env/bin)

*Creating the 'friend' network*
1. Run layer0.py - ensure .process() keep_celebs attribute is set to False
2. In the output folder, duplicate layer0.json and call it layer1.json
3. Run layer1.py
4. Repeat Steps 2-3 until you reach the desired network layer depth  
