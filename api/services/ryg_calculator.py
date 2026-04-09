"""RYG (Red/Yellow/Green) threshold calculator."""
from api.models.schemas import ThresholdConfig


def calculate_status(value: float, config: ThresholdConfig) -> str:
    """
    Calculate RYG status based on value and thresholds.
    
    direction="higher_is_worse": value >= red → RED, value >= yellow → YELLOW
    direction="lower_is_worse":  value <= red → RED, value <= yellow → YELLOW
    """
    if config.direction == "higher_is_worse":
        if value >= config.red:
            return "red"
        elif value >= config.yellow:
            return "yellow"
        return "green"
    else:
        # lower_is_worse
        if value <= config.red:
            return "red"
        elif value <= config.yellow:
            return "yellow"
        return "green"


def calculate_achievement(actual: float, target: float) -> float:
    """Calculate achievement percentage."""
    if target == 0:
        return 0.0
    return round((actual / target) * 100, 1)


def get_status_from_achievement(pct: float, higher_is_better: bool = True) -> str:
    """
    Derive status from achievement percentage.
    
    For metrics where higher is better (e.g., revenue):
      < 70% = RED, < 90% = YELLOW, >= 90% = GREEN
    
    For metrics where lower is better (e.g., churn):
      > 130% = RED, > 110% = YELLOW, <= 110% = GREEN
    """
    if higher_is_better:
        if pct < 70:
            return "red"
        elif pct < 90:
            return "yellow"
        return "green"
    else:
        if pct > 130:
            return "red"
        elif pct > 110:
            return "yellow"
        return "green"


def get_overall_status(summary: dict[str, int]) -> str:
    """
    Determine overall status from KPI summary counts.
    Any RED → overall RED
    Any YELLOW + no RED → overall YELLOW
    All GREEN → overall GREEN
    """
    red_count = summary.get("red", 0)
    yellow_count = summary.get("yellow", 0)
    
    if red_count > 0:
        return "red"
    elif yellow_count > 0:
        return "yellow"
    return "green"
