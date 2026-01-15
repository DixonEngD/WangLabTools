import cv2
import os
import argparse

def extract_frames(video_path, step, out_dir):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    os.makedirs(out_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Failed to open video.")

    frame_idx = 0
    save_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % step == 0:
            out_path = os.path.join(out_dir, f"{save_idx:06d}.png")
            cv2.imwrite(out_path, frame)
            save_idx += 1

        frame_idx += 1

    cap.release()
    print(f"Done. Extracted {save_idx} frames to '{out_dir}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Video frame extraction")
    parser.add_argument("--video", type=str, required=True, help="Input video file")
    parser.add_argument("--step", type=int, default=10, help="Extract one frame every N frames")
    parser.add_argument("--out_dir", type=str, default="frames", help="Output directory")

    args = parser.parse_args()

    extract_frames(
        video_path=args.video,
        step=args.step,
        out_dir=args.out_dir
    )
