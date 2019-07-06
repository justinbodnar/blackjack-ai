from __future__ import absolute_import, division, print_function

# tf and keras
import tensorflow as tf
#from tensorflow import keras
import keras
#from keras.models import model_from_json

# helper libs
import numpy as np
import matplotlib.pyplot as plt

# Blackjack import
from Blackjack import *
import Blackjack as bj

# lets make some data sets
import Blackjack as bj

#bj.gen_data_set( 500000, "blackjack3-2", 3, False )


# get the data set
data = open( "data_sets/blackjack3-2-out.data2").readlines()
tags = open( "data_sets/blackjack3-2-out.tags2").readlines()
data_clean = []
tags_clean = []
#strip whitespace
first = True
i = 0
for datum in data:
	print( i )
	i = i + 1
	# skip empty line first
	if first:
		first = False
		continue
	clean_datum = datum[1:datum.index('\n')-1].strip().split(', ')
	clean_datum[0] = int( clean_datum[0] )
	clean_datum[1] = int( clean_datum[1] )
#	print( clean_datum )
	data_clean = data_clean + [ clean_datum ]

first = True
for tag in tags:
	if first:
		first = False
		continue
	tag = tag[:tag.index('\n')]
	if tag is "h":
		tags_clean = tags_clean + [ 1.0 ]
	else:
		tags_clean = tags_clean + [ 0.0 ]

size = int( len(data)*(0.75) )

train_data = np.array( data_clean[1:size] )
train_tags = np.array( tags_clean[1:size] )
test_data = np.array( data_clean[size:] )
test_tags = np.array( tags_clean[size:] )

model = keras.Sequential()
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(1028, input_dim=54) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )
model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data, train_tags, epochs=10)
test_loss, test_acc = model.evaluate(test_data, test_tags)
print('Test accuracy:', test_acc)

# save model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
model_json = model.to_json()
with open( "models/blackjackmodel.3-2-out.json", "w") as json_file:
	json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("models/blackjackmodel.3-2-out.h5")
print( "Model saved" )


wins, losses, ties = test_model( "blackjackmodel.3-2-out", 10000, False, 3, False )
total = wins + losses + ties
win_percentage = (wins/total)*100.0
loss_percentage = (losses/total)*100.0
tie_percentage = (ties/total)*100.0
print( "Percentage won:  " + str( win_percentage ) )
print( "Percentage lost: " + str( loss_percentage ) )
print( "Percentage tied: " + str( tie_percentage ) )


