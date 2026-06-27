import os
import matplotlib
# Use a completely safe non-interactive backend
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

if __name__ == "__main__":
    print("====================================================")
    print("   MATPLOTLIB DIRECT FLUID ANIMATION COMPILER        ")
    print("====================================================\n")

    frame_dir = "deformation_frames"
    output_gif = "jordan_curve_morph_tour.gif"

    # Track paths numerically to ensure perfect chronologic sequences
    frames_paths = [os.path.join(frame_dir, f"frame_{i}.png") for i in range(1, 6)]

    # Build smooth back-and-forth ping-pong looping sequence
    # frame 1 -> 2 -> 3 -> 4 -> 5 -> 4 -> 3 -> 2
    looping_paths = frames_paths + frames_paths[-2:0:-1]

    # Verify files are physically present in the directory
    missing_files = [f for f in frames_paths if not os.path.exists(f)]
    if missing_files:
        print(f"Error: Missing expected frame files: {missing_files}")
        print("Please run 'python3 9Deformation_Tour.py' first.")
    else:
        print("Initializing Direct Stream Media Canvas...")
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.axis('off') # Remove axis ticks from compiling background

        # Read and stack images into active volatile runtime buffers
        ims = []
        for path in looping_paths:
            img = plt.imread(path)
            # Render each image slice cleanly over our master canvas
            im = ax.imshow(img, animated=True)
            ims.append([im])

        print("Stitching array frames into system container matrix...")
        # interval=800 defines the delay between frames in milliseconds
        ani = animation.ArtistAnimation(fig, ims, interval=800, blit=True)

        print(f"Executing direct-to-disk write operation: {output_gif}")
        # Forced pillow writer handles flushing tasks automatically
        ani.save(output_gif, writer='pillow')
        plt.close()

        # Immediate verification scan
        if os.path.exists(output_gif) and os.path.getsize(output_gif) > 0:
            file_size_kb = os.path.getsize(output_gif) / 1024.0
            print("\n====================================================")
            print(f"SUCCESS: Animation loop populated and saved!")
            print(f" -> File Location: ./{output_gif}")
            print(f" -> Verified Disk Footprint: {file_size_kb:.2f} KiB")
            print("====================================================")
        else:
            print("\nError: System reports file stream remained unpopulated.")
