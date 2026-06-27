import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# PHASE 1: GENERATE JORDAN CURVE FAMILIES
# ==========================================
def generate_circle(n=300):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    return np.column_stack((np.cos(t), np.sin(t)))

def generate_ellipse(n=300, a=1.4, b=0.7, angle_deg=45):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    x = a * np.cos(t)
    y = b * np.sin(t)
    rad = np.radians(angle_deg)
    c, s = np.cos(rad), np.sin(rad)
    return np.column_stack((x*c - y*s, x*s + y*c))

def generate_bumpy_bezier(n=300):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    # Modulation creates continuous "unsmooth lumps" without crossing self
    r = 1.0 + 0.15 * np.sin(3*t) + 0.08 * np.cos(5*t)
    return np.column_stack((r*np.cos(t), r*np.sin(t)))

# ==========================================
# PHASE 2: CENTRAL CHORD RADIAL TRANSFORM
# ==========================================
def analyze_curve(curve):
    """
    Moves point x along the curve, automatically maps y on the opposite side
    through the center (0,0), and collects lengths and midpoints.
    """
    midpoints = []
    chords = []

    for x in curve:
        # Step 5 & 6: Find y on the line passing through center
        # Since center is at (0,0), y is approximately closest to the inverted point -x
        dists = np.hypot(curve[:,0] + x[0], curve[:,1] + x[1])
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.hypot(x[0] - y[0], x[1] - y[1])

        midpoints.append(midpoint)
        chords.append({
            'x': x,
            'y': y,
            'midpoint': midpoint,
            'length': length
        })

    return np.array(midpoints), chords

# ==========================================
# PHASE 3: AUTOMATED INSCRIBED SQUARE HUNTER
# ==========================================
def hunt_squares(chords, tol_len=0.04, tol_mid=0.04, tol_ortho=0.1):
    """
    Scans the gathered chord structures ('straws') to find two chords that:
    1. Share nearly the exact same midpoint.
    2. Have nearly the exact same length.
    3. Are perpendicular to each other.
    """
    n = len(chords)
    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']
        for j in range(i + 1, n):
            c2 = chords[j]

            # Condition A: Matching Length
            if abs(c1['length'] - c2['length']) > tol_len:
                continue

            # Condition B: Overlapping Midpoints
            mid_dist = np.hypot(c1['midpoint'][0] - c2['midpoint'][0],
                                c1['midpoint'][1] - c2['midpoint'][1])
            if mid_dist > tol_mid:
                continue

            # Condition C: Perpendicular / Orthogonal Chords (Dot product ~ 0)
            v2 = c2['x'] - c2['y']
            dot_product = np.dot(v1, v2) / (c1['length'] * c2['length'])
            if abs(dot_product) < tol_ortho:
                return (c1, c2) # Found a valid inscribed square profile

    return None
