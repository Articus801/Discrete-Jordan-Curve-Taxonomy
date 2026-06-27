import numpy as np
import matplotlib.pyplot as plt

def load_data():
    """Safely ingests the boundary matrices from disk."""
    try:
        sharp = np.load('17_sharp_curve.npy')
        rounded = np.load('17_rounded_curve.npy')
        return sharp, rounded
    except FileNotFoundError:
        print("Error: Missing 17_sharp_curve.npy or 17_rounded_curve.npy.")
        print("Please run 17_hybrid_generator.py first to establish the boundaries.")
        exit(1)

if __name__ == "__main__":
    print("[20_taxonomy_visualizer] Initiating visual asset rendering engine...")

    # 1. Load coordinates
    sharp_curve, rounded_curve = load_data()
    origin = np.array([0.5, 0.5])

    # 2. Setup the unified three-panel diagnostic canvas
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=150)
    plt.subplots_adjust(wspace=0.3)

    # -------------------------------------------------------------------------
    # PANEL 1: THE GEOMETRIC DISSECTION (Overlaid boundary manifolds)
    # -------------------------------------------------------------------------
    ax1 = axes[0]
    ax1.plot(sharp_curve[:, 0], sharp_curve[:, 1], color='#e41a1c', lw=1.5, label='Pure Sharp (Fractal)')
    ax1.plot(rounded_curve[:, 0], rounded_curve[:, 1], color='#377eb8', lw=1.5, ls='--', label='Rounded Variant')
    ax1.scatter(origin[0], origin[1], color='black', zorder=5, label='Origin (0.5, 0.5)')

    ax1.set_title("Panel 1: Boundary Geometry Overlap", fontsize=11, fontweight='bold')
    ax1.set_xlim(-0.1, 1.1)
    ax1.set_ylim(-0.1, 1.4)
    ax1.set_aspect('equal')
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower center', fontsize=9)

    # -------------------------------------------------------------------------
    # PANEL 2: THE STRAW FIELD INTERROGATION (Visualising the Attractor)
    # -------------------------------------------------------------------------
    ax2 = axes[1]
    # Re-draw boundaries as context background strings
    ax2.plot(sharp_curve[:, 0], sharp_curve[:, 1], color='#e41a1c', alpha=0.3, lw=1)

    # Cast a subset of 180 straws visually so the plot remains clean and scannable
    visual_angles = np.linspace(-np.pi, np.pi, 180, endpoint=False)
    centered_sharp = sharp_curve - origin
    sharp_angles = np.arctan2(centered_sharp[:, 1], centered_sharp[:, 0])

    for alpha in visual_angles:
        # Resolve discrete coordinate hits identical to script 18
        diff = np.abs(sharp_angles - alpha)
        diff = np.minimum(diff, 2 * np.pi - diff)
        idx = np.argmin(diff)
        hit_point = sharp_curve[idx]

        # Color-code straws based on zone targeting to visually highlight the "Cusp"
        # Straws pointing upward (y > 0.9) hit the fractal patch zone
        if hit_point[1] > 0.95:
            ax2.plot([origin[0], hit_point[0]], [origin[1], hit_point[1]], color='#ff7f00', alpha=0.4, lw=0.8)
        else:
            ax2.plot([origin[0], hit_point[0]], [origin[1], hit_point[1]], color='grey', alpha=0.15, lw=0.5)

    ax2.scatter(origin[0], origin[1], color='black', zorder=5)
    ax2.set_title("Panel 2: Radial Straw Field & Attractor", fontsize=11, fontweight='bold')
    ax2.set_xlim(-0.1, 1.1)
    ax2.set_ylim(-0.1, 1.4)
    ax2.set_aspect('equal')
    ax2.grid(True, linestyle=':', alpha=0.6)

    # -------------------------------------------------------------------------
    # PANEL 3: THE TAXONOMY SIGNATURE SPACE (Mapping Invariance)
    # -------------------------------------------------------------------------
    ax3 = axes[2]
    # Coordinates derived directly from the terminal outputs of Script 18/19
    # Placing them into a mapping space to illustrate the taxonomy grouping
    skew_sharp, kurt_sharp = -1.17142, 1.50125
    skew_round, kurt_round = -1.19848, 1.62878

    # Plot baseline reference domains for future researchers
    ax3.axvspan(-0.2, 0.2, ymin=0, ymax=0.3, color='green', alpha=0.05, label='Class-E Domain (Smooth/Circles)')

    # Plot our active experimental points
    ax3.scatter(skew_sharp, kurt_sharp, color='#e41a1c', marker='o', s=100, zorder=5, label='Pure Sharp (Class-H)')
    ax3.scatter(skew_round, kurt_round, color='#377eb8', marker='^', s=100, zorder=5, label='Rounded (Class-H)')

    # Draw a link vector highlighting the compact family clustering
    ax3.plot([skew_sharp, skew_round], [kurt_sharp, kurt_round], color='purple', linestyle=':', lw=1.5, label='Topological Link')

    ax3.set_title("Panel 3: Taxonomy Signature Space", fontsize=11, fontweight='bold')
    ax3.set_xlabel("Skewness Metric", fontsize=10)
    ax3.set_ylabel("Kurtosis Metric", fontsize=10)
    ax3.set_xlim(-1.5, 0.5)
    ax3.set_ylim(0.0, 2.5)
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend(loc='upper right', fontsize=9)

    # Annotate the taxonomic convergence area
    ax3.annotate('Converged Family Domain\n[J-Curve::Class-H::Alpha]',
                 xy=((skew_sharp+skew_round)/2, (kurt_sharp+kurt_round)/2),
                 xytext=(-1.4, 0.5),
                 arrowprops=dict(facecolor='black', arrowstyle='->', lw=0.8),
                 fontsize=9, bbox=dict(boxstyle='round,pad=0.3', fc='yellow', alpha=0.1))

    # 4. Save and manifest asset on disk
    output_filename = "20_taxonomy_diagnostic.png"
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    print(f" SUCCESS: Comprehensive taxonomy visual compiled.")
    print(f" Saved asset as '{output_filename}' in your working directory.")
