from typing import List, Tuple


def mix_colors(colors: List[Tuple[int, int, int]], weights: List[float]) -> Tuple[int, int, int]:
    """
    Calculate weighted average of RGB values.
    
    Args:
        colors: List of RGB tuples, e.g., [(255, 0, 0), (0, 255, 0)]
        weights: List of weights corresponding to each color, e.g., [0.5, 0.5]
    
    Returns:
        Tuple of (r, g, b) representing the mixed color
    
    Raises:
        ValueError: If colors and weights lists have different lengths or are empty
    """
    if not colors or not weights:
        raise ValueError("Colors and weights lists cannot be empty")
    
    if len(colors) != len(weights):
        raise ValueError("Colors and weights lists must have the same length")
    
    # Normalize weights to sum to 1
    total_weight = sum(weights)
    if total_weight == 0:
        raise ValueError("Total weight cannot be zero")
    
    normalized_weights = [w / total_weight for w in weights]
    
    # Calculate weighted average for each channel
    r = sum(color[0] * weight for color, weight in zip(colors, normalized_weights))
    g = sum(color[1] * weight for color, weight in zip(colors, normalized_weights))
    b = sum(color[2] * weight for color, weight in zip(colors, normalized_weights))
    
    # Round to nearest integer and clamp to valid RGB range (0-255)
    r = int(round(r))
    g = int(round(g))
    b = int(round(b))
    
    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    
    return (r, g, b)