# 3D MNIST

This repository contains a notebook exploring different architectures for classifying 3D MNIST data. It compares the performance of a newer ResNet-style architecture with skip connections against a traditional convolutional neural network (CNN). The analysis includes training accuracy, validation accuracy, and weight distribution metrics to highlight the advantages and challenges of each approach.

Key comparisons include:

- Traditional sequential CNN vs. ResNet-style model
- Effect of residual connections on feature learning
- Differences in weight distribution and training stability

## Observations

### Architectures

**Architecture 1:**
![Model Architecture 1](./images/model_architecture_1.png)

**Architecture 2:**
![Model Architecture 2](./images/model_architecture_2.png)

The two architectures are different in that the first architecture uses traditional sequential CNN architecture, whilst the second architecture uses a ResNet-style with skip connection and identity mappings.

For the first architecture, progressive feature extraction with increasing filter sizes is used (8 -> 16 -> 32 -> 64). The second architecture maintains consistent feature maps within blocks (16 -> 32 -> 64) and uses residual connections to preserve information flow.

The first network uses a single batch normalization layer at the end whilst the second uses multiple batch normalization and activation pairs after each convolution based on ResNet best practices.

For downsampling, the first network has a larger dense section (2048 -> 512 -> 10), whilst the second network has a more compact dense section (512 -> 128 -> 10)

In terms of parameter efficiency, the first network has more parameters in the dense layers, however, the second network has more parameters in the convolutional layers with fewer in the dense layers, which is generally better for spatial data.

Although the second network has more modern design choices like:

- Residual connections to help with gradient flow
- More consistent use of batch normalization
- Global Average Pooling to reduce parameters
- Better parameter distribution

## Performance Metrics

The following is the graph between the two best runs on different model architectures:

![Training and Validation](./images/Accuracy.png)

### Training Accuracy

The newer run (20250130-204504\train - pink) achieves a higher final accuracy (~0.99) compared to the run (20250130-201452\train - orange) which reached about (~0.95). So the rapid increase in accuracy suggests an aggressive learning approach from higher learning weights and weight updates.

### Validation Accuracy

The newer run (20250130-204504\validation - cyan) has a much lower validation accuracy (~0.5 to ~0.6) compared to the earlier run (20250130-201452\validation in blue) which stabilized around ~0.6. The validation curve fluctuates heavily in the newer model.

## Weight Distribution Metrics

![Beta and Bias Histogram](./images/beta_and_bias_histogram.png)

### Beta Histogram

The beta histogram shows the distribution of the weight tensors during training. It helps in visualizing how the values of the tensors evolve over time.

The `20250130-201452\train` histogram shows a relatively smooth distribution of the beta parameters values. So the spread stays narrow showing stable updates. Whereas the `20250130-204504\train` has an oscillating pattern with increasing spread over time. Which can be indicative of instability or a higher learning rate causing fluctuations in th e beta parameter.

### Bias histogram

The bias histogram shows the distribution of bias values in the model's layer during training.

From the `20250130-201452\train` we can see that values are centered around 0, where they gradually spread out in a controlled manner. Whilst `20250130-204504\train` shows oscillations and increasing variance over time, which indicate more unstable updates. We can link this back to the beta histogram indicating instability.

![Gamma and Kernel Histogram](./images/gamma_and_kernel_histogram.png)

### Gamma Histogram

The purpose of the Gamma histogram is to monitor the scaling parameters in batch normalization. From the `20250130-201452\train` the more stable gamma values can indicate less feature adaption, whilst `20250130-204504\train` suggests more dynamic feature learning, possibly due to the residual connection.

### Kernel Histograms

These are use to track the distribution in of the learned weights in convolutional layers, which are often useful to see things like vanishing gradients, dead neurons, weight saturation and unhealthy initialization effects. `20250130-201452\train - Orange)` are disturbed in a relatively stable manner, which suggests controlled weight updates. `(20250130-204504\train - Pink)` appears to have higher oscillations and is more dynamic compared to the first model. The range of weight values fluctuates more, which indicates a higher learning rate, and potential instability, with the risk of overfitting.

## Analysis

We can see on the runs where there are more rapid fluctuations, it can be due to a high learning rate, and since on the first run we changed the architecture to reduce the amount of dropout, this instability is due to the decrease in the regularization. We also see with the later run that validation accuracy is lower than the initial run, and we have higher training accuracy than the first run which is a sure sign of over fitting.

## Next Steps

1. Reduce Learning rate
2. Apply L2, weight decay, and/or increase the amount of dropout we do to control the over-fitting

# Conclusion

From the comparison of the two architectures, we observe that while the second model (ResNet-Style) introduces design principles, improved batch normalization placement, and average pooling, its performance metrics indicate challenges in stability and generalization.

The newer model exhibits higher training (~0.99 vs. ~0.95) but suffers from lower validation accuracy (~0.5 - 0.6 vs ~0.6), suggesting overfitting. This is reinforced by beta, bias, gamma, and kernel histogram, which show more oscillatory and unstable weight distributions compared to more controlled updates of the first model. The rapid weight fluctuations likely stem from a higher learning rate and reduced regularization, leading to unstable convergence/

To improve generalization, reducing the learning rate and reintroducing (L2, dropout) are necessary next steps. These adjustments should help balance of ResNet-style architecture while ensuring stable training and improved validation performance.

By refining these hyperparameters, we can better leverage the benefits of the second model while addressing the overfitting concerns observed in the analysis.
