SINGLE_NUMBER = {
	'один': 1,
	'два': 2,
	'три': 3,
	'четыре': 4,
	'пять': 5,
	'шесть': 6,
	'семь': 7,
	'восемь': 8,
	'первый': 1,
	'второй': 2,
	'третий': 3,
	'четвертый': 4,
	'пятый': 5,
	'шестой': 6,
	'седьмой': 7,
	'восьмой': 8,
	'двадцать': 2,
	'тридцать': 3,
	'сорок': 4,
	'пятьдесят': 5,
	'шестьдесят': 6,
	'семьдесят': 7,
	'восемьдесят': 8,
}

DOUBLE_NUMBER = {
	'одиннадцать': 11,
	'двенадцать': 12,
	'тринадцать': 13,
	'четырнадцать': 14,
	'пятнадцать': 15,
	'шестнадцать': 16,
	'семнадцать': 17,
	'восемнадцать': 18,
	'одиннадцатый': 11,
	'двенадцатый': 12,
	'тринадцатый': 13,
	'четырнадцатый': 14,
	'пятнадцатый': 15,
	'шестнадцатый': 16,
	'семнадцатый': 17,
	'восемнадцатый': 18,
}

TOOTH = 'зуб'
TOOTH_KEY_WORDS = set(SINGLE_NUMBER.keys())
TOOTH_KEY_WORDS.update(DOUBLE_NUMBER.keys())

INSPECTION_END = {'жалобы', 'жалобу'}

CHILD_FORMULA = [55, 54, 53, 52, 51, 61, 62, 63, 64, 65, 85, 84, 83, 82, 81, 71, 72, 73, 74, 75]
ADULT_FORMULA = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28, 48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]

VALID_NUMBERS = set(CHILD_FORMULA)
VALID_NUMBERS.update(ADULT_FORMULA)

VALUE_MAPPING = {
	'кариес': 'С',
	'пломба': 'П',
	'пломбакариес': 'П/С',
	'пульпит': 'PI',
	'периодонтит': 'Pt',
	'корень': 'R',
	'отсутствует': '0',
	'зубныеотложения': 'з/о',
	'дефектпломбы': 'д/п',
	'коронка': 'К',
	'вкладка': 'вк',
	'формирователь': 'Ф',
	'имплант': 'И',
	'рецессия': 'Р',
	'клиновидныйдефект': 'кл/д',
	'глубокаяфиссура': 'г/ф',
	'герметик': 'г/р',
	'подвижностьпервойстепени': 'I',
	'подвижностьвторойстепени': 'II-III',
	'подвижностьтретейстепени': 'II-III',
	'пришеечныйкариес': 'С/пр',
	'вторичныйкариес': 'С/втч',
	'скол': 'ск',
	'ретинированный': 'ret',
	'дистопированый': 'dys',
	'эстетическийдефект': 'э/д',
	'керамическаявкладка': 'In',

}

VALUE_WORDS = set(VALUE_MAPPING.keys())


REPLACE_MISTAKES = {
	'звук': 'зуб',
	'корис': 'кариес',
	'кариз': 'кариес',
	'карез': 'кариес',
	'карис': 'кариес',
	'корез': 'кариес',
	'колес': 'кариес',
	'каресс': 'кариес',
	'кариеса': 'кариес',
	'каринз': 'кариес',
	'кариус': 'кариес',
	'каверз': 'кариес',
	'кариездентина': 'кариес',
	'крс': 'кариес',
	'кс': 'кариес',
	'калия': 'кариес',
	'помба': 'пломба',
	'пломбы': 'пломба',
	'клумбы': 'пломба',
	'клоббы': 'пломба',
	'пломбам': 'пломба',
	'дефекты': 'дефект',
	'периодантид': 'периодонтит',
	'клиновильный': 'клиновидный',
	'кленовидный': 'клиновидный',
	'кальновидный': 'клиновидный',
	'лечен': 'пломба',
	'искусственный': 'имплант',
}

REPLACE_WORDS = {
	'дефект пломба': 'дефектпломбы',
	'клиновидный дефект': 'клиновидныйдефект',
	'пломба кариес': 'пломбакариес',
	'пломбоскол': 'пломба скол',
	'зубные отложения': 'зубныеотложения',
	'глубокая фиссура': 'глубокаяфиссура',
	'пришеечный кариес': 'пришеечныйкариес',
	'вторичный кариес': 'вторичныйкариес',
	'подвижность первой степени': 'подвижностьпервойстепени',
	'подвижность второй степени': 'подвижностьвторойстепени',
	'подвижность третей степени': 'подвижностьтретейстепени',
	'эстетический дефект': 'эстетическийдефект',
	'керамическая вкладка': 'керамическаявкладка',
	'запятая': '',
	'запитая': '',
	'на момент посещения': '',
	'осмотр': '',
}
