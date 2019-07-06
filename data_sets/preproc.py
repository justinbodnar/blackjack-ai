# this script helps to process data sets
# there will surely be double situations
# so lets take care of them
data = open( "blackjack2-2.data" ).readlines()
tags = open( "blackjack2-2.tags" ).readlines()
data_out = open( "blackjack2-2-out.data", "w+" )
tags_out = open( "blackjack2-2-out.tags", "w+" )

# for skipping the initial empty line
first = True

# print original length
print( "Before: " + str( len(data) ) )

# instantiate empty dicts
initial = { }
final = {}

# loop through data to make initial dict
for i in range( len(data) ): # we assume the lists are equal in cardinality
	if first:
		first = False
		continue
	key = data[i].strip() + ":" + tags[i].strip()
	if key in initial.keys():
		initial[ key ] = initial[ key ] + 1
	else:
		initial[ key ] = 1

# loop through initial dict to make final dict
for key in initial.keys():

	# output for debugging
	print( "key: "     + key )
	print( "element: " + str( initial[ key ] ) )

	# form reverse key first
	if key[-1] is "h":
		reverse_key = key[:-1] + "s"
	else:
		reverse_key = key[:-1] + "h"


	print( "reverse: " + reverse_key )

	# if reverse key in dict
	if reverse_key in initial.keys():
		# insert higher element containign key into final output files
		if initial[ reverse_key ] > initial[ key ]:
			# strip into data and tag
	                data = reverse_key.split(':')[0]
	                tag = reverse_key.split(':')[1]
	                data_out.write( data + "\n" )
	                tags_out.write( tag + "\n" )

		else:
			# strip into data and tag
	                data = key.split(':')[0]
	                tag = key.split(':')[1]
	                data_out.write( data + "\n" )
	                tags_out.write( tag + "\n" )

	# else reverse_key not in dict
	else:
		# insert key into final
		# strip key into data and tag for seperate file insertion
		data = key.split(':')[0]
		tag = key.split(':')[1]
		data_out.write( data + "\n" )
		tags_out.write( tag + "\n" )

data_out.close()
tags_out.close()

# print final length of data set
print( "After: " + str( len(data) ) )
