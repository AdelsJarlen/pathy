
import time
import threading
from math import floor

# spaces = "          "
# progress = f"[{spaces}]"

# print("\rProcessing" + progress, end='')

# for i in range(10):
#     time.sleep(.5)
#     spaces = spaces[:i] + "█" + spaces[i+1:] 
#     print("\rProcessing" + f"[{spaces}] {(i+1) * 10}%", end='')

# print("\nDONE!")

def create_progress_bar(message: str, progress: int, count: int) -> str:
    
    # Setting up how wide the progress bar should be
    num_spaces = 100
    spaces = ""
    for i in range(num_spaces - 1): spaces += " "
    
    
    percentage = floor(progress / count * 100)
    
    for i in range(floor(num_spaces * percentage / 100)):
        spaces = (spaces[:i] + "█" + spaces[i+1:])
    
    s = f"{message} [{spaces}] {percentage + 1}%, {progress} of {count}"
    
    return "\r" + s
