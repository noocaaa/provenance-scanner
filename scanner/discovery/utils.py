"""
File: utils.py
Author: Noelia Carrasco Vilar
Date: 2025-12-08
Description:
    Useful functions. 
"""

import subprocess
import re

def run(cmd):
    """Run a shell command and return output as string."""
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL).decode()
    except:
        return ""

def extract_regex(pattern, text, default=""):
    m = re.search(pattern, text, re.MULTILINE)
    return m.group(1).strip() if m else default