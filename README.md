# wolf_detection

Use machine learning to detect wolf in Werewolf game

## Steps


### Download Video
* youtube-dl
```sh
youtube-dl -f mp4 <URL>
youtube-dl -f mp4 https://www.youtube.com/watch?v=HRpDjcmNHqE -o add_videos/0311.mp4
```

### Cut up Video
* ffmpeg
```sh
ffmpeg -i add_videos/0311.mp4 -ss 00:01:32 -to 00:31:05 -c copy ./add_videos/0311cut.mp4
```

### Convert Video to Images
* ffmpeg
  * make directory to store images
  * eight images in one second
```sh
mkdir add_videos/0311_images
```
```sh
ffmpeg -i input.mp4 -r 1 out%5d.png
ffmpeg -i add_videos/0311cut.mp4 -r 8 add_videos/0311_images/0311%5d.png
```

### Detect Faces
* YOLO
  * looking for images of only one person
  * save in ./results/
```sh
./darknet detect cfg/yolov3.cfg yolov3.weights add_videos/0311_images/
```

### Copy Images to Another Server
```sh
scp -r results tiffany@merry.ee.ncku.edu.tw:~/git/wolf_detection/
```

### Detect 09chen
* facenet
  * execute in facenet directory
  * save in ./09face/
  * delete not 09 by filezilla
```sh
python identify.py
```

### Crop Images Top
```sh
python cropimg.py
```

### Divide all Images into Train Test Validation
```sh
python divide.py
```
