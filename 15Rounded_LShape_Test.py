import matplotlib
# Guarantee non-interactive terminal execution
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def apply_chaikin_smoothing(vertices, refinements=3, cutting_depth=0.20):
    """
    Applies Chaikin's Corner-Cutting Algorithm to smoothly round off
    sharp polygon corners, mimicking a graphical Bezier curve transition.
    """
    pts = np.array(vertices)
    for _ in range(refinement_steps:=refinement_steps if 'refinement_steps' in locals() else refinements):
        new_pts = []
        n = len(pts)
        for i in range(n):
            p0 = pts[i]
            p1 = pts[(i + 1) % n]

            # Cut the corner by placing two new points along the edge segment
            q = (1.0 - cutting_depth) * p0 + cutting_depth * p1
            r = cutting_depth * p0 + (1.0 - cutting_depth) * p1
            new_pts.extend([q, r])
        pts = np.array(new_pts)
    return pts

def generate_rounded_l_shape(n_points=540):
    """Generates a perfectly smooth, corner-less L-bracket centered at (0,0)."""
    # Raw orthogonal vertices of our L-bracket
    vertices = np.array([
        [-0.5, 0.5], [0.5, 0.5], [0.5, -0.1],
        [0.0, -0.1], [0.0, -0.5], [-0.5, -0.5]
    ])

    # Smooth out the sharp corners using Chaikin refinement
    smoothed_pts = apply_chaikin_smoothing(vertices, refinements=4, cutting_depth=0.18)

    # Interpolate to match the target high-density coordinate point grid
    t_old = np.linspace(0, 1, len(smoothed_pts))
    t_new = np.linspace(0, 1, n_points, endpoint=False)

    x_new = np.interp(t_new, t_old, smoothed_pts[:, 0])
    y_new = np.interp(t_new, t_old, smoothed_pts[:, 1])

    curve = np.column_stack((x_new, y_new))
    curve -= np.mean(curve, axis=0) # Absolute center of mass alignment
    return curve

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
                    # FIXED DEFINITIVELY: sq is a tuple pair. Access chord1 using index 0
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.08:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))
    return found_squares

if __name__ == "__main__":
    print("====================================================")
    print("    ROUNDED NON-CONVEX L-SHAPE TOPOLOGY TEST         ")
    print("====================================================\n")

    print("Analyzing smooth non-convex boundary: ROUNDED_L_SHAPE")
    curve = generate_rounded_l_shape()
    midpoints, chords = analyze_curve_ccrt(curve)

    # Hunting for squares with a well-balanced local tolerance window
    squares = hunt_squares_ccrt(chords, tol=0.04)
    print(f" -> Boundary Coordinates: {len(curve)}")
    print(f" -> Inscribed Squares Isolated: {len(squares)}")

    # Plot layout logic
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))

    # Panel 1: Primary Workspace
    ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Rounded L Boundary')
    ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, zorder=3, label='Midpoint Cloud')

    for sq_idx, sq in enumerate(squares):
        c1, c2 = sq
        pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
        ax1.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=3.0, zorder=4,
                label="Verified Inscribed Square" if sq_idx == 0 else "")

    ax1.set_title("Rounded L-Shape Clean Canvas")
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right')

    # Panel 2: Continuous Straw Caustics
    for i in range(0, len(midpoints), 2):
        ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.2, lw=0.8)
    ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=2)
    ax2.axhline(0, color='black', lw=0.5, linestyle='--')
    ax2.axvline(0, color='black', lw=0.5, linestyle='--')
    ax2.set_title("Rounded L-Shape Caustic Web")
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    output_filename = "stresstest_extreme_rounded_l_shape.png"
    plt.savefig(output_filename, dpi=150)
    plt.close()
    print(f" -> Image saved cleanly to: {output_filename}\n")

    print("====================================================")
    print("ROUNDED NON-CONVEX TEST COMPLETED SUCCESSFULLY!")
    print("====================================================")
