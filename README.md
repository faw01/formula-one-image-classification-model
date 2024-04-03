# formula-one-image-classification-model
Repository holds code and data for image classification model - of cars representing particular teams in Formula 1.

# Repository structure
- `/input`: data for model training, validation and testing are stored here. The amount of images commited is an example - I reduced their number to lessen the amount of storage held in GitHub/GitLab,
- `/logs`: place for logs created during model training,
- `/models`: space for binary model file (h5 format),
- `formula-one-image-classification.ipynb`: improved / fixed jupyter notebook explaining model training process (once again, by [faw](https://github.com/faw01)).

# Docker image
## Building
`docker build --no-cache -t f1-image-classification-model:v0.7 -f Dockerfile .`
## Running
`docker run -it f1-image-classification-model:v0.7`

# Adding image to use in minikube
`minikube image load f1-image-classification-model:v0.7`

# Example
## Image
![sample image](./input/lando-norris-mclaren-mcl35m-1.png)

## Output
```
1st Prediction: mclaren with 99.96% confidence.
2nd Prediction: bwt with 0.04% confidence.
3rd Prediction: toro_rosso with 0.00% confidence.
4th Prediction: williams with 0.00% confidence.
5th Prediction: mercedes with 0.00% confidence.
6th Prediction: haas with 0.00% confidence.
7th Prediction: redbull with 0.00% confidence.
8th Prediction: alfa_romeo with 0.00% confidence.
9th Prediction: ferrari with 0.00% confidence.
10th Prediction: renault with 0.00% confidence.
```
# Model structure
```
Model: "sequential"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Layer (type)                    ┃ Output Shape           ┃       Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ conv2d (Conv2D)                 │ (None, 254, 254, 16)   │           448 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d (MaxPooling2D)    │ (None, 127, 127, 16)   │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_1 (Conv2D)               │ (None, 125, 125, 32)   │         4,640 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_1 (MaxPooling2D)  │ (None, 62, 62, 32)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ conv2d_2 (Conv2D)               │ (None, 60, 60, 16)     │         4,624 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ max_pooling2d_2 (MaxPooling2D)  │ (None, 30, 30, 16)     │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ flatten (Flatten)               │ (None, 14400)          │             0 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense (Dense)                   │ (None, 256)            │     3,686,656 │
├─────────────────────────────────┼────────────────────────┼───────────────┤
│ dense_1 (Dense)                 │ (None, 10)             │         2,570 │
└─────────────────────────────────┴────────────────────────┴───────────────┘
 Total params: 3,698,938 (14.11 MB)
 Trainable params: 3,698,938 (14.11 MB)
 Non-trainable params: 0 (0.00 B)
```

# Sources / Acknowledgements
## F1 Cars
### classification model: [by faw, available here](https://github.com/faw01/formula-one-image-classification-model),
### images dataset: [by Sérgio Gomes and José Henrique Brito, available here](https://github.com/2AiBAIT/F1CarsDataset),
### containerization and API creation: [by Aleksander Zawalich, available here](https://github.com/azawalich).