import uuid
import time
import random
from datetime import datetime, timedelta
from typing import List, Any

def generate_unique_id(prefix: str = "IBN") -> str:
    """Generate a unique identifier for intent records."""
    timestamp = int(time.time() * 1000)
    random_part = uuid.uuid4().hex[:12]
    return f"{prefix}_{timestamp}_{random_part}"

def random_choice(items: List[Any]) -> Any:
    """Select a random item from a list."""
    return random.choice(items)

def random_int(min_val: int, max_val: int) -> int:
    """Generate a random integer within range."""
    return random.randint(min_val, max_val)

def random_float(min_val: float, max_val: float, decimals: int = 2) -> float:
    """Generate a random float within range."""
    return round(random.uniform(min_val, max_val), decimals)

def current_timestamp() -> str:
    """Get current timestamp in ISO format."""
    return datetime.now().isoformat()

def random_timestamp_within_days(days: int) -> str:
    """Generate a random timestamp within the last N days."""
    now = datetime.now()
    random_days = random.uniform(0, days)
    past_time = now - timedelta(days=random_days)
    return past_time.isoformat()
