import tensorflow as tf
from tensorflow.keras.models import load_model
import cv2
import pandas as pd
import numpy as np
import plotly.express as px

from .constants import *

def initialize_model(path, input_path):
    data = tf.keras.utils.image_dataset_from_directory(input_path)
    class_names = data.class_names
    label_to_class = {i: class_name for i, class_name in enumerate(class_names)}
    return label_to_class, load_model(path)

def predict_image(filepath, model, labels):
    image_np = cv2.imread(filepath)
    # image_np = np.frombuffer(file, np.uint8)
    # img = cv2.imdecode(image_np, cv2.IMREAD_COLOR)  
    img_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
    input_shape = (256, 256)
    resized_img = cv2.resize(img_rgb, input_shape)
    resized_img_normalized = resized_img / 255.0
    input_data = np.expand_dims(resized_img_normalized, axis=0)
    yhat = model.predict(input_data)
    sorted_indices = np.argsort(yhat[0])[::-1]
    prefixes = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th']
    response = {
        'prediction': {
            'class': '',
            'confidence_percent': 0.0,
            'message': ''
        },
        'predictions': {}
    }
    for i, index in enumerate(sorted_indices):
        prob = yhat[0][index]
        class_name = labels[index]
        message = f'{i+1}{prefixes[i]} Prediction: {class_name} with {prob*100:.2f}% confidence.'
        temp_dict = {
            'class': class_name,
            'confidence_percent': round(prob*100,2),
            'message': message
        }
        if i == 0:
            response['prediction'] = temp_dict
        response['predictions'][i+1] = temp_dict
    return response

def make_chart(prediction_data):
  chart_filepath = './static/temp_file_plotly_graph.html'
  colors_teams_chart = colors_teams
  teams_number = len(teams)
  range_chart = list(range(0, 360, 360 // teams_number))
  class_majority = prediction_data['prediction']['class']
  prediction_majority = prediction_data['prediction']['confidence_percent']
  team_majority = list(filter(lambda x: teams_classes[x] == class_majority, teams_classes))[0]

  f1_data = pd.DataFrame(colors_teams_chart.items(), columns=['team', 'color'])
  f1_data_temp = pd.DataFrame(teams_classes.items(), columns=['team', 'team_class'])
  f1_data = pd.merge(f1_data, f1_data_temp, how='left', on='team')
  f1_data['direction'] = range_chart
  
  prediction_dict = {
     'team_class': [],
     'prediction_value': [],
     'prediction': []
  }
  
  for single_prediction in prediction_data['predictions']:
     prediction_dict['team_class'].append(prediction_data['predictions'][single_prediction]['class'])
     prediction_dict['prediction_value'].append(prediction_data['predictions'][single_prediction]['confidence_percent'])
     prediction_dict['prediction'].append('{}%'.format(prediction_data['predictions'][single_prediction]['confidence_percent']))

  f1_data_temp = pd.DataFrame.from_dict(prediction_dict)
  prediction_df = pd.merge(f1_data, f1_data_temp, how='left', on='team_class')

  chart_title = '''Formula 1 Image Classification Model<br>
  <b>Team Prediciton: {} - {}%</b><br>
  <sup>Hover chart bars to see value of predictions</sup><br>'''.format(team_majority, prediction_majority)

  fig = px.bar_polar(
    prediction_df, 
    r="prediction_value", 
    theta="direction", 
    template="plotly_dark", 
    color="team", 
    color_discrete_map = colors_teams_chart, 
    hover_data={
      'team': False,
      'direction': False,
      'prediction_value': False,
      'prediction': True
    },
    title=chart_title)

  fig.update_layout(
      polar={
          "angularaxis": {
              "tickmode": "array",
              "tickvals": range_chart,
              "ticktext": teams
          },
          "radialaxis": {
            'side': 'counterclockwise',
            'range':[0, 100],
            'showticklabels': True,
            'ticks':''
            },
            "bgcolor": "rgb(16,16,23)",
      },
      showlegend=False,
      title_x=0.5,
      title_y=0.95,
      plot_bgcolor="rgb(16,16,23)",
      paper_bgcolor="rgb(16,16,23)"
  ) 

  fig.update_traces()
  
  with open(chart_filepath, 'w') as f:
    f.write(fig.to_html(include_plotlyjs='cdn'))

  return chart_filepath