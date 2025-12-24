# YOLO Models Directory

This directory contains YOLO model checkpoint files.

## Files (not included in repository)

- `yolov11n.pt` (~6MB) - YOLOv11 nano model

## Download

### Option 1: Use download script

```bash
./download_models.sh
```

### Option 2: Automatic download

The model will be automatically downloaded by Ultralytics on first use.

### Option 3: Manual download

Models are cached in `~/.cache/ultralytics/` after first download.
You can copy them here:

```bash
cp ~/.cache/ultralytics/yolov11n.pt ./
```

**Note**: Model files are excluded from git via `.gitignore`.
