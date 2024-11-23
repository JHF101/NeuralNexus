# Malaria Parasite Detection Challenge

## Overview

The objective of this challenge was to create a machine learning solution for **multiclass object detection and classification** of malaria parasites in blood slide images. Specifically, the task involved identifying the **trophozoite stage** of malaria and distinguishing between infected and uninfected blood cells.

This scalable AI solution aims to support large-scale screening, alleviate the burden on healthcare workers, and improve healthcare efficiency in resource-limited settings.

### Key Metrics

The competition used **Mean Average Precision @ IoU threshold 0.5 (mAP@0.5)** to evaluate model performance. Submissions needed to predict bounding boxes and classification for objects in images in the specified format.

---

## My Solution

For this challenge, I implemented a robust and efficient machine learning pipeline that utilized state-of-the-art techniques for image preprocessing, model training, and experiment tracking.

### Techniques and Tools

1. **Data Augmentation with Albumentations**

   - To enhance the model's ability to generalize, I applied various augmentation strategies using the Albumentations library.
   - Augmentation techniques included:
     - Random rotations
     - Brightness and contrast adjustments
     - Horizontal and vertical flips
     - Blurring and noise injection
   - These transformations simulated real-world variability in blood slide images, making the model more robust.

2. **Model Training with Ultralytics YOLO**

   - I trained multiple versions of the **YOLO (You Only Look Once)** object detection models using the Ultralytics framework.
   - Different YOLO architectures (e.g., YOLOv11) were experimented with to balance performance and computational efficiency.
   - To specialize the model for the malaria dataset, I froze the backbone layers of the YOLO model and fine-tuned the neck and head layers. This approach retained pre-trained feature extraction capabilities while adapting the detection layers for malaria-specific objects.
   - Hyperparameter tuning was employed to optimize detection accuracy while adhering to the computational resource constraints.

3. **Experiment Tracking with MLflow**
   - All experiments were tracked using **MLflow** to ensure reproducibility and transparency.
   - Tracked metrics included:
     - Model architecture and hyperparameters
     - Training and validation loss
     - mAP scores
   - MLflow also helped in managing multiple model runs and selecting the best-performing version for submission.

---

## Key Results

- Achieved high mAP@0.5 scores by leveraging advanced data augmentation and optimized YOLO v11n. ([PR Curve](training_results/PR_curve.png)). The WBC score was very high at the top right corner indicating high precision and recall, which aligns with the excellent mAP score of 0.980, however the Trophozoite curve is lower, especially at higher recall values, reflecting the slightly lower mAP score of 0.75. Which shows the models struggles with this class.
- However, the **confidence scores** for some predictions were notably low, especially for smaller objects and overlapping blood cells. This indicates that the model was uncertain in distinguishing between classes, particularly under challenging conditions ([Predictions](training_results/val_batch1_pred.jpg)).

### Discussion on Low Confidence Scores

The low confidence of the model can be attributed to several factors:

1. **Class Imbalance**

   - The dataset may have had an uneven distribution of classes (e.g., fewer trophozoite examples compared to WBCs or NEG). This could lead the model to perform better on majority classes while struggling with underrepresented ones.

   **Improvement Strategy:** Use techniques like **oversampling of minority classes**, **class-specific augmentation**, or **loss weighting** to ensure balanced training.

2. **Insufficient Training Data Variability**

   - Despite the applied augmentations, the model may have struggled to generalize to real-world variability, such as lens blur, lighting inconsistencies, or differences in the cameras used to capture the images.

   **Improvement Strategy:** Increase data diversity through **domain-specific augmentations**, such as mimicking lighting conditions, blur, or stain artifacts common in blood slides.

3. **Model Architecture Limitations**

   - Although YOLO architectures are efficient, certain variations may not be optimal for detecting small, dense objects like blood cells.

   **Improvement Strategy:** Experiment with architectures designed for small object detection, such as **Faster R-CNN**, or incorporate higher-resolution input images during training.

Addressing these challenges could significantly improve the model's confidence scores, resulting in more reliable predictions and better real-world applicability.

## Challenge Impact

This project was an opportunity to contribute to an important global health challenge. The resulting model can assist in:

- Scaling malaria diagnostics in remote areas.
- Reducing dependency on skilled technicians for microscopic examination.
- Enhancing early detection and treatment, ultimately saving lives.

---

## Acknowledgments

This challenge was supported by:

- **Lacuna Fund**: Addressing the gap in labeled datasets for underserved populations.
- **Makerere AI Health Lab**: Advancing healthcare through innovative AI solutions.

For more information about malaria and its impact, visit [Lacuna Fund](https://www.lacunafund.org).
