from flask import Flask, request, jsonify
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image, ImageDraw
import io
import base64
from flask_cors import CORS 

app = Flask(__name__)
CORS(app)

# Load pre-trained Faster R-CNN model
# Load pre-trained Faster R-CNN model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
model.load_state_dict(torch.hub.load_state_dict_from_url(
    "https://download.pytorch.org/models/fasterrcnn_resnet50_fpn_coco-258fb6c6.pth",
    progress=True
))
model.eval()

# Define the classes for COCO dataset
COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

def detect_objects(image):
    img = Image.open(image)
    img_tensor = transforms.ToTensor()(img)
    img_tensor = img_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(img_tensor)

    object_counts = {}
    for box, label, score in zip(output[0]['boxes'], output[0]['labels'], output[0]['scores']):
        if score > 0.5:
            class_name = COCO_INSTANCE_CATEGORY_NAMES[label.item()]
            if class_name in object_counts:
                object_counts[class_name] += 1
            else:
                object_counts[class_name] = 1

            draw = ImageDraw.Draw(img)
            draw.rectangle([(box[0], box[1]), (box[2], box[3])], outline="red", width=3)
            draw.text((box[0], box[1]), class_name, fill="red")

    # Convert image to base64-encoded string
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    img_base64_str = base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

    return img_base64_str, object_counts

@app.route('/detect', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    image_data, object_counts = detect_objects(file)

    return jsonify({'image': image_data, 'object_counts': object_counts})

if __name__ == '__main__':
    app.run(debug=True)