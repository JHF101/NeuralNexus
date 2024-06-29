import cv2
import os

drawing=False
# default class label is the first one
class_label = 0
# list of class labels
classes = ["hardhat", "no-hardhat"]

color_map = {}
color_list = [(0, 0, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
for i in range(len(classes)):
    color_map[classes[i]] = color_list[i]

# Create the base annotation directory
base_folder = 'annotations/'
if not os.path.exists(base_folder):
    os.makedirs(base_folder)

# folder containing images to annotate
img_folder = "annotations/images/"
img_names = []
for file in os.listdir(img_folder):
    if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png'):
        img_names.append(file)

ann_folder = "annotations/labels/"
if not os.path.exists(ann_folder):
    os.makedirs(ann_folder)

def display_instructions(image):
    instructions = [
        "Instructions:",
        "LMB: Draw bounding box",
        "RMB: Change class label",
        "C: Clear all boxes",
        "S: Save and next image",
        "D: Delete last box",
        "Q: Quit"
    ]

    for i, text in enumerate(instructions):
        cv2.putText(image, text, (10, image.shape[0] - 10 - (i * 20)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

for img_name in img_names:
    img_path = img_folder + img_name
    ann_path = ann_folder + img_name.split('.')[0] + '.txt'

    img = cv2.imread(img_path)
    og_img = img.copy()
    img_copy = img.copy()

    bbox_list = []

    # If the label file exists, read the bounding boxes
    if os.path.exists(ann_path):
        with open(ann_path, "r") as f:
            for line in f:
                parts = line.strip().split()

                # Read class label
                class_label = int(parts[0])

                # Read normalized coordinates
                normalized_x_min = float(parts[1])
                normalized_y_min = float(parts[2])
                normalized_width = float(parts[3])
                normalized_height = float(parts[4])

                # Reverse normalization
                img_width = img.shape[1]
                img_height = img.shape[0]

                x_center = normalized_x_min * img_width
                y_center = normalized_y_min * img_height
                width = normalized_width * img_width
                height = normalized_height * img_height

                x1 = int(x_center - width / 2.0)
                y1 = int(y_center - height / 2.0)
                x2 = int(x_center + width / 2.0)
                y2 = int(y_center + height / 2.0)

                bbox_list.append((int(class_label), (x1, y1, x2, y2)))

    def draw_bounding_box(event, x, y, flags, param):
        global ix, iy, drawing, bbox, img_copy, class_label
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            class_key = classes[class_label]
            class_text = f"Class: {class_key}"
            if drawing == True:
                img_copy = img.copy()
                cv2.rectangle(img_copy, (ix, iy), (x, y), color_map[class_key], 2)
                cv2.putText(img_copy, class_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_map[class_key], 2)
                cv2.imshow("image", img_copy)

        elif event == cv2.EVENT_RBUTTONUP:
            class_label = (class_label + 1) % len(classes)
            class_key = classes[class_label]
            print(f"Selected class: {class_key} ({class_label})")
            cv2.putText(img_copy, class_key, (x+5, y+5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[class_key], 2)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            class_key = classes[class_label]
            cv2.rectangle(img, (ix, iy), (x, y), color_map[class_key], 2)
            bbox = [ix, iy, x, y]
            bbox_list.append((class_label, bbox))

            cv2.putText(img, class_key, (x + 5, y + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[class_key], 2)
            cv2.imshow("image", img)

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", draw_bounding_box)


    while True:
        # Display the image
        for bbox in bbox_list:
            class_key = classes[bbox[0]]
            cv2.rectangle(img_copy, (bbox[1][0], bbox[1][1]), (bbox[1][2], bbox[1][3]), color_map[class_key], 2)
            cv2.putText(img_copy, class_key, (bbox[1][0] + 5, bbox[1][1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[class_key], 2)
        display_instructions(img_copy)
        cv2.imshow("image", img_copy)

        key = cv2.waitKey(1) & 0xFF

        # clear all bounding boxes
        if key == ord("c"):
            img = img_copy.copy()
            bbox_list = []
            print("Clicked C")
            # Wipe the file containing the bounding boxes
            with open(f"{ann_path}", "w") as f:
                pass
            img = og_img.copy()
            cv2.imshow("image", img)

        # save bounding boxes and move to next image
        elif key == ord("s"):
            with open(f"{ann_path}", "w") as f:
                for bbox in bbox_list:
                    class_label = bbox[0]
                    x1, y1, x2, y2 = bbox[1]

                    x_min = min(x1, x2)
                    y_min = min(y1, y2)
                    x_max = max(x1, x2)
                    y_max = max(y1, y2)

                    width = x_max - x_min
                    height = y_max - y_min

                    # Normalize the coordinates
                    img_width = img.shape[1]
                    img_height = img.shape[0]

                    normalized_x_min = (x_min + width / 2.0) / img_width
                    normalized_y_min = (y_min + height / 2.0) / img_height
                    normalized_width = width / img_width
                    normalized_height = height / img_height

                    f.write(f"{class_label} {normalized_x_min:.6f} {normalized_y_min:.6f} {normalized_width:.6f} {normalized_height:.6f}\n")
            break

        # delete last bounding box
        elif key == ord("d"):
            print("Deleting")
            if len(bbox_list) > 0:
                bbox_list.pop()
                img_copy = og_img.copy()
                cv2.imshow("image", img_copy)
                for bbox in bbox_list:
                    class_key = classes[bbox[0]]
                    cv2.rectangle(img_copy, (bbox[1][0], bbox[1][1]), (bbox[1][2], bbox[1][3]), color_map[class_key], 2)
                    cv2.putText(img_copy, class_key, (bbox[1][0] + 5, bbox[1][1] + 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color_map[class_key], 2)
                img_copy = og_img.copy()
                cv2.imshow("image", img_copy)

        elif key == ord("q"):  # quit annotation
            cv2.destroyAllWindows()
            exit()

