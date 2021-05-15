## CoWIN Slot Finder( with Email)


A set of python scripts that uses CoWIN Open APIs to notify when appointment is available through email.

#### Steps
- Install Python version 3 if not already installed. See this for instructions: [Install Python3](https://www.geeksforgeeks.org/download-and-install-python-3-latest-version/)
- Depending on your operating system, install requirements using either of following commands: 
  - `pip3 install -r requirements.txt`
  - `python-pip3 install -r requirements.txt`
  - `pip install -r requirements.txt`
- Edit [AllEmailData.json](https://github.com/Lakshmikittur/CoWINSlotNotifier/blob/main/NotifyViaEmail/AllEmailData.json) file using district id from [StatesDistricts.json](https://github.com/Lakshmikittur/CoWINSlotNotifier/blob/main/NotifyViaEmail/StatesDistricts.json)
- Run *FindSlotsAndEmail.py* one time using `python FindSlotsAndEmail.py` OR `python3 FindSlotsAndEmail.py`
- To run *FindSlotsAndEmail.py* every 10 seconds, execute *Scheduler.py* using `python Scheduler.py` OR `python3 Scheduler.py`
