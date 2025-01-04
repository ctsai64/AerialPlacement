import cv2
import numpy as np

classes = []
with open('coco.names', 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')
net = cv2.dnn.readNetFromDarknet('yolov3-320.cfg', 'yolov3-320.weights')
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

def runDetection(outs, img):
    box = []
    ide = []
    conf = []
    mid = []
    for a in outs:
        for b in a:
            scores = b[5:]
            classid = np.argmax(scores)
            con = scores[classid]
            if con > 0.4:
                w = int(b[2] * 640)
                h = int(b[3] * 640)
                x = int(b[0] * 640 - w / 2)
                y = int(b[1] * 480 - h / 2)
                box.append([x, y, w, h])
                ide.append(classid)
                conf.append(float(con))
                mid.append([int(b[0]*640), int(b[1]*640)])
    keep = cv2.dnn.NMSBoxes(box, conf, 0.4, 0.3)
    results = []
    for k in keep:
        b = box[k]
        x = b[0]
        y = b[1]
        w = b[2]
        h = b[3]
        results.append([classes[ide[k]], [x, y], [w, h], mid[k]])
    return results

def getImage():
    cam = cv2.VideoCapture("/dev/video0")
    cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    success, img = cam.read()
    newImg = cv2.dnn.blobFromImage(img, 1 / 255, (320, 320), [0, 0, 0], 1, crop=False)
    net.setInput(newImg)
    outLayer = []
    for n in net.getUnconnectedOutLayers():
        outLayer.append(net.getLayerNames()[n - 1])
    outputs = net.forward(outLayer)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    return [outputs, newImg]

def returnResults():
    image = getImage()
    results = runDetection(image[0], image[1])
    if len(results) > 0:
        for t in results:
            if t[0] == "cup":
                return results[results.index(t)]
    return False
    
while True:
    ask = input("Run detection? (y/n) ")
    if ask == "y":
        print(returnResults())
    else:
        break
    
