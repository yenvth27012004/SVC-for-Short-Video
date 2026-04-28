import os
import subprocess

# ========== CẤU HÌNH ==========
ffmpeg     = "ffmpeg"
width      = 720
height     = 1280
fps        = 30
seg_frames = 30
segments   = 59

yuv_files = {
    "svc_L0":    r"D:\ShortVideoStreaming\svc_L0.yuv",
    "svc_L1":    r"D:\ShortVideoStreaming\svc_L1.yuv",
    "svc_L2":    r"D:\ShortVideoStreaming\svc_L2.yuv",
    "onlyL0":    r"D:\ShortVideoStreaming\onlyL0.yuv",
    "onlyL1":    r"D:\ShortVideoStreaming\onlyL1.yuv",
    "onlyL2":    r"D:\ShortVideoStreaming\onlyL2.yuv",
    "orig":      r"D:\ShortVideoStreaming\v1.yuv",
}

seg_dir = r"D:\ShortVideoStreaming\segments_yuv"
os.makedirs(seg_dir, exist_ok=True)
# ==============================

for name, yuv_path in yuv_files.items():
    out_dir = os.path.join(seg_dir, name)
    os.makedirs(out_dir, exist_ok=True)

    for seg in range(segments):
        start_frame = seg * seg_frames
        out_file = os.path.join(out_dir, f"seg{seg}.yuv")

        cmd = [
            ffmpeg, "-y",
            "-f", "rawvideo",
            "-pix_fmt", "yuv420p",
            "-s", f"{width}x{height}",
            "-r", str(fps),
            "-i", yuv_path,
            "-vf", f"trim=start_frame={start_frame}:end_frame={start_frame + seg_frames},setpts=PTS-STARTPTS",
            "-f", "rawvideo",
            "-pix_fmt", "yuv420p",
            out_file
        ]
        subprocess.run(cmd, capture_output=True)
        print(f"{name} seg{seg} done")

print("Chia segment xong!")