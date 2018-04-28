from datetime import datetime
import pickle

with open('timetable.pkl', 'rb') as f:
    timetable = pickle.load(f)

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
