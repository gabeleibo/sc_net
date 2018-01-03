![alt text](https://raw.githubusercontent.com/gabeleibo/sc_net/master/graphs/network_layer1.jpeg)

### How to run the Scraper
1. Install [Anaconda](https://anaconda.org/anaconda/python) and create a new environment
```
conda create -n sc_env python=3.5 anaconda
source activate sc_env
pip install -r requirements.txt
```
2. Download the Chrome Web Driver [here](https://sites.google.com/a/chromium.org/chromedriver/downloads)
3. Move the Chrome Driver to the environment bin (ROOTUSER/anaconda/envs/sc_env/bin)
4. Run layer0.py
5. In output, duplicate layer0.json and call it layer1.json
6. Run layer1.py
7. Repeat Steps 5-6 until you reach the desired network layer depth  
