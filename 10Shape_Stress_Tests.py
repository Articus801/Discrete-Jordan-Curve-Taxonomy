import matplotlib
# Non-interactive backend ensures no terminal lock-ups
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os

# ==========================================
# PHASE 1: POLYGONAL GEOMETRY GENERATORS
# ==========================================
def generate_polygon(sides=3, n_points=400, regular=True):
    """Generates regular or irregular centered polygonal boundaries."""
    angles = np.linspace(0, 2 * np.pi, sides, endpoint=False)

    if not regular:
        # Add asymmetry to create an irregular hexagon
        np.random.seed(42) # Pin seed so it remains consistent
        angles += np.random.uniform(-0.15, 0.15, sides)
        radii = np.random.uniform(0.7, 1.3, sides)
    else:
        radii = np.ones(sides)

    vertices = np.column_stack((radii * np.cos(angles), radii * np.sin(angles)))
    vertices = np.vstack([vertices, vertices[0]]) # Close polygon path

    # Interpolate smoothly along edges to create high-density point sets
    pts_per_side = n_points // sides
    curve_pts = []
    for i in range(sides):
        p1, p2 = vertices[i], vertices[i+1]
        for t in np.linspace(0, 1, pts_per_side, endpoint=False):
            curve_pts.append((1-t)*p1 + t*p2)

    # Center the coordinate system strictly to the mean center of mass
    curve_pts = np.array(curve_pts)
    curve_pts -= np.mean(curve_pts, axis=0)
    return curve_pts

def generate_koch_snowflake(steps=3, n_points=384):
    """Generates a complete, centered Koch Snowflake loop."""
    pts = np.array([[0.0, 0.75], [-0.65, -0.375], [0.65, -0.375], [0.0, 0.75]])
    for _ in range(steps):
        next_pts = []
        for i in range(len(pts) - 1):
            p1, p2 = pts[i], pts[i+1]
            v = p2 - p1
            a = p1 + v / 3.0
            b = p1 + 2.0 * v / 3.0
            r = np.array([-v[1], v[0]]) * (np.sqrt(3) / 6.0)
            mid = p1 + v / 2.0
            peak = mid + r
            next_pts.extend([p1, a, peak, b])
        next_pts.append(pts[-1])
        pts = np.array(next_pts)

    pts = pts[:-1]
    pts -= np.mean(pts, axis=0) # Zero out center of mass
    return pts

# ==========================================
# PHASE 2: CORE ANALYSIS ENGINES
# ==========================================
def analyze_curve_ccrt(curve):
    midpoints = []
    chords = []
    for x in curve:
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]
        midpoint = (x + y) / 2.0
        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': np.linalg.norm(x - y)})
    return np.array(midpoints), chords

def hunt_squares_ccrt(chords, tol=0.05):
    n = len(chords)
    found_squares = []
    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']
        for j in range(i + 1, n):
            c2 = chords[j]
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) > tol: continue
            if abs(c1['length'] - c2['length']) > tol: continue

            v2 = c2['x'] - c2['y']
            norm1, norm2 = np.linalg.norm(v1), np.linalg.norm(v2)
            if norm1 < 1e-6 or norm2 < 1e-6: continue
            if abs(np.dot(v1, v2) / (norm1 * norm2)) < 0.12:
                duplicate = False
                for sq in found_squares:
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.08:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))
    return found_squares

# ==========================================
# PHASE 3: STRESS TEST EXECUTION
# ==========================================
if __name__ == "__main__":
    print("====================================================")
    print("      JORDAN CURVE GEOMETRIC STRESS TESTS           ")
    print("====================================================\n")

    test_shapes = {
        'Triangle': lambda: generate_polygon(sides=3, n_points=399, regular=True),
        'Regular_Hexagon': lambda: generate_polygon(sides=6, n_points=402, regular=True),
        'Irregular_Hexagon': lambda: generate_polygon(sides=6, n_points=402, regular=False),
        'Koch_Snowflake': lambda: generate_koch_snowflake(steps=3)
    }

    for name, generator in test_shapes.items():
        print(f"Running stress test on shape: {name.upper()}")
        curve = generator()
        midpoints, chords = analyze_curve_ccrt(curve)

        # Adjust tolerances based on shape complexity to catch genuine intersections
        current_tol = 0.06 if 'Hexagon' in name else 0.04
        squares = hunt_squares_ccrt(chords, tol=current_tol)

        print(f" -> Boundary Vertices Processed: {len(curve)}")
        print(f" -> Inscribed Squares Isolated: {len(squares)}")

        # Plot and save diagnostic profile
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

        # Panel 1: Complete Workspace with Square Overlays
        ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Shape Boundary')
        ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, zorder=3, label='Midpoint Cloud')

        for sq_idx, sq in enumerate(squares):
            c1, c2 = sq
            pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
            ax1.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=2.5, zorder=4,
                    label="Inscribed Square" if sq_idx == 0 else "")

        ax1.set_title(f"{name} Analysis Workspace")
        ax1.set_aspect('equal')
        ax1.grid(True, linestyle=':', alpha=0.5)
        ax1.legend(loc='upper right')

        # Panel 2: Isolated Caustic Straws
        for i in range(0, len(midpoints), 2):
            ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.2, lw=0.8)
        ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=2)
        ax2.axhline(0, color='black', lw=0.5, linestyle='--')
        ax2.axvline(0, color='black', lw=0.5, linestyle='--')
        ax2.set_title(f"{name} Isolated Caustic Straws")
        ax2.set_aspect('equal')
        ax2.grid(True, linestyle=':', alpha=0.5)

        plt.tight_layout()
        output_filename = f"stresstest_{name.lower()}.png"
        plt.savefig(output_filename, dpi=150)
        plt.close()
        print(f" -> Diagnostic charts exported as: {output_filename}\n")

    print("====================================================")
    print("ALL GEOMETRIC STRESS TESTS COMPLETED SUCCESSFULLY!")
    print("Review your folder for the 'stresstest_*.png' outputs.")
    print("====================================================")
