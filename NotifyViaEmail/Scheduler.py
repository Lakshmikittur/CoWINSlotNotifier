#!/usr/bin/env python3

import time
import os
import subprocess

# Run slot finding script every 10 seconds
while True:
    cmd = ["python3", "FindSlotsAndEmail.py"]
    if os.name == 'nt':
        cmd[0] = "python"
    result = subprocess.run(cmd)
    time.sleep(10)
