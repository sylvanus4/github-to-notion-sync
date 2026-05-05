---
name: opencv-toolkit
description: >-
  Comprehensive OpenCV (cv2) Python toolkit for image and video processing operations.
  ALWAYS invoke when the user asks to "resize image with opencv", "detect edges", "find contours",
  "face detection", "feature matching", "template matching", "color space conversion",
  "histogram equalization", "image segmentation", "watershed", "grabcut", "perspective transform",
  "affine transform", "blur image", "sharpen image", "morphological operation", "erode", "dilate",
  "threshold image", "adaptive threshold", "canny edge", "sobel filter", "draw on image",
  "annotate image", "video capture", "frame extraction opencv", "ORB features", "SIFT features",
  "homography", "panorama stitch", "HAAR cascade", "DNN module", "YOLO opencv",
  "image blending", "alpha blend", "PSNR", "SSIM", "blur detection", "batch image processing",
  "connected components", "distance transform", "flood fill", "k-means segmentation",
  "opencv-toolkit", "cv2", "컴퓨터 비전", "이미지 처리", "엣지 검출", "윤곽선 검출",
  "얼굴 검출", "특징점 매칭", "색공간 변환", "히스토그램 평활화", "이미지 분할",
  "모폴로지 연산", "이미지 블렌딩", "비디오 캡처", "프레임 추출", "템플릿 매칭",
  "객체 검출", "이미지 필터", "이미지 리사이즈", "원근 변환", "이미지 주석",
  "워터셰드", "그랩컷", "CLAHE", "적응형 임계값", "배치 이미지".
  Do NOT use for simple image compression/format conversion without CV operations (use image-optimizer).
  Do NOT use for ImageMagick CLI operations (use imagemagick-toolkit).
  Do NOT use for ffmpeg video operations (use ffmpeg-toolkit).
  Do NOT use for AI image generation (use pika-text-to-video or muapi-image-studio).
  Do NOT use for web image optimization only (use image-optimizer).
metadata:
  author: "thaki"
  version: "1.0.0"
  category: "execution"
  platforms: [darwin, linux]
  tags: [opencv, cv2, image, video, computer-vision, detection, segmentation, transform, filter, feature, contour, histogram, threshold, morphology, dnn]
---

# opencv-toolkit

Comprehensive Python toolkit wrapping OpenCV 4.x (`cv2`) for image processing, computer vision, and video analysis. Exposes the full parameter surface through structured workflows covering 14 operation categories.

## Quick Reference

| I want to... | Category | Key Function |
|---|---|---|
| Read/write/convert format | 1: Image I/O | `cv2.imread`, `cv2.imwrite` |
| Resize, crop, rotate, flip | 2: Geometric Transforms | `cv2.resize`, `cv2.warpAffine` |
| Adjust brightness, histogram | 3: Color & Histogram | `cv2.equalizeHist`, `CLAHE` |
| Blur, sharpen, morphology | 4: Filtering | `cv2.GaussianBlur`, `cv2.morphologyEx` |
| Detect edges, threshold | 5: Edge & Threshold | `cv2.Canny`, `cv2.threshold` |
| Find/draw contours, shapes | 6: Contours | `cv2.findContours`, `cv2.drawContours` |
| Match features, stitch | 7: Feature Detection | `cv2.ORB_create`, `cv2.BFMatcher` |
| Detect faces, objects | 8: Object Detection | `cv2.CascadeClassifier`, `cv2.dnn` |
| Draw lines, text, overlays | 9: Drawing | `cv2.putText`, `cv2.rectangle` |
| Process video frames | 10: Video | `cv2.VideoCapture`, `cv2.VideoWriter` |
| Segment regions | 11: Segmentation | `cv2.watershed`, `cv2.grabCut` |
| Blend, composite images | 12: Arithmetic | `cv2.addWeighted`, `cv2.bitwise_and` |
| Measure quality metrics | 13: Quality Metrics | `cv2.PSNR`, Laplacian variance |
| Process many files at once | 14: Batch | `glob` + loop pattern |

## Constraints

- Every `cv2` call uses validated parameters; never pass raw user strings to file paths without existence check
- Always validate input files exist before processing (`os.path.isfile`)
- Never overwrite the original source file; output to `{stem}_{operation}.{ext}`
- For video processing, always release `VideoCapture` and `VideoWriter` objects in a `finally` block
- Quote file paths containing spaces when invoking via Shell
- Never commit output image/video files to git
- Cap complex pipelines at 10 operations per script; split into multiple scripts for more
- Prefer `python3 -c "..."` one-liners for simple operations; use temp scripts for multi-step

## Prerequisites

- Python >= 3.9
- `pip install opencv-python` (with GUI/highgui) or `pip install opencv-python-headless` (server, no GUI)
- Optional: `pip install opencv-contrib-python` for SIFT, extra modules
- Verify: `python3 -c "import cv2; print(cv2.__version__)"`
- macOS: `brew install python3 && pip3 install opencv-python`

## Workflow

### Step 0: Inspect Input

```python
import cv2, os
img = cv2.imread("input.jpg")
print(f"Shape: {img.shape}, Dtype: {img.dtype}, Size: {os.path.getsize('input.jpg')} bytes")
```

For video: `cap = cv2.VideoCapture("input.mp4"); print(cap.get(cv2.CAP_PROP_FRAME_COUNT), cap.get(cv2.CAP_PROP_FPS))`

### Step 1: Select Operation Category

Match user request to one of the 14 categories below.

### Step 2: Build Python Script

Construct the script from validated parameters using category-specific references.

### Step 3: Execute

Run via `python3 -c "..."` or `python3 /tmp/cv_op.py`. Background if >30s expected.

### Step 4: Verify Output

Check output file exists and probe properties:
```python
out = cv2.imread("output.jpg"); print(f"Output: {out.shape}")
```

## Operation Categories

### Category 1: Image I/O & Format Conversion

| Operation | Code |
|---|---|
| Read image | `img = cv2.imread("in.jpg")` (BGR) |
| Read grayscale | `img = cv2.imread("in.jpg", cv2.IMREAD_GRAYSCALE)` |
| Read with alpha | `img = cv2.imread("in.png", cv2.IMREAD_UNCHANGED)` |
| Write JPEG (quality) | `cv2.imwrite("out.jpg", img, [cv2.IMWRITE_JPEG_QUALITY, 90])` |
| Write PNG (compression) | `cv2.imwrite("out.png", img, [cv2.IMWRITE_PNG_COMPRESSION, 5])` |
| BGR to RGB | `rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)` |
| BGR to Gray | `gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)` |
| BGR to HSV | `hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)` |
| BGR to LAB | `lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)` |

### Category 2: Geometric Transforms

| Operation | Code |
|---|---|
| Resize to WxH | `cv2.resize(img, (W, H))` |
| Resize by factor | `cv2.resize(img, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)` |
| Crop ROI | `cropped = img[y:y+h, x:x+w]` |
| Rotate 90 CW | `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)` |
| Rotate arbitrary | `M = cv2.getRotationMatrix2D((cx,cy), angle, 1.0); cv2.warpAffine(img, M, (w,h))` |
| Flip horizontal | `cv2.flip(img, 1)` |
| Flip vertical | `cv2.flip(img, 0)` |
| Perspective transform | `M = cv2.getPerspectiveTransform(src_pts, dst_pts); cv2.warpPerspective(img, M, (w,h))` |

Interpolation flags: `INTER_NEAREST` (fast), `INTER_LINEAR` (default), `INTER_AREA` (shrink), `INTER_CUBIC` (enlarge), `INTER_LANCZOS4` (best quality).

### Category 3: Color & Histogram Operations

| Operation | Code |
|---|---|
| Histogram equalization | `cv2.equalizeHist(gray)` |
| CLAHE | `clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)); clahe.apply(gray)` |
| Split channels | `b, g, r = cv2.split(img)` |
| Merge channels | `cv2.merge([b, g, r])` |
| Brightness adjust | `cv2.convertScaleAbs(img, alpha=1.2, beta=30)` |
| Gamma correction | `lut = np.array([((i/255)**gamma)*255 for i in range(256)], np.uint8); cv2.LUT(img, lut)` |

`alpha` controls contrast (1.0=same), `beta` controls brightness offset.

### Category 4: Filtering & Blurring

| Filter | Code | Use Case |
|---|---|---|
| Gaussian blur | `cv2.GaussianBlur(img, (5,5), 0)` | General noise reduction |
| Median blur | `cv2.medianBlur(img, 5)` | Salt-and-pepper noise |
| Bilateral filter | `cv2.bilateralFilter(img, 9, 75, 75)` | Edge-preserving smooth |
| Box filter | `cv2.blur(img, (5,5))` | Simple average |
| Sharpen (custom) | `kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]); cv2.filter2D(img, -1, kernel)` | Sharpening |
| Erode | `cv2.erode(img, kernel, iterations=1)` | Shrink white regions |
| Dilate | `cv2.dilate(img, kernel, iterations=1)` | Expand white regions |
| Open | `cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)` | Remove small noise |
| Close | `cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)` | Fill small holes |
| Gradient | `cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kernel)` | Edge outline |
| Top Hat | `cv2.morphologyEx(img, cv2.MORPH_TOPHAT, kernel)` | Bright detail extraction |
| Black Hat | `cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, kernel)` | Dark detail extraction |

Kernel creation: `kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))` — shapes: `MORPH_RECT`, `MORPH_ELLIPSE`, `MORPH_CROSS`.

### Category 5: Edge Detection & Thresholding

| Method | Code |
|---|---|
| Canny | `cv2.Canny(gray, 50, 150)` |
| Sobel X | `cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)` |
| Sobel Y | `cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)` |
| Laplacian | `cv2.Laplacian(gray, cv2.CV_64F)` |
| Simple threshold | `_, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)` |
| Otsu threshold | `_, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)` |
| Adaptive (mean) | `cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)` |
| Adaptive (gaussian) | `cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)` |

Canny thresholds: low=50-100, high=150-300 typical. Ratio 1:2 or 1:3 recommended.

### Category 6: Contour & Shape Analysis

```python
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
    x, y, w, h = cv2.boundingRect(cnt)
    hull = cv2.convexHull(cnt)
    M = cv2.moments(cnt)
    cx, cy = int(M['m10']/M['m00']), int(M['m01']/M['m00']) if M['m00'] != 0 else (0, 0)
```

Retrieval modes: `RETR_EXTERNAL` (outer only), `RETR_LIST` (all flat), `RETR_TREE` (full hierarchy).

### Category 7: Feature Detection & Matching

| Detector | Code |
|---|---|
| ORB | `orb = cv2.ORB_create(nfeatures=500); kp, des = orb.detectAndCompute(gray, None)` |
| SIFT | `sift = cv2.SIFT_create(); kp, des = sift.detectAndCompute(gray, None)` |
| AKAZE | `akaze = cv2.AKAZE_create(); kp, des = akaze.detectAndCompute(gray, None)` |
| BF Match | `bf = cv2.BFMatcher(cv2.NORM_HAMMING); matches = bf.knnMatch(des1, des2, k=2)` |
| FLANN Match | `flann = cv2.FlannBasedMatcher(index_params, search_params); matches = flann.knnMatch(des1, des2, k=2)` |
| Homography | `M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)` |

Lowe's ratio test: `good = [m for m, n in matches if m.distance < 0.75 * n.distance]`

SIFT requires `opencv-contrib-python`. ORB is free and fast.

### Category 8: Object Detection

| Method | Code |
|---|---|
| Haar face detect | `face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'); faces = face_cascade.detectMultiScale(gray, 1.3, 5)` |
| DNN from file | `net = cv2.dnn.readNet("model.weights", "model.cfg"); blob = cv2.dnn.blobFromImage(img, 1/255, (416,416), swapRB=True); net.setInput(blob); outs = net.forward(net.getUnconnectedOutLayersNames())` |
| Template match | `res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED); loc = np.where(res >= 0.8)` |

DNN supports: ONNX, Caffe, TensorFlow, Darknet (YOLO), TorchScript models.

**Full DNN inference pipeline (YOLO-style):**

```python
import cv2, numpy as np

net = cv2.dnn.readNet("yolov4-tiny.weights", "yolov4-tiny.cfg")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

img = cv2.imread("photo.jpg")
h, w = img.shape[:2]
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
net.setInput(blob)
outs = net.forward(net.getUnconnectedOutLayersNames())

boxes, confidences, class_ids = [], [], []
for out in outs:
    for det in out:
        scores = det[5:]
        cid = np.argmax(scores)
        conf = scores[cid]
        if conf > 0.5:
            cx, cy, bw, bh = (det[0:4] * [w, h, w, h]).astype(int)
            x, y = cx - bw // 2, cy - bh // 2
            boxes.append([x, y, bw, bh])
            confidences.append(float(conf))
            class_ids.append(cid)

idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
for i in idxs.flatten():
    x, y, bw, bh = boxes[i]
    cv2.rectangle(img, (x, y), (x + bw, y + bh), (0, 255, 0), 2)
```

For ONNX models: `net = cv2.dnn.readNetFromONNX("model.onnx")`. GPU acceleration: `net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA); net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)`.

### Category 9: Drawing & Annotation

| Shape | Code |
|---|---|
| Line | `cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)` |
| Rectangle | `cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)` |
| Circle | `cv2.circle(img, (cx,cy), radius, (0,0,255), -1)` |
| Ellipse | `cv2.ellipse(img, (cx,cy), (a,b), angle, 0, 360, (255,255,0), 2)` |
| Text | `cv2.putText(img, "Hello", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2)` |
| Arrow | `cv2.arrowedLine(img, (x1,y1), (x2,y2), (0,255,0), 2)` |
| Polylines | `cv2.polylines(img, [pts], True, (0,255,0), 2)` |
| Fill poly | `cv2.fillPoly(img, [pts], (0,255,0))` |

Color format is BGR `(B, G, R)`. Thickness `-1` fills the shape.

### Category 10: Video Processing

```python
cap = cv2.VideoCapture("input.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter("output.mp4", fourcc, fps, (w, h))
try:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # process frame here
        out.write(frame)
finally:
    cap.release()
    out.release()
```

| FourCC | Container | Notes |
|---|---|---|
| `mp4v` | .mp4 | Universal, moderate quality |
| `XVID` | .avi | Good compatibility |
| `avc1` | .mp4 | H.264 (macOS) |
| `MJPG` | .avi | Motion JPEG, large files |

Frame extraction: `cap.set(cv2.CAP_PROP_POS_FRAMES, N)` to seek to frame N.

**Optical flow (dense Farneback):**

```python
prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None,
    pyr_scale=0.5, levels=3, winsize=15, iterations=3, poly_n=5, poly_sigma=1.2, flags=0)
mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
hsv = np.zeros_like(prev_frame)
hsv[..., 0] = ang * 180 / np.pi / 2
hsv[..., 1] = 255
hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
flow_rgb = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
```

Sparse (Lucas-Kanade): `cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, prev_pts, None, **lk_params)` for tracking specific points.

### Category 11: Image Segmentation

| Method | Code |
|---|---|
| Watershed (full pipeline) | See watershed example below |
| GrabCut | `mask, bgd, fgd = np.zeros(...); cv2.grabCut(img, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)` |
| Flood fill | `cv2.floodFill(img, mask, (x,y), (255,255,255))` |
| Connected components | `n, labels, stats, centroids = cv2.connectedComponentsWithStats(binary)` |
| Distance transform | `cv2.distanceTransform(binary, cv2.DIST_L2, 5)` |
| K-means color seg | `criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0); _, labels, centers = cv2.kmeans(pixels, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)` |

**Watershed full pipeline example:**

```python
import cv2, numpy as np
img = cv2.imread("coins.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3,3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(opening, kernel, iterations=3)
dist = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist, 0.5 * dist.max(), 255, 0)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0
markers = cv2.watershed(img, markers)
img[markers == -1] = [0, 0, 255]
```

### Category 12: Image Arithmetic & Blending

| Operation | Code |
|---|---|
| Add (saturating) | `cv2.add(img1, img2)` |
| Subtract | `cv2.subtract(img1, img2)` |
| Alpha blend | `cv2.addWeighted(img1, 0.7, img2, 0.3, 0)` |
| Bitwise AND | `cv2.bitwise_and(img1, img2, mask=mask)` |
| Bitwise OR | `cv2.bitwise_or(img1, img2)` |
| Bitwise NOT | `cv2.bitwise_not(img)` |
| ROI paste | `img[y:y+h, x:x+w] = overlay` |

### Category 13: Image Quality & Metrics

| Metric | Code |
|---|---|
| PSNR | `cv2.PSNR(img1, img2)` |
| Blur detection | `cv2.Laplacian(gray, cv2.CV_64F).var()` (< 100 = blurry) |
| Mean/Std | `mean, std = cv2.meanStdDev(img)` |

### Category 14: Batch Processing

```python
import glob, cv2, os
for f in glob.glob("input_dir/*.jpg"):
    img = cv2.imread(f)
    result = cv2.resize(img, (800, 600))
    stem = os.path.splitext(os.path.basename(f))[0]
    cv2.imwrite(f"output_dir/{stem}_resized.jpg", result)
```

For parallel: use `concurrent.futures.ThreadPoolExecutor(max_workers=4)`.

## Error Handling

| Error | Symptom | Recovery |
|---|---|---|
| File not found | `img is None` after imread | Check path with `os.path.isfile()` |
| Import error | `ModuleNotFoundError: cv2` | `pip install opencv-python` |
| Codec missing | VideoWriter produces 0-byte file | Try different fourcc (`XVID`, `MJPG`) |
| Shape mismatch | `error: (-209:Sizes of input arguments do not match)` | Verify both images have same dimensions |
| Grayscale needed | `error: (-215:Assertion failed) src.type() == CV_8UC1` | Convert with `cvtColor(img, COLOR_BGR2GRAY)` |
| SIFT unavailable | `AttributeError: module 'cv2' has no attribute 'SIFT_create'` | `pip install opencv-contrib-python` |

## Gotchas

- OpenCV reads images in **BGR** order, not RGB. Use `cvtColor` before displaying with matplotlib or passing to other libraries.
- `cv2.imread` returns `None` on failure (no exception). Always check `if img is None`.
- `cv2.imwrite` infers format from the output file extension, not from the source.
- VideoWriter fourcc `mp4v` may fail on some systems; fall back to `XVID` + `.avi`. Always release resources: `cap.release(); out.release(); cv2.destroyAllWindows()`. Use a `try/finally` block for video pipelines to prevent leaked file handles and zombie processes.
- `cv2.resize` takes `(width, height)` but numpy shape is `(height, width, channels)`.
- Morphological kernels must be created with `getStructuringElement`, not bare numpy arrays, for consistent behavior.
- `findContours` modifies the input image in older OpenCV versions; pass a copy.
- SIFT/SURF are patented; use ORB or AKAZE for open-source projects.

## Anti-Example

> "Here's how to detect edges:
> `img = cv2.imread('photo.jpg'); edges = cv2.Canny(img, 50, 150)`"

This fails because: no existence check on input file, Canny typically expects grayscale input (passing BGR may produce noisy results), no output save, no parameter explanation. Every cv2 pipeline must validate input, convert color space appropriately, and verify output.

## See Also

- **imagemagick-toolkit** -- CLI-based image manipulation (no Python required)
- **image-optimizer** -- Web-optimized image compression and format conversion
- **ffmpeg-toolkit** -- Video/audio operations beyond frame-level processing
- **video-compress** -- Simple video compression presets
- **pika-text-to-video** -- AI video generation (not traditional CV)
