
import boto3
import json
from keras.models import load_model
from utils.utils import get_yolo_boxes

class YOLOv3Predictor():
    def __init__(self, config):
        s3 = boto3.client("s3")
        s3.download_file(config["bucket"], config["key"], config["model_name"])
        self.model = load_model(config["model_name"])

        with open(config["model_config"]) as json_file:
            data = json.load(json_file)
        for key in data:
            setattr(self, key, data[key])

    def predict(self, payload):
        boxes = get_yolo_boxes(self.model, [payload], self.net_h, self.net_w,
        self.anchors, self.obj_thresh, self.nms_thresh)[0]

        return boxes