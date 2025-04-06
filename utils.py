import random
from datetime import datetime

def format_datetime(dt=None):
    """
    Format datetime object or current time to string
    
    Args:
        dt (datetime, optional): Datetime object to format. If None, use current time.
        
    Returns:
        str: Formatted datetime string
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def generate_random_stats(base_hp=20, base_other=5, variation=2):
    """
    Generate random monster stats with some variation
    
    Args:
        base_hp (int): Base HP value
        base_other (int): Base value for other stats
        variation (int): Amount of random variation (+/-)
        
    Returns:
        dict: Dictionary of randomized stats
    """
    return {
        "HP": random.randint(base_hp - variation, base_hp + variation),
        "atk": random.randint(base_other - variation, base_other + variation),
        "def": random.randint(base_other - variation, base_other + variation),
        "spA": random.randint(base_other - variation, base_other + variation),
        "spD": random.randint(base_other - variation, base_other + variation),
        "Spe": random.randint(base_other - variation, base_other + variation)
    }
