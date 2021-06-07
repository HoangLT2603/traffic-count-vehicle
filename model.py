import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import cv2
import argparse
import time
from object_detection.utils import label_map_util
from PIL import Image
import numpy as np
import math

tf.get_logger().setLevel('ERROR')

parser = argparse.ArgumentParser()
parser.add_argument('--model', help='Folder that the Saved Model is Located In',
                    default='exported-models/my_model')
parser.add_argument('--labels', help='Where the Labelmap is Located',
                    default='annotations/label_map.pbtxt')
parser.add_argument('--threshold', help='Minimum confidence threshold for displaying detected objects',
                    default=0.4)

args = parser.parse_args()
# Enable GPU dynamic memory allocation
gpus = tf.config.experimental.list_physical_devices('GPU')
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

PATH_TO_MODEL_DIR = args.model
PATH_TO_LABELS = args.labels
PATH_TO_SAVED_MODEL = PATH_TO_MODEL_DIR + "/saved_model"
MIN_CONF_THRESH = float(args.threshold)


imH = 500
imW = 700
max_distance = 50


def load_model():
    print('Loading model...')
    start_time = time.time()
    detect_fn = tf.saved_model.load(PATH_TO_SAVED_MODEL)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Done! Took {} seconds'.format(elapsed_time))
    return detect_fn

category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS,use_display_name=True)


#chuyển image sang dạng mảng
def load_image_into_numpy_array(path):
    return np.array(Image.open(path))

#lấy box,class của các đối tượng
def get_object(frame,detect_fn):
    #convert image sang hệ màu BGR
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    frame_expanded = np.expand_dims(frame_rgb, axis=0)


    # convert frame sang dạng tensor.
    input_tensor = tf.convert_to_tensor(frame)
    # The model expects a batch of images, so add an axis with `tf.newaxis`.
    input_tensor = input_tensor[tf.newaxis, ...]

    # detect
    detections = detect_fn(input_tensor)

    # All outputs are batches tensors.
    # Convert to numpy arrays, and take index [0] to remove the batch dimension.
    # We're only interested in the first num_detections.
    num_detections = int(detections.pop('num_detections'))
    detections = {key: value[0, :num_detections].numpy()
                  for key, value in detections.items()}
    detections['num_detections'] = num_detections

    # detection_classes should be ints.
    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)

    # SET MIN SCORE THRESH TO MINIMUM THRESHOLD FOR DETECTIONS

    detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
    scores = detections['detection_scores']
    boxes = detections['detection_boxes']
    classes = detections['detection_classes']
    box = []
    class_ = []
    for i in range(len(scores)):
        if ((scores[i] > MIN_CONF_THRESH) and (scores[i] <= 1.0)):
            ymin = int(max(1, (boxes[i][0] * imH)))
            xmin = int(max(1, (boxes[i][1] * imW)))
            ymax = int(min(imH, (boxes[i][2] * imH)))
            xmax = int(min(imW, (boxes[i][3] * imW)))
            boxx=[xmin,ymin,xmax-xmin, ymax-ymin]
            box.append(boxx)
            class_name = category_index[int(classes[i])]['name']
            class_.append(class_name)
    return box, class_

#kiểm tra đối tượng cũ hay mới
def is_old(center_Xd, center_Yd, boxes):
    for box_tracker in boxes:
        (xt, yt, wt, ht) = [int(c) for c in box_tracker]
        center_Xt, center_Yt = int((xt + (xt + wt)) / 2.0), int((yt + (yt + ht)) / 2.0)
        distance = math.sqrt((center_Xt - center_Xd) ** 2 + (center_Yt - center_Yd) ** 2)

        if distance < max_distance:
            return True
    return False


#tính toán lại tạo độ của box
def get_box_info(box):
    (x, y, w, h) = [int(v) for v in box]
    center_X = int((x + (x + w)) / 2.0)
    center_Y = int((y + (y + h)) / 2.0)
    return x, y, w, h, center_X, center_Y



