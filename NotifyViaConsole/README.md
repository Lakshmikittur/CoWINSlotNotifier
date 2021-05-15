## CoWIN Slot Finder


A set of python scripts that uses CoWIN Open APIs to notify when appointment is available.

#### Steps
- Install Python version 3 if not already installed. See this for instructions: [Install Python3](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/)
- Depending on your operating system, install requirements using either of following commands: 
  - `pip3 install -r requirements.txt`
  - `python-pip3 install -r requirements.txt`
  - `pip install -r requirements.txt`
- Edit [DistrictsData.json](DistrictsData.json) file using district id from [StatesDistricts.json](../NotifyViaEmail/StatesDistricts.json)
- Run *FindSlots.py* one time using `python FindSlots.py` OR `python3 FindSlots.py`
- To run *FindSlots.py* every 10 seconds, execute *Scheduler.py* using `python Scheduler.py` OR `python3 Scheduler.py`
