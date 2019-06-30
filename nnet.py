from __future__ import absolute_import, division, print_function

# tf and keras
import tensorflow as tf
#from tensorflow import keras
import keras
#from keras.models import model_from_json

# helper libs
import numpy as np
import matplotlib.pyplot as plt

# for saving models
import pickle

# introduction
print( "TensorFlow Version: " + tf.__version__ )

# get the data set
data = open( "data_sets/blackjack.data.1").readlines()
tags = open( "data_sets/blackjack.tags.1").readlines()
data_clean = []
tags_clean = []
#strip whitespace
for datum in data:
	data_clean = data_clean + [  datum[:datum.index('\n')] ]

for tag in tags:
	tag = tag[:tag.index('\n')]
	if tag is "h":
		tags_clean = tags_clean + [ 1.0 ]
	else:
		tags_clean = tags_clean + [ 0.0 ]

size = len(data)//2

train_data = np.array( data_clean[1:size] )
train_tags = np.array( tags_clean[1:size] )
test_data = np.array( data_clean[size:] )
test_tags = np.array( tags_clean[size:] )

#model = keras.Sequential([
#	keras.layers.Dense(128, activation=tf.nn.relu),
#	keras.layers.Dense(2, activation=tf.nn.softmax)
#])


#model = keras.Sequential()
#model.add( keras.layers.Dense(4096, input_dim=1) )
#model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )

#model.compile(optimizer='adam',
#	loss='sparse_categorical_crossentropy',
#	metrics=['accuracy'])

#model.fit(train_data, train_tags, epochs=10)

# save model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
#model_json = model.to_json()
#with open( "models/blackjackmodel.json", "w") as json_file:
#	json_file.write(model_json)
# serialize weights to HDF5
#model.save_weights("models/blackjackmodel.h5")
#print( "Model saved" )

# open serialized model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
json_file = open('models/blackjackmodel.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = keras.models.model_from_json( loaded_model_json, custom_objects={"GlorotUniform": tf.keras.initializers.glorot_uniform} )
model.load_weights( "models/blackjackmodel.h5" )
print( "Model loaded from disk" )

for i in range(21):
	print( i )
	prediction = model.predict( np.array( [ i ] ) )
	if prediction[0][0] > prediction[0][1]:
		print( "stay" )
	else:
		print( "hit" )
