# BlackJack-AI - Machine Learning Library for Card Games

A Python library designed for training TensorFlow neural networks to play Blackjack and implement card-counting strategies. This project serves as both a practice ground for improving AI/ML skills and an educational tool for students exploring canonical AI/ML problems, such as decision-making and strategy optimization in Blackjack.

For more information on `Deck.py`, please read [the Deck.py documentation](DECK.md)

## Blackjack.py

The `Blackjack.py` module is responsible for generating datasets of Blackjack hands using Monte Carlo simulations. It creates randomized hands, simulates decision-making processes, and stores structured representations of these hands along with their corresponding outcomes.

## Installation

Clone the repository and install dependencies:
```bash
git clone https://github.com/justinbodnar/Artificial-Intelligence-in-BlackJack-Card-Counting.git
pip install -r requirements.txt
```

## Generating Blackjack Datasets

Use `Blackjack.py` to generate datasets with the following code:
```python
import Blackjack as blackjack
blackjack.gen_data_set(100, "test", 1)
```

The `gen_data_set()` function accepts the following parameters:

- **`num_hands` (int)**:  Specifies the number of hands to simulate.  
  - Example: `100` will simulate 100 hands.  
  - Note: Each "hit" action generates additional data points.

- **`file_name` (str)**:  The base name of the dataset files to be created in the `/data_sets` directory.  
  - Example: `"test"` will generate the files `./data_sets/test.data` and `./data_sets/test.tags`.

- **`info_level` (int)**:  
  Determines the amount of information to include in the dataset. Available levels:  
  - **`1`**: Includes only the player's hand value.  
  - **`2`**: Includes the player's hand value and the dealer's face-up card.  
  - **`3`**: Includes all cards seen so far.

## Data Representation for Training

### Hands
Player hands are represented as integers for simplicity and consistency within the dataset.  
For example: `18`, `10`, or `21`.

### Decisions
Each decision made by the player is tagged with one of two possible labels:
- **`h`**: Indicates the player chose to hit.
- **`s`**: Indicates the player chose to stay.

### Tagging Logic
The tagging process assigns `h` or `s` based on the player's actions and outcomes:

1. **If the player hits:**
   - **Busts**: Tag = `s`
   - **Does not bust**: Tag = `h`

2. **If the player stays:**
   - **Wins the hand**: Tag = `s`
   - **Loses the hand**: Tag = `h`


### Example Dataset Format
Each entry in the dataset includes the following:
- **Hand Representation**: An integer value representing the player's hand.
- **Tag**: Either `h` (hit) or `s` (stay).

#### Sample Dataset

| Hand Value | Decision Tag |
|:----------:|:------------:|
|     15     |      `h`     |
|     22     |      `s`     |
|     19     |      `s`     |
|     14     |      `h`     |


This representation provides a standardized format, ensuring consistent and interpretable data across simulations.

### Example Scenarios

**Example 1: Dealer Busts**
1. **Initial Player Hand:** `(3♠, 4♣)`  
   - Hand Value: `7`  
   - Player chooses to **hit**.
2. **Updated Player Hand:** `(3♠, 4♣, 12♦)`  
   - Hand Value: `19`  
   - Player chooses to **stay**.
3. **Outcome:** The dealer busts, resulting in a win for the player.

**Generated Dataset Entries:**
- `7, h`  → **Player hits** on a hand value of `7`.  
- `19, s` → **Player stays** on a hand value of `19`.

**Generated data and tags**:
```
7, h
19, s
```

**Example 2**: Player Busts
1. **Initial Player Hand:** `(2♦, 10♣)`  
   - Hand Value: `12`  
   - Player chooses to **hit**.
2. **Updated Player Hand:** `(2♦, 10♣, 2♠)`  
   - Hand Value: `14`  
   - Player chooses to **hit** again.
3. **Updated Player Hand:** `(2♦, 10♣, 2♠, 9♣)`  
   - Hand Value: `23` (Bust).  
   - The player **busts**, ending the round.

**Generated Dataset Entries:**
- `12, h`  → **Player hits** on a hand value of `12`.  
- `14, s` → **Player stays** on a hand value of `14`.

**Generated data and tags**
```
12, h
14, s
```

# First Blackjack Model - Dataset Level 1

The first model trains a neural network to play Blackjack using only the value of the current hand as input. A dataset for this task was generated with 3,959 Monte Carlo simulations using `Blackjack.py`. The dataset is stored in `/data_sets/blackjack.data.1` and `/data_sets/blackjack.tags.1`.

### Creating Level 1 Dataset

<pre>
import Blackjack as bj
bj.gen_data_set( 3000, "blackjack1", 1 ) # this was renamed later
</pre>


### Preprocessing Level 1 Datset

<pre>
# get the dataset
data = open( "data_sets/blackjack2-2-out.data").readlines()
tags = open( "data_sets/blackjack2-2-out.tags").readlines()
data_clean = []
tags_clean = []

#strip whitespaces and such
first = True
i = 0
for datum in data:

	# skip empty line first
	if first:
		first = False
		continue
	clean_datum = datum[:datum.index('\n')].strip()
	data_clean = data_clean + [ int(clean_datum) ]

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

The model in this example is a dense 2-layer neural network. The first layer consists of 4,096 neurons, while the second layer contains 2 neurons, corresponding to the decisions: "hit" or "stay." The model uses the **Adam** optimizer with a loss function of **sparse_categorical_crossentropy**. Training and testing data are split randomly in a 50/50 ratio, and the model is trained for 10 epochs.

### Training a Model

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

The model evaluates its accuracy using a **train-test split**, where 25% of the dataset is randomly designated as the test set. The remaining 75% is used for training. After training, the model can be saved using the following command:

### Saving the Model

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

### Using The Model

To determine a heuristic, hand values ranging from 2 to 21 were tested on the classifier. This process requires deserializing the model from its saved file.

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

The test cases were provided using the following code:

<pre>
print( "testing model" )

for i in range(21):
	prediction = model.predict( np.array([ [i,10] ]) )
	if prediction[0][0] > prediction[0][1]:
		print( str(i) + " stay" )
	else:
		print( str(i) + " hit" )
</pre>

This process produced the following output:

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

The model learned to hit on any hand value below 17, which aligns with the strategy typically employed by the dealer.

To evaluate the model against a large number of Monte Carlo simulations, the `test_model()` function in `Blackjack.py` can be used. The command is:

<pre>
wins, losses, ties = test_model( "blackjackmodel.1", 10000, True, 1, False )
total = wins + losses + ties
win_percentage = (wins/total)*100.0
loss_percentage = (losses/total)*100.0
tie_percentage = (ties/total)*100.0
print( "Percentage won:  " + str( win_percentage ) )

</pre>

The win percentage for this model, tested over 10,000 games, is **52.42%**.

# Second Blackjack model - Dataset Level 2

This model builds upon the previous techniques by including the dealer's face-up card in the dataset.

Previously, data was represented as a single integer for the player's hand. Now, the data consists of a tuple: `(player_hand, dealer_hand)`, where:
- `player_hand`: The player's current hand value.
- `dealer_hand`: The dealer's face-up card.

#### Example
```plaintext
[ 18, 13, s ]
```
In this example:
- `18` is the player's hand value.
- `13` is the dealer's face-up card.
- `s` indicates the decision to stay.


Number of Simulations: **5,323**

Location:
  - Data File: /data_sets/blackjack.data.2
  - Tags File: /data_sets/blackjack.tags.2

### Creating Level 2 Dataset

<pre>
import Blackjack as bj
bj.gen_data_set( 4000, "test", 2 ) # this was renamed later
</pre>

### Preprocessing Level 2 Dataset

<pre>
# get the dataset
data = open( "data_sets/blackjack2-2-out.data").readlines()
tags = open( "data_sets/blackjack2-2-out.tags").readlines()
data_clean = []
tags_clean = []
#strip whitespace
first = True
i = 0
for datum in data:

	# skip empty line first
	if first:
		first = False
		continue
	clean_datum = datum[:datum.index('\n')].strip()
	clean_datum = clean_datum[1:-1].split(',')
	clean_datum[0] = int( clean_datum[0] )
	clean_datum[1] = int( clean_datum[1][1:] )
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

The neural network used a similar layer structure as the previous model, but with a **16-neuron second layer**. The optimizer was **Nadam**, and the model was trained for **100 epochs**.

### Training a Model

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

The only difference between the training of Model 1 and Model 2 lies in the parameters and file names used.

### Testing The Model

For testing purposes, I referenced a helpful Blackjack strategy chart available at [wizardofodds.com](https://wizardofodds.com/games/blackjack/strategy/calculator/).


Generating a similar table through the neural network can be done using the following method:

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

This process produces the following chart:

![Blackjack classifier results](https://raw.githubusercontent.com/justinbodnar/artificial-intelligence-in-card-games/master/docs/blackjack_odds_mine.png)

There is a clear pattern in both charts, confirming that the neural network has begun to learn the strategy of Blackjack.

To evaluate the model against a large number of Monte Carlo simulations, the `test_model()` function in `Blackjack.py` can be used. The command is:


<pre>
wins, losses, ties = test_model( "blackjackmodel.2", 10000, True, 2, False )
total = wins + losses + ties
win_percentage = (wins/total)*100.0
loss_percentage = (losses/total)*100.0
tie_percentage = (ties/total)*100.0
print( "Percentage won:  " + str( win_percentage ) )
print( "Percentage lost: " + str( loss_percentage ) )
print( "Percentage tied: " + str( tie_percentage ) )
</pre>

The win percentage for 10,000 games with this model is **41.49%**. Interestingly, this result is less accurate than the model that used less information about the game. This discrepancy suggests that the dataset may be incorrect, corrupt, or otherwise flawed. This issue will be revisited in future revisions.

# Third Blackjack Model - Dataset Level 3

This model builds upon the previous ones by including a record of all cards seen so far in addition to the player's hand and the dealer's face-up card. The simulation assumes the dealer is using a single deck, which is reshuffled once the cards run out. This is where we begin simulating real card counting.

- Number of Data Points: 16,979
- Location:
  - Data File: /data_sets/blackjack.data.3
  - Tags File: /data_sets/blackjack.tags.3

### Creating Level 3 Dataset

<pre>
import Blackjack as blackjack
blackjack.gen_data_set( 12000, "test", 3 )
</pre>

### Preprocessing Level 3 Dataset

<pre>
# get the dataset
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

### Training a Model

The third model features two hidden layers with **64** and **128 neurons**, respectively. The optimizer used was **Adam**, and the model was trained for **50 epochs**. The serialized model is stored at `/models/blackjackmodel.3.json` and `/models/blackjackmodel.3.h5`

<pre>
model = keras.Sequential()
model.add( keras.layers.Dense( 54, input_dim=54 ) )
model.add( keras.layers.Dense( 64, input_dim=26 ) )
model.add( keras.layers.Dense( 128, input_dim=13 ) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )

model.compile(optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy'])

model.fit(train_data, train_tags, epochs=50)

test_loss, test_acc = model.evaluate(test_data, test_tags)

print('Test accuracy:', test_acc)
</pre>

The model had an accuracy of 0.73, similiar to the last two models.

### Using The Model

To evaluate the model against a large number of Monte Carlo simulations, use the `test_model()` function in `Blackjack.py`. The command is:

<pre>
wins, losses, ties = test_model( "blackjackmodel.3", 10000, True, 3, False )
total = wins + losses + ties
win_percentage = (wins/total)*100.0
loss_percentage = (losses/total)*100.0
tie_percentage = (ties/total)*100.0
print( "Percentage won:  " + str( win_percentage ) )
print( "Percentage lost: " + str( loss_percentage ) )
print( "Percentage tied: " + str( tie_percentage ) )
</pre>

The win percentage for 10,000 games with this model is **41.33%**. This result is less accurate than all other models that used less information about the game. This suggests that the dataset may be incorrect, corrupt, or otherwise flawed. This issue will be revisited in future revisions.

# Issues regarding the datasets

### 

Consider the final test results.

|      Strategy       |   Win Percentage   |
|:-------------------:|:------------------:|
|     **Level 1**     |       51.82%       |
|     **Level 2**     |       41.49%       |
|     **Level 3**     |       41.33%       |
| **Only Hitting**    |       3.42%        |
| **Only Staying**    |       41.99%       |
| **Random Moves**    |       30.67%       |

Level 1 is the most accurate model, with performance declining as additional game information is introduced in Levels 2 and 3. This counterintuitive result suggests issues such as overfitting, noisy data, or inconsistencies in the datasets that require further investigation and refinement. 

Notably, the best-performing classifier (Level 1) is only **9.17%** more accurate than the strategy of always staying. Levels 2 and 3 perform slightly worse than always staying, though the difference is negligible. This highlights the need to improve dataset quality and address potential flaws, such as conflicting or redundant information.

### Repeating Hands

The dataset contains multiple identical hands, resulting in redundancy and unnecessary inflation of the dataset. To address this, the script `/data_sets/preproc.py` was created to identify and remove duplicate entries, ensuring each hand is represented only once.

### Conflicting Tags

In some scenarios, the same hand results in conflicting conclusions, leading to opposing tags in the dataset. This inconsistency can confuse the model during training. The script `/data_sets/preproc.py` resolves these conflicts by removing the data point with fewer occurrences, maintaining consistency in the dataset.

### Project Roadmap

- **Functionalization**: Refactor `./data_sets/pre_proc.py` into a modular function for integration into `blackjack.py`
- **Dataset Validation**: Verify the integrity and consistency of the datasets to identify issues such as conflicting tags, missing data, or incorrect labels.
- **Hyperparameter Optimization**: Experiment with hyperparameters to determine if adjustments (e.g., learning rate, number of epochs) improve performance with the more complex datasets.
- **Data Restructuring**:  Explore alternative ways of representing and structuring the data.
