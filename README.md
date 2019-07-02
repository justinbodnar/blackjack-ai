# Artificial Intelligence in Blackjack Card Counting
A python library for teaching TensorFlow neural networks to play Blackjack and count cards.

# Blackjack.py
Blackjack.py is used to generate data sets about hands of blackjack via Monte Carlo simulations. This is done by generating random hands, letting the computer make random moves, and storing representations of the hands tagged with the eventual outcome of the decision.

# Representing a hand of blackjack and generating your own data sets

To generate a data set of Blackjack hands using Monte Carlo simulations use:

<pre>
import Blackjack as blackjack
blackjack.gen_data_set( 100, "test", 1 )
</pre>

The first parameter is how many hands to play (note the data set may be larger as each 'hit' will generate another data point).
The second parameter is the name of the file to save to in the '/data_sets' directory. the example code will create two files '/data_sets/test.data' and '/data_sets/test.tags' If the data set already exists the new data points will be appended.
The third paramter is the level of information to put in the dataset.

Level 1 stores only information about the players hand value.
Level 2 stores level 1 plus the dealers face-up card.
Level 3 stores level 2 plus a record of all cards seen.

For the purpose of training a nuerel network to play blackjack, we want to represent a hand in a way that tells us whether we should 'hit' or 'stay.' Luckily we only need to store a few integers. We then tag the data as either 'h' or 's' for 'hit' or 'stay.'

How we determine whether the hand warrants a 'h' or 's' is a matter of opinion. The current iteration will simply append in the following manner:

<pre>
if user hits and busts:
	tag = 's'
elif user hits and doesn't bust:
	tag = 'h'
elif user stays and wins hand:
	tag = 's'
elif user stays and loses hand:
	tag = 'h'
</pre>

Example scenarios and expected data:

<pre>
Example 1

player hand: ( 3-s, 4-c )
player hits
player hand: ( 3-s, 4-c, 12-d )
player stays
dealer busts

generated data and tags:
(because we won the game, we assume every move was a good move)
7,  h # hit on 7
19, s # stay on 19

Example 2

player hand: ( 2-d, 10-c )
player hits
player hand: ( 2-d, 10-c, 2-s )
player hits
player hand: ( 2-d, 10-c, 2-s, 9-c )
player busts

generated data and tag

12, h
14, s
</pre>

# first Blackjack model - data set level 1

The first model teaches a neural net to play based soley on the value of the current hand. A data set for this task was produced with 3,959 monte carlo simulations generated with Blackjack.py. The data set is located at /data_sets/blackjack.data.1 and /data_sets/blackjack.tags.1.

code to create this data set

<pre>
import Blackjack as bj
bj.gen_data_set( 3000, "blackjack1", 1 ) # this was renamed later
</pre>


code for preprocessing the data set

<pre>
# get the data set
data = open( "data_sets/blackjack.data.1").readlines()
tags = open( "data_sets/blackjack.tags.1").readlines()
data_clean = []
tags_clean = []
#strip whitespace
first = True
for datum in data:
	# skip empty line first
	if first:
		first = False
		continue
	clean_datum = datum[1:datum.index('\n')-1].strip().split(', ')
	clean_datum[0] = int( clean_datum[0] )
	clean_datum[1] = int( clean_datum[1] )
	print( clean_datum )
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
</pre>

The model in this example a dense 2-layer neurel network. The first layer contained 4096 neurons, while the second only had two, for 'hit' or 'stay.' The 'adam' optimizer was used, with a loss of 'sparse_categorical_crossentropy.' Training and testing data was split 50/50 randomly. There are 10 epochs.

code for training the model

<pre>
model = keras.Sequential()
model.add( keras.layers.Dense(4096, input_dim=2) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )
model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data, train_tags, epochs=10)
test_loss, test_acc = model.evaluate(test_data, test_tags)
print('Test accuracy:', test_acc)
</pre>

The model will output the accuracy of the model, using a random 25% of input as test cases. The model can then be saved via

<pre>
# save model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
model_json = model.to_json()
with open( "models/blackjackmodel.1.json", "w") as json_file:
	json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("models/blackjackmodel.1.h5")
print( "Model saved" )
</pre>

To find a heuristic, hand values from 2-21 were tested on the classifier. To do this we need to first deserialize the model from its file

<pre>
# open serialized model
# taken from https://machinelearningmastery.com/save-load-keras-deep-learning-models/
json_file = open('models/blackjackmodel.1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = keras.models.model_from_json( loaded_model_json, custom_objects={"GlorotUniform": tf.keras.initializers.glorot_uniform} )
model.load_weights( "models/blackjackmodel.1.h5" )
print( "Model loaded from disk" )
</pre>

Giving the test cases was done via

<pre>
print( "testing model" )

for i in range(21):
	prediction = model.predict( np.array([ [i,10] ]) )
	if prediction[0][0] > prediction[0][1]:
		print( str(i) + " stay" )
	else:
		print( str(i) + " hit" )
</pre>

This gave the output

<pre>
0  hit
1  hit
2  hit
3  hit
4  hit
5  hit
6  hit
7  hit
8  hit
9  hit
10 hit
11 hit
12 hit
13 hit
14 hit
15 hit
16 hit
17 stay
18 stay
19 stay
20 stay
</pre>

The model learned to hit on any hand value below 17. This happens to be the strategy used by the dealer.

# Second Blackjack model - data set level 2

This model will use all the previous techniques, but the data set will now include the dealer's upward facing card.

So where previously we used the single integer for data, we will now use a tuple of players_hand, and dealers_hand respectively.

Example

[ 18, 13, s ]

The data set for this consists of 5,323 entries, located in data_sets/blackjack.data.2 and data_sets/blackjack.tags.2. Loading the data is done the same as in model 1.

code to generate this data set

<pre>
import Blackjack as bj
bj.gen_data_set( 4000, "test", 2 ) # this was renamed later
</pre>

The neural network used a similar layer scheme as the previous, with an 16-neuron second layer. The optimizer was 'nadam,' and there were 100 epochs.

code for training this network

<pre>
model = keras.Sequential()
model.add( keras.layers.Dense(16, input_dim=2) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )
model.compile(optimizer='nadam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])
model.fit(train_data, train_tags, epochs=100)
test_loss, test_acc = model.evaluate(test_data, test_tags)
print('Test accuracy:', test_acc)
</pre>

Notice the only difference between the training of model 1 and model 2 is parameters and file names.

For testing purposes I found this nifty chart for Blackjack strategy at wizardofodds.com/games/blackjack/strategy/calculator/

![Basic Blackjack Strategy](https://raw.githubusercontent.com/justinbodnar/artificial-intelligence-in-card-games/master/docs/blackjack_odds.png)

Generating s imiliar table through the neural entwork can be done via

<pre>
results = []

for i in range(0,17):
	results = results + [ "" ]
	for j in range(0,9):
		prediction = model.predict( np.array([ [i+5,j+2] ] ) )
		if prediction[0][0] > prediction[0][1]:
			results[i] = results[i] + "s"
		else:
			results[i] = results[i] + "h"
print( "  ", end="" )
for x in range( len(results[0]) ):
	print( " " + str( (x+4)%10 ), end="" )
print( )
for i in range( len(results) ):
	print( i+5, end="" )
	if i+5 < 10:
		print( "  ", end="" )
	else:
		print( " ", end="" )
	for j in range( len(results[i] ) ):
		print( results[i][j], end=" " )
	print( )
</pre>

This produces the following chart.

![Blackjack classifier results](https://raw.githubusercontent.com/justinbodnar/artificial-intelligence-in-card-games/master/docs/blackjack_odds_mine.png)

There is a clear pattern on both. This confirms the neural network has begun to learn the strategy of Blackjack.

The next model with contain information on which cards have been seen throughout the game, so that the model will learn to count cards.
