import cv2
import numpy as np
from ultralytics import YOLO
from collections import deque

# ======================
# 配置与开关
# ======================
model_path = "/mnt/e/whyu/whyu_sz/yolov8/runs/detect/salmo_speed/weights/best.pt"
video_path = "/mnt/e/whyu/zxh_salmo/Speed/1.mp4"
output_path = "/mnt/e/whyu/zxh_salmo/Speed/1_tracking.mp4"
tracker_cfg = "/mnt/e/whyu/whyu_sz/yolov8/ultralytics-main/ultralytics/cfg/trackers/bytetrack.yaml"

# 功能开关
SHOW_TRAJECTORY = True    # 是否显示游动轨迹
SHOW_ARROW = True         # 是否显示方向箭头
TRAJECTORY_LEN = 30       # 轨迹保存的帧数
ARROW_FIXED_LENGTH = 40   # 箭头的固定像素长度

# ======================
# 加载模型
# ======================
model = YOLO(model_path)

# ======================
# 视频信息
# ======================
cap = cv2.VideoCapture(video_path)
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
cap.release()

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = cv2.VideoWriter(output_path, fourcc, fps, (w, h))

# ======================
# 状态记录
# ======================
prev_state = {} 
# 轨迹字典: {track_id: deque([(x, y), (x, y), ...], maxlen=TRAJECTORY_LEN)}
trajectories = {}

# ======================
# 运行 tracking
# ======================
results = model.track(
    source=video_path,
    stream=True,
    persist=True,
    tracker=tracker_cfg,
    verbose=False
)

frame_idx = 0

for r in results:
    frame = r.orig_img.copy()

    if r.boxes is None or r.boxes.id is None:
        writer.write(frame)
        frame_idx += 1
        continue

    boxes = r.boxes.xyxy.cpu().numpy()
    ids = r.boxes.id.cpu().numpy().astype(int)

    for box, track_id in zip(boxes, ids):
        x1, y1, x2, y2 = map(int, box)
        cx, cy = int((x1 + x2) / 2), int((y1 + y2) / 2)
        body_len = max(x2 - x1, y2 - y1)

        # 更新轨迹数据
        if track_id not in trajectories:
            trajectories[track_id] = deque(maxlen=TRAJECTORY_LEN)
        trajectories[track_id].append((cx, cy))

        speed_bl = 0.0
        
        # 计算速度与方向
        if track_id in prev_state:
            px, py = prev_state[track_id]["center"]
            dx = cx - px
            dy = cy - py
            dist = np.sqrt(dx**2 + dy**2)

            if body_len > 1:
                speed_bl = (dist / body_len) * fps
            speed_bl = max(speed_bl, 1.0) # 水流补偿

            # 1. 绘制方向箭头 (可选)
            if SHOW_ARROW and dist > 1: # 只有发生移动时才画
                # 归一化方向向量并乘以固定长度
                unit_dx = dx / dist
                unit_dy = dy / dist
                ex = int(cx + unit_dx * ARROW_FIXED_LENGTH)
                ey = int(cy + unit_dy * ARROW_FIXED_LENGTH)
                
                cv2.arrowedLine(frame, (cx, cy), (ex, ey), (0, 0, 255), 2, tipLength=0.3)

        # 2. 绘制游动轨迹 (可选)
        if SHOW_TRAJECTORY and len(trajectories[track_id]) > 1:
            pts = list(trajectories[track_id])
            for i in range(1, len(pts)):
                # 越近的轨迹点颜色越深/越粗 (可选优化)
                cv2.line(frame, pts[i-1], pts[i], (255, 0, 0), 2)

        # 更新当前状态供下一帧使用
        prev_state[track_id] = {"center": (cx, cy)}

        # 绘制检测框和 ID 速度
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"ID {track_id} | {speed_bl:.2f} BL/s"
        cv2.putText(frame, label, (x1, y1 - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    writer.write(frame)
    frame_idx += 1

writer.release()
print("Tracking video saved to:", output_path)