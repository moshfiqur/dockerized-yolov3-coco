## Object detection using YOLO v3 in Docker
A dockerized implementation of YOLO v3 object detection running on gunicorn. The prediction code was directly inspired/modified by [qqwweee/keras-yolo3][1].

[1]: https://github.com/qqwweee/keras-yolo3



### Build command
```
$ docker build -t yolov3-coco .
```

### Run command

Run with interactive shell access to container
```
$ docker run -it \
    -v /srv/downloads/ml-datasets/pretrained-models/yolov3-coco:/usr/src/app/yolov3-coco:ro \
    yolov3-coco bash
```

Run to test the app in action. We needed to increase the memory limit using `-m 2g` for the object detection model to work.
```
$ docker run \
    -v /srv/downloads/ml-datasets/pretrained-models/yolov3-coco:/usr/src/app/yolov3-coco:ro \
    -p 10080:10080 \
    -m 4g yolov3-coco
```