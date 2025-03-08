from const import *


def _prepare_data(data):
	for rw in REPLACE_MISTAKES.keys():
		if rw in data:
			data = data.replace(rw, REPLACE_MISTAKES[rw])

	for rw in REPLACE_WORDS.keys():
		if rw in data:
			data = data.replace(rw, REPLACE_WORDS[rw])
	return data


def _get_teeth_number(words):
	result = None
	if len(words) == 1:
		result = DOUBLE_NUMBER.get(words[0])
	elif len(words) == 2:
		if words[0] in SINGLE_NUMBER and words[1] in SINGLE_NUMBER:
			result = SINGLE_NUMBER.get(words[0]) * 10 + SINGLE_NUMBER.get(words[1])
	if result in VALID_NUMBERS:
		return result


def _replace_numbers_data(data):
	new_data = [ ]
	curr = []
	for w in data.split():
		if w in DOUBLE_NUMBER:
			new_data.append('| ' + str(DOUBLE_NUMBER.get(w)))
		elif w in SINGLE_NUMBER:
			curr.append(w)
		elif curr:
			teeth_number = _get_teeth_number(curr)
			if teeth_number:
				new_data.append('| ' + str(teeth_number))
			curr = []
			new_data.append(w)
		elif w not in INSPECTION_END and w != TOOTH:
			new_data.append(w)
		if w in INSPECTION_END:
			break

	if curr:
		teeth_number = _get_teeth_number(curr)
		if teeth_number:
			new_data.append('| ' + str(teeth_number))
	return ' '.join(new_data)


def _parse_teeth_formula(result):
	unrecognized_words = set()

	is_child_formula = False
	formula = {}
	for teeth in result.split('|'):
		row = teeth.strip()
		if row:
			teeth_number = None
			values_words = []
			for word in row.split():
				if word.isnumeric():
					teeth_number = int(word)
				elif word in VALUE_WORDS:
					values_words.append(word)
				else:
					unrecognized_words.add(word)
			if teeth_number:
				if teeth_number > 50:
					is_child_formula = True
				formula[teeth_number] = ', '.join([VALUE_MAPPING.get(v) for v in values_words]) or '?'

	return {
		'type': 'child' if is_child_formula else 'adult',
		'formula': formula,
		'unrecognized_words': unrecognized_words,
	}


def get_result(data):
	return _parse_teeth_formula(_replace_numbers_data(_prepare_data(data)))


def get_formatted_formula(result):
	msg = []
	formula = result['formula']
	if 0 in formula:
		del formula[0]

	if formula:
		if result['type'] == 'child':
			for t in CHILD_FORMULA:
				if t in formula:
					msg.append(str(t) + ' - ' + formula[t])
				else:
					msg.append(str(t))
		else:
			for t in ADULT_FORMULA:
				if t in formula:
					msg.append(str(t) + ' - ' + formula[t])
				else:
					msg.append(str(t))
	else:
		msg.append('Формула не распознана')
	if result['unrecognized_words']:
		msg.append('Не распознаны слова: ' + ', '.join(result['unrecognized_words']))
	return '\n'.join(msg)
