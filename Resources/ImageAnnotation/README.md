# Image Annotation Tool

This Python script provides a simple image annotation tool using OpenCV. It allows you to annotate objects in images with bounding boxes and class labels. The script lets you draw bounding boxes around objects of interest, assign class labels, save annotations, and move between images for annotation.

## Table of Contents

- [Description](#description)
- [How to Use](#how-to-use)
- [Key Bindings](#key-bindings)
- [License](#license)

## Description

The script uses OpenCV to display images and allow interactive annotation. It loads images from a specified folder, reads existing annotations from corresponding annotation files, and allows you to add, modify, and delete bounding boxes for different classes.

The annotation process involves drawing bounding boxes around objects within the images and assigning class labels to these boxes. Annotations are saved in text files, one per image, following the format:

```
<class_id> <x1> <y1> <x2> <y2>
```

Where `<class_id>` is the index of the class label, and `(x1, y1)` and `(x2, y2)` represent the top-left and bottom-right corners of the bounding box, respectively.

## How to Use

1. Place your images for annotation in the `images/` folder.
2. Ensure the script and images are in the same directory.
3. Run the script using a Python interpreter: `python yolo_annotator.py`.
4. An image window will appear, and you can use the key bindings described below to annotate the image.
5. Once annotations are complete, press the 's' key to save the annotations and move to the next image.

## Key Bindings

- **Left Mouse Button (LMB):** Press and hold to draw bounding boxes. Release to confirm the bounding box and assign a class label.
- **Right Mouse Button (RMB):** Click to cycle through available class labels.
- **'c' key:** Clear all bounding boxes on the current image.
- **'s' key:** Save annotations and move to the next image.
- **'d' key:** Delete the last drawn bounding box.
- **'q' key:** Quit the annotation tool.

## License

This script is provided under the MIT License. Feel free to modify and distribute it as needed.

---

_Note: This annotation tool is intended for simple use cases. For more complex annotation tasks, consider using dedicated annotation tools or frameworks._
