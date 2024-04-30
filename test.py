import json


# We are adding nan values
# (out of range float values)
# in dictionary
Dictionary ={(1, 2, 3):'Welcome', 2:'to',
			3:'Geeks', 4:'for',
			5:'Geeks', 6:float('nan')}

# If we hadn't set allow_nan to 
# true we would have got 
# ValueError: Out of range float 
# values are not JSON compliant
json_string = json.dumps(Dictionary,
						skipkeys = True,
						allow_nan = True)

print('Equivalent json string of dictionary:', 
	json_string)
