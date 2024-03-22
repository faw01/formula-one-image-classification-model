# formula-one-image-classification-model
Repository holds code and data for image classification model - of cars representing particular teams in Formula 1.

# Repository structure
- `/input`: data for model training, validation and testing are stored here. The amount of images commited is an example - I reduced their number to lessen the amount of storage held in GitHub/GitLab,
- `/logs`: place for logs created during model training,
- `/models`: space for binary model file (h5 format),
- `formula-one-image-classification.ipynb`: improved / fixed jupyter notebook explaining model training process (once again, by [faw](https://github.com/faw01)).

# Example
## Image
![sample image](./input/lando-norris-mclaren-mcl35m-1.png)

## Output
```
1th Prediction: mclaren with 58.55% confidence.
2th Prediction: ferrari with 41.36% confidence.
3th Prediction: bwt with 0.07% confidence.
4th Prediction: williams with 0.01% confidence.
5th Prediction: alfa_romeo with 0.00% confidence.
6th Prediction: redbull with 0.00% confidence.
7th Prediction: mercedes with 0.00% confidence.
8th Prediction: toro_rosso with 0.00% confidence.
9th Prediction: haas with 0.00% confidence.
10th Prediction: renault with 0.00% confidence.
```

# Sources / Acknowledgements
## F1 Cars
### classification model: [by faw, available here](https://github.com/faw01/formula-one-image-classification-model),
### images dataset: [by Sérgio Gomes and José Henrique Brito, available here](https://github.com/2AiBAIT/F1CarsDataset).