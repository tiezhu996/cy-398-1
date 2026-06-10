from app.constants.points import POINT_RULES

def calculate_points(category: str, weight_kg: float) -> int:
    return max(1, int(POINT_RULES.get(category, 3) * max(weight_kg, 0.1)))
