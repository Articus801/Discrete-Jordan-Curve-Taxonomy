import numpy as np

def generate_dynamic_bumpy_bezier(n):
    """
    Generates the exact same bumpy shape family, scaled dynamically
    to the requested coordinate resolution.
    """
    t = np.linspace(0, 2*np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3*t) + 0.08 * np.cos(5*t)
    return np.column_stack((r*np.cos(t), r*np.sin(t)))

def analyze_curve_ccrt(curve):
    """
    Executes the Central Chord Radial Transform (CCRT) to map out the midpoint straws.
    """
    chords = []
    for x in curve:
        # Opposite ray target
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.linalg.norm(x - y)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})
    return chords

def hunt_all_squares(chords, tol_len, tol_mid, tol_ortho=0.1):
    """
    Sweeps the dataset exhaustively to isolate unique inscribed squares.
    """
    n = len(chords)
    found_squares = []

    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']

        for j in range(i + 1, n):
            c2 = chords[j]

            # Skip checking a chord against its own spatial inverse
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) < 1e-4 and \
               np.linalg.norm(c1['x'] - c2['y']) < 1e-4:
                continue

            # Condition A: Length Match
            if abs(c1['length'] - c2['length']) > tol_len:
                continue

            # Condition B: Overlapping Midpoints
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) > tol_mid:
                continue

            # Condition C: Perpendicular / Orthogonal Chords
            v2 = c2['x'] - c2['y']
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 < 1e-6 or norm2 < 1e-6:
                continue
            dot_product = np.dot(v1, v2) / (norm1 * norm2)

            if abs(dot_product) < tol_ortho:
                # Deduplicate entries sharing roughly the same midpoint space
                duplicate = False
                for sq in found_squares:
                    if np.linalg.norm(sq['midpoint'] - c1['midpoint']) < 0.05:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append(c1)

    return len(found_squares)

if __name__ == "__main__":
    print("====================================================")
    print("   JORDAN CURVE RESOLUTION CONVERGENCE SCANNER     ")
    print("====================================================\n")

    # Resolutions to scan
    resolutions = [100, 300, 600, 1200]

    for N in resolutions:
        curve = generate_dynamic_bumpy_bezier(N)
        chords = analyze_curve_ccrt(curve)

        # DYNAMIC TOLERANCE SCALING: As the grid gets tighter (N increases),
        # the spatial distance between adjacent coordinate points shrinks.
        # We tighten tolerances proportionally so we don't pick up false positives.
        current_tol_len = 0.08 if N == 100 else (0.05 if N <= 600 else 0.03)
        current_tol_mid = 0.08 if N == 100 else (0.05 if N <= 600 else 0.03)

        squares_found = hunt_all_squares(chords, tol_len=current_tol_len, tol_mid=current_tol_mid)

        print(f"Sampling Resolution N = {N:4d} | Chords: {len(chords):4d} | Verified Squares: {squares_found}")

    print("\nSweep Complete.")
