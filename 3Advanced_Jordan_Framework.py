import numpy as np

# =====================================================================
# 1. CORE MATH ENGINE: EXHAUSTIVE MULTI-SQUARE HUNTER (Bullet Point 2)
# =====================================================================
def hunt_all_squares(chords, tol_len=0.05, tol_mid=0.05, tol_ortho=0.1):
    """
    Sweeps the entire chord dataset exhaustively to count and isolate
    ALL distinct inscribed squares, strictly avoiding ghost/inverted duplicates.
    """
    n = len(chords)
    found_squares = []

    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']

        for j in range(i + 1, n):
            c2 = chords[j]

            # Prevent matching a chord with its own spatial inverse
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) < 1e-4 and \
               np.linalg.norm(c1['x'] - c2['y']) < 1e-4:
                continue

            # Condition A: Matching Lengths
            if abs(c1['length'] - c2['length']) > tol_len:
                continue

            # Condition B: Overlapping Midpoints
            mid_dist = np.linalg.norm(c1['midpoint'] - c2['midpoint'])
            if mid_dist > tol_mid:
                continue

            # Condition C: Orthogonality (Perpendicular Chords)
            v2 = c2['x'] - c2['y']
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 < 1e-6 or norm2 < 1e-6:
                continue
            dot_product = np.dot(v1, v2) / (norm1 * norm2)

            if abs(dot_product) < tol_ortho:
                # Store unique matches by tracking their unique midpoint profile
                duplicate = False
                for sq in found_squares:
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.05:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))

    return len(found_squares)

# =====================================================================
# 2. TRANSFORM FUNCTIONS & RADIAL ENGINE
# =====================================================================
def analyze_curve_with_center(curve, center_offset):
    """
    Executes CCRT relative to an arbitrary, translated frame of reference center.
    """
    midpoints = []
    chords = []

    for x in curve:
        # Vector pointing from the shifted center to point x
        ray = x - center_offset
        # Find where the opposing ray intersects the curve
        target_direction = center_offset - ray
        dists = np.linalg.norm(curve - target_direction, axis=1)
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.linalg.norm(x - y)

        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})

    return np.array(midpoints), chords

# =====================================================================
# 3. GENERATORS: KOCH FRACTAL SURFACE GENERATOR (Bullet Point 3)
# =====================================================================
def generate_koch_snowflake_loop(steps=3):
    """
    Generates a closed, rough, non-smooth fractal Jordan curve loop.
    """
    # Initial equilateral triangle vertices
    pts = np.array([
        [0.0, 0.866],
        [-0.5, -0.134],
        [0.5, -0.134],
        [0.0, 0.866]
    ])

    for _ in range(steps):
        next_pts = []
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            # Calculate the 3 intermediate fractal points
            v = p2 - p1
            a = p1 + v / 3.0
            b = p1 + 2.0 * v / 3.0
            # Find the outward pointing peak position
            r = np.array([-v[1], v[0]]) * (np.sqrt(3) / 6.0)
            mid = p1 + v / 2.0
            peak = mid + r
            next_pts.extend([p1, a, peak, b])
        next_pts.append(pts[-1])
        pts = np.array(next_pts)

    return pts[:-1] # Return clean closed loop array

def generate_bumpy_bezier(n=500):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3*t) + 0.08 * np.cos(5*t)
    return np.column_stack((r*np.cos(t), r*np.sin(t)))

def generate_ellipse(n=500, a=1.4, b=0.7):
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    return np.column_stack((a * np.cos(t), b * np.sin(t)))

# =====================================================================
# 4. EXECUTION FLOW
# =====================================================================
if __name__ == "__main__":
    print("Executing Extended Research Suite...\n")

    # --- TASK 1: TRANSLATING CENTER EXPERIMENT ---
    print("--- 1. Center Translation Analysis (Ellipse) ---")
    ellipse_curve = generate_ellipse(n=500)

    offsets = [np.array([0.0, 0.0]), np.array([0.1, 0.0]), np.array([0.3, 0.2])]
    for off in offsets:
        mids, _ = analyze_curve_with_center(ellipse_curve, off)
        var_x = np.var(mids[:, 0])
        var_y = np.var(mids[:, 1])
        total_variance = var_x + var_y
        print(f"Center Offset: [{off[0]:.1f}, {off[1]:.1f}] -> Midpoint Structural Variance: {total_variance:.6f}")
    print()

    # --- TASK 2: EXHAUSTIVE COUNTER SYSTEM ---
    print("--- 2. Exhaustive Multi-Square Sweeper ---")
    bumpy_curve = generate_bumpy_bezier(n=600)
    _, bumpy_chords = analyze_curve_with_center(bumpy_curve, np.array([0.0, 0.0]))
    total_squares = hunt_all_squares(bumpy_chords)
    print(f"Total authentic, independent squares verified inside bumpy curve: {total_squares}\n")

    # --- TASK 3: FRACTAL STRESS TEST ---
    print("--- 3. Rough Fractal Boundary Stress Test ---")
    fractal_curve = generate_koch_snowflake_loop(steps=3) # Generates hundreds of jagged segments
    print(f"Fractal loop instantiated with {len(fractal_curve)} boundary vertices.")
    _, fractal_chords = analyze_curve_with_center(fractal_curve, np.array([0.0, 0.366])) # Fractal barycenter
    fractal_squares = hunt_all_squares(fractal_chords, tol_len=0.08, tol_mid=0.08)
    print(f"Total squares isolated inside rough fractal curve: {fractal_squares}")
