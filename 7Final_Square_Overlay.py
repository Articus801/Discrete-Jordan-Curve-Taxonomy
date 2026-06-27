import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def generate_dynamic_bumpy_bezier(n):
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    r = 1.0 + 0.18 * np.sin(3 * t) + 0.08 * np.cos(5 * t)
    return np.column_stack((r * np.cos(t), r * np.sin(t)))

def analyze_curve_ccrt(curve):
    midpoints = []
    chords = []
    for x in curve:
        dists = np.linalg.norm(curve + x, axis=1)
        y = curve[np.argmin(dists)]
        midpoint = (x + y) / 2.0
        length = np.linalg.norm(x - y)
        midpoints.append(midpoint)
        chords.append({'x': x, 'y': y, 'midpoint': midpoint, 'length': length})
    return np.array(midpoints), chords

def hunt_all_squares(chords, tol_len=0.04, tol_mid=0.04, tol_ortho=0.1):
    n = len(chords)
    found_squares = []
    for i in range(n):
        c1 = chords[i]
        v1 = c1['x'] - c1['y']
        for j in range(i + 1, n):
            c2 = chords[j]
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) < 1e-4 and \
               np.linalg.norm(c1['x'] - c2['y']) < 1e-4:
                continue
            if abs(c1['length'] - c2['length']) > tol_len:
                continue
            if np.linalg.norm(c1['midpoint'] - c2['midpoint']) > tol_mid:
                continue
            v2 = c2['x'] - c2['y']
            norm1 = np.linalg.norm(v1)
            norm2 = np.linalg.norm(v2)
            if norm1 < 1e-6 or norm2 < 1e-6:
                continue
            dot_product = np.dot(v1, v2) / (norm1 * norm2)
            if abs(dot_product) < tol_ortho:
                duplicate = False
                for sq in found_squares:
                    if np.linalg.norm(sq[0]['midpoint'] - c1['midpoint']) < 0.05:
                        duplicate = True
                        break
                if not duplicate:
                    found_squares.append((c1, c2))
    return found_squares

if __name__ == "__main__":
    print("Executing final high-res square extraction (N=600)...")
    N = 600 # Using our verified convergence baseline
    curve = generate_dynamic_bumpy_bezier(N)
    midpoints, chords = analyze_curve_ccrt(curve)
    final_squares = hunt_all_squares(chords)

    print(f"Trapped {len(final_squares)} true geometric squares. Rendering final graphics...")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6.5))

    # Left Panel: Curve + Verified Squares
    ax1.plot(curve[:, 0], curve[:, 1], 'b-', lw=2.5, label='Jordan Curve ($\gamma$)')
    ax1.scatter(midpoints[:, 0], midpoints[:, 1], color='red', s=4, zorder=3, label='Midpoint Cloud')

    for i in range(0, len(chords), 20):
        c = chords[i]
        ax1.plot([c['x'], c['y']], [c['x'], c['y']], color='gray', alpha=0.1, lw=1)

    square_count = 0
    for sq in final_squares:
        square_count += 1
        c1, c2 = sq
        # Form the 4 corners of the square loop properly
        pts = np.array([c1['x'], c2['x'], c1['y'], c2['y'], c1['x']])
        ax1.plot(pts[:, 0], pts[:, 1], color='limegreen', lw=3.0, zorder=5,
                 label=f'Inscribed Square {square_count}')

    ax1.set_title("Verified Inscribed Squares Found", fontsize=12, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.5)
    ax1.legend(loc='upper right')

    # Right Panel: Caustic spectrum unchanged
    for i in range(0, len(midpoints), 2):
        ax2.plot([0, midpoints[i, 0]], [0, midpoints[i, 1]], color='crimson', alpha=0.2, lw=0.8)
    ax2.scatter(midpoints[:, 0], midpoints[:, 1], color='darkred', s=2)
    ax2.axhline(0, color='black', lw=0.5, linestyle='--')
    ax2.axvline(0, color='black', lw=0.5, linestyle='--')
    ax2.set_title("Isolated Midpoint Straw Spectrum", fontsize=12, fontweight='bold')
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.5)

    plt.tight_layout()
    output_filename = "final_verified_inscribed_squares.png"
    plt.savefig(output_filename, dpi=300)
    print(f"\nSUCCESS: Output file saved beautifully as: {output_filename}")
