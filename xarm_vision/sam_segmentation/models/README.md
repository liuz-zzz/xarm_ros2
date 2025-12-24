# SAM Models Directory

This directory contains SAM (Segment Anything Model) checkpoint files.

## Files (not included in repository)

- `sam_vit_b.pth` (358MB) - ViT-B model, fastest
- `sam_vit_l.pth` (1.2GB) - ViT-L model, balanced
- `sam_vit_h.pth` (2.4GB) - ViT-H model, most accurate

## Download

Run the download script from the package root:

```bash
./download_models.sh
```

Or download manually:

```bash
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O sam_vit_b.pth
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth -O sam_vit_l.pth
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth -O sam_vit_h.pth
```

**Note**: Model files are excluded from git via `.gitignore` due to their large size.
