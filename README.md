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

### Testing the prediction
A sample php script [uploader.php][1] is given which will send a POST request with an image to http://localhost:10080 where the docker service is running. 

[1]: https://github.com/moshfiqur/dockerized-yolov3-coco/blob/master/uploader.php

The output from the service will be a json encoded string looks like this:

```json
{
    "status": "success", 
    "detections": {
        "status": "success", 
        "time_taken": 3.6899283000000196, 
        "msg": "", 
        "detections": [
            {
                "label": "chair", 
                "score": 0.582422137260437, 
                "left": 74, 
                "top": 602, 
                "right": 421, 
                "bottom": 904
            }, {
                "label": "person", 
                "score": 0.9987449645996094, 
                "left": 98, 
                "top": 101, 
                "right": 1025, 
                "bottom": 935
            }
        ]
    }
}
```