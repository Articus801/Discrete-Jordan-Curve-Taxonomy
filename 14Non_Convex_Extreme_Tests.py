import matplotlib
# Guarantee non-interactive terminal execution
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_l_shape(n_points=480):
    """Generates a perfectly centered L-shaped non-convex block boundary."""
    vertices = np.array([
        [-0.5, 0.5], [0.5, 0.5], [0.5, -0.1],
        [0.0, -0.1], [0.0, -0.5], [-0.5, -0.5], [-0.5, 0.5]
    ])

    pts_per_segment = n_points // 6
    curve_pts = []
    for i in range(6):
        p1, p2 = vertices[i], vertices[i+1]
        for t in np.linspace(0, 1, pts_per_segment, endpoint=False):
            curve_pts.append((1-t)*p1 + t*p2)

    curve_pts = np.array(curve_pts)
    curve_pts -= np.mean(curve_pts, axis=0) # Normalize center of mass
    return curve_pts

def generate_starburst(n_points=600):
    """Generates a high-frequency 12-peak radial wave curve profile."""
    t = np.linspace(0, 2 * np.pi, n_points, endpoint=False)
    r = 0.8 + 0.3 * np.sin(12 * t)
    x = r * np.cos(t)
    y = r * np.sin(t)
    curve_pts = np.column_stack((x, y))
    curve_pts -= np.mean(curve_pts, axis=0)
    return curve_pts

# ==========================================
# CORE ANALYSIS PIPELINE
# ==========================================
def analyze_curve_ccrt(curve):
    midpoints, chords = [], []
    for x in curve:
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]
        midpoint = (x + y) / 2.0
        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': np.linalg.norm(x - y)})
    return np.array(midpoints), chords

def hunt_squares_ccrt(chords, tol=0.04):
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
                    # FIXED COMPLETELY: Accessing the first tuple element using index 0
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.08:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))
    return found_squares

if __name__ == "__main__":
    print("====================================================")
    print("     DEEP NON-CONVEX & EXTREME STRESS TESTS         ")
    print("====================================================\n")

    extreme_shapes = {
        'L_Shape': generate_l_shape,
        'Starburst_Waves': generate_starburst
    }

    for name, generator in extreme_shapes.items():
        print(f"Executing stress test matrix: {name.upper()}")
        curve = generator()
        midpoints, chords = analyze_curve_ccrt(curve)

        # Balance precision tuning dynamically
        current_tol = 0.04 if name == 'L_Shape' else 0.05
        squares = hunt_squares_ccrt(chords, tol=current_tol)

        print(f" -> Boundary Data Points: {len(curve)}")
        print(f" -> Squares Extracted: {len(squares)}")

        # Plotting layout logic
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

        # Panel 1: Primary Shape Domain
        ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Shape Boundary')
        ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, zorder=3, label='Midpoint Cloud')

        for sq_idx, sq in enumerate(squares):
            c1, c2 = sq
            pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
            ax1.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=3.0, zorder=4,
                    label="Verified Inscribed Square" if sq_idx == 0 else "")

        ax1.set_title(f"{name} Analysis Canvas")
        ax1.set_aspect('equal')
        ax1.grid(True, linestyle=':', alpha=0.5)
        ax1.legend(loc='upper right')

        # Panel 2: Internal Ray Envelope
        for i in range(0, len(midpoints), 2):
            ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.2, lw=0.8)
        ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=2)
        ax2.axhline(0, color='black', lw=0.5, linestyle='--')
        ax2.axvline(0, color='black', lw=0.5, linestyle='--')
        ax2.set_title(f"{name} Midpoint Caustic Array")
        ax2.set_aspect('equal')
        ax2.grid(True, linestyle=':', alpha=0.5)

        plt.tight_layout()
        output_filename = f"stresstest_extreme_{name.lower()}.png"
        plt.savefig(output_filename, dpi=150)
        plt.close()
        print(f" -> Diagnostic map saved cleanly to: {output_filename}\n")

    print("====================================================")
    print("ALL EXTREME TESTS FINISHED. DATA FOLDER POPULATED.")
    print("====================================================")
