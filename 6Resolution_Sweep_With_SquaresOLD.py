import matplotlib
# Use a non-interactive backend to guarantee the terminal never hangs/freezes
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_dynamic_bumpy_bezier(n):
    """
    Generates our standard bumpy shape family, scaled dynamically
    to the requested coordinate resolution.
    """
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3 * t) + 0.08 * np.cos(5 * t)
    return np.column_stack((r * np.cos(t), r * np.sin(t)))

def analyze_curve_ccrt(curve):
    """
    Executes the Central Chord Radial Transform (CCRT) to map out the midpoint straws.
    """
    midpoints = []
    chords = []
    for x in curve:
        # Find opposing boundary intersection passing through the frame center
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]

        midpoint = (x + y) / 2.0
        length = np.linalg.norm(x - y)

        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})
    return np.array(midpoints), chords

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
                    found_squares.append((c1, c2))

    return found_squares

if __name__ == "__main__":
    print("====================================================")
    print("   JORDAN CURVE RESOLUTION & VISUALIZATION ENGINE    ")
    print("====================================================\n")

    # --- PART 1: THE RESOLUTION CONVERGENCE SCAN ---
    resolutions = [100, 300, 600, 1200]

    for N in resolutions:
        test_curve = generate_dynamic_bumpy_bezier(N)
        _, test_chords = analyze_curve_ccrt(test_curve)

        # Dynamic tolerance scaling based on coordinate grid density
        current_tol_len = 0.08 if N == 100 else (0.05 if N <= 600 else 0.02)
        current_tol_mid = 0.08 if N == 100 else (0.05 if N <= 600 else 0.02)

        squares_found = hunt_all_squares(test_chords, tol_len=current_tol_len, tol_mid=current_tol_mid)
        print(f"Sampling Resolution N = {N:4d} | Chords Checked: {len(test_chords):4d} | Independent Squares Found: {len(squares_found)}")

    print("\nResolution convergence scan finished successfully.")
    print("Generating comprehensive visual files using high-resolution grid (N=1200)...")

    # --- PART 2: GRAPHICAL EXTRACTION AND SQUARE OVERLAY ---
    high_res_N = 1200
    curve = generate_dynamic_bumpy_bezier(high_res_N)
    midpoints, chords = analyze_curve_ccrt(curve)

    # Run the square hunter on the cleanest available resolution
    final_squares = hunt_all_squares(chords, tol_len=0.02, tol_mid=0.02)

    # Initialize our dual-panel workspace
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

    # Left Panel Layout: Complete Workspace
    ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Jordan Curve ($\gamma$)')
    ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, zorder=3, label='Midpoint Cloud')

    # Render chord lines structural background sparsely to avoid visual crowding
    for i in range(0, len(chords), 40):
        c = chords[i]
        ax1.plot([c['x'][0], c['y'][0]], [c['x'][1], c['y'][1]], color='gray', alpha=0.1, lw=1)

    # Draw discovered squares over the workspace in bold green
    square_count = 0
    for sq in final_squares:
        square_count += 1
        c1, c2 = sq
        # Extract the 4 corner points of the verified square
        pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
        ax1.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=3.0, zorder=5,
                 label='Inscribed Square' if square_count == 1 else "")

    ax1.set_title("Central Chord Radial Transform & Inscribed Squares", fontsize=12, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right')

    # Right Panel Layout: Straw Spectrum Mechanics
    for i in range(0, len(midpoints), 4):
        ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.2, lw=0.8)

    ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=2)
    ax2.axhline(0, color='black', lw=0.5, linestyle='--')
    ax2.axvline(0, color='black', lw=0.5, linestyle='--')

    ax2.set_title("Isolated Midpoint Straw Spectrum (High Density Caustics)", fontsize=12, fontweight='bold')
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()

    # Export PNG file directly to directory without firing visual window blockades
    output_filename = "jordan_curve_with_inscribed_squares.png"
    plt.savefig(output_filename, dpi=300)

    print("\n====================================================")
    print(f"SUCCESS: Visual output chart cleanly saved as:\n -> {output_filename}")
    print("====================================================")
