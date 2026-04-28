import os
import numpy as np
import matplotlib.pyplot as plt

# ========== CẤU HÌNH ==========
width      = 720
height     = 1280
seg_frames = 30
segments   = 59

seg_dir = r"D:\ShortVideoStreaming\segments_yuv"

cases = {
    "SVC L0":       "svc_L0",
    "SVC L0+L1":    "svc_L1",
    "SVC L0+L1+L2": "svc_L2",
    "1 Layer QP=32":"onlyL0",
    "1 Layer QP=30":"onlyL1",
    "1 Layer QP=26":"onlyL2",
}
# ==============================

frame_size = width * height * 3 // 2
y_size     = width * height

def tinh_psnr(file_dec, file_orig):
    with open(file_dec,  "rb") as f: data_dec  = f.read()
    with open(file_orig, "rb") as f: data_orig = f.read()

    mse_total = 0
    for i in range(seg_frames):
        offset = i * frame_size
        y_dec  = np.frombuffer(data_dec [offset:offset+y_size], dtype=np.uint8).astype(np.float64)
        y_orig = np.frombuffer(data_orig[offset:offset+y_size], dtype=np.uint8).astype(np.float64)
        mse_total += np.mean((y_dec - y_orig) ** 2)

    mse_avg = mse_total / seg_frames
    if mse_avg == 0:
        return 100.0
    return 10 * np.log10(255**2 / mse_avg)

# Tính PSNR
psnr_all = {key: [] for key in cases}

for label, folder in cases.items():
    print(f"Đang tính PSNR: {label}...")
    for seg in range(segments):
        file_dec  = os.path.join(seg_dir, folder,  f"seg{seg}.yuv")
        file_orig = os.path.join(seg_dir, "orig",  f"seg{seg}.yuv")
        val = tinh_psnr(file_dec, file_orig)
        psnr_all[label].append(val)
        print(f"  seg{seg}: {val:.4f} dB")

# In bảng
print(f"\n{'Seg':<6}", end="")
for key in cases: print(f"{key:<16}", end="")
print("\n" + "-" * 100)
for seg in range(segments):
    print(f"{seg:<6}", end="")
    for key in cases: print(f"{psnr_all[key][seg]:<16.4f}", end="")
    print()
print("-" * 100)
print(f"{'TB':<6}", end="")
for key in cases:
    print(f"{sum(psnr_all[key])/segments:<16.4f}", end="")
print()

# Vẽ biểu đồ
colors  = ['blue', 'orange', 'green', 'cyan', 'red', 'purple']
markers = ['o', 's', '^', 'v', 'D', 'x']

plt.figure(figsize=(16, 7))
for i, key in enumerate(cases):
    plt.plot(range(segments), psnr_all[key], label=key,
             marker=markers[i], markersize=3, color=colors[i])

plt.xlabel("Segment")
plt.ylabel("PSNR (dB)")
plt.title("So sánh PSNR theo từng Segment")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("psnr_chart.png")
plt.show()
print("Đã lưu: psnr_chart.png")