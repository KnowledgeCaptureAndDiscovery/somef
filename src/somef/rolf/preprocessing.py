"""
Author: Jenifer Tabita Ciuciu-Kiss
"""

import pandas as pd
from nltk.corpus import stopwords
import re
import numpy as np
import inflect
import contractions
from bs4 import BeautifulSoup
import re, string, unicodedata
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk import word_tokenize


TEXT = 'Text'

class Preprocessor:

	def __init__(self, data : pd.DataFrame) -> None:
		self.data = data

	def denoise_text(self, text):
		# Strip html if any. For ex. removing <html>, <p> tags
		soup = BeautifulSoup(text, "html.parser")
		text = soup.get_text()
		# Replace contractions in the text. For ex. didn't -> did not
		text = contractions.fix(text)
		text.replace("""404: Not Found""", '')
		return text

	def remove_stop_words(self, text : str):
		stop_words = stopwords.words('english')
		stop_words += ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundred', 'thousand', 'and']
		stop_words += ['network', 'install', 'run', 'file', 'use', 'result', 'paper', 'python', 'using', 'code', 'model', 'train', 'implementation', 'use']
		stop_words += ['data', 'dataset', 'example', 'build', 'learn', 'download', 'obj']
		return [word for word in text if word not in stop_words]
		
	def remove_codeblocks(self, text):
		return re.sub('```.*?```', ' ', text)

	def remove_punctuation(self, text):
		res = re.sub(r'[^\w\s]|\_', ' ', text)
		return res

	def remove_non_ascii(self, words):
		"""Remove non-ASCII characters from list of tokenized words"""
		new_words = []
		for word in words:
			new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
			new_words.append(new_word)
		return new_words

	def replace_numbers(self, words):
		"""Replace all interger occurrences in list of tokenized words with textual representation"""
		p = inflect.engine()
		new_words = []
		for word in words:
			if word.isdigit():
				new_word = p.number_to_words(word)
				new_words += new_word.split(' ')
			else:
				new_words.append(word)
		return new_words

	def stemming(self, text, porter_stemmer):
		stem_text = [porter_stemmer.stem(word) for word in text]
		return stem_text

	def stem_words(self, words):
		"""Stem words in list of tokenized words"""
		stemmer = LancasterStemmer()
		stems = []
		for word in words:
			stem = stemmer.stem(word)
			stems.append(stem)
		return stems
	
	def lemmatizer(self, text):
		wordnet_lemmatizer = WordNetLemmatizer()
		lemm_text = [wordnet_lemmatizer.lemmatize(word, pos='n') for word in text if word != '']
		return lemm_text
	
	def lemmatize_verbs(self, words):
		"""Lemmatize verbs in list of tokenized words"""
		lemmatizer = WordNetLemmatizer()
		lemmas = []
		for word in words:
			lemma = lemmatizer.lemmatize(word, pos='v')
			lemmas.append(lemma)
		return lemmas

	def lemmatize_nouns(self, words):
		"""Lemmatize verbs in list of tokenized words"""
		lemmatizer = WordNetLemmatizer()
		lemmas = []
		for word in words:
			lemma = lemmatizer.lemmatize(word, pos='n')
			lemmas.append(lemma)
		return lemmas

	def lemmatize_adjectives(self, words):
		"""Lemmatize verbs in list of tokenized words"""
		lemmatizer = WordNetLemmatizer()
		lemmas = []
		for word in words:
			lemma = lemmatizer.lemmatize(word, pos='a')
			lemmas.append(lemma)
		return lemmas

	def remove_one_char_and_number_words(self, text):
		res = [word for word in text if word.isdigit() == False and len(word) > 2]
		return res

	def remove_links(self, text):
		regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
		return (re.sub(regex, '', text))

	def remove_links2(self, text):
		return ' '.join([token for token in text.split(' ') if 'http' not in token])

	def get_keys(self,text, l):
		dict1 = {}
		for eachStr in text:
			if eachStr in dict1.keys():
				count = dict1[eachStr]
				count = count + 1
				dict1[eachStr.lower()] = count
			else: dict1[eachStr.lower()] = 1
		remekys = []
		for key in dict1:
			if dict1[key] < l or len(key) <= 2:
				remekys.append(key)
		for key in remekys:
			del dict1[key]
		return ' '.join(list(dict1.keys()))

	def run(self):
		NEWCOLNAME = TEXT
		self.data[NEWCOLNAME]= self.data[TEXT].apply(lambda x: x)

		pipeline = {
			'remove codeblocks': lambda x: self.remove_codeblocks(x),
			'remove links': lambda x : self.remove_links2(x),
			'remove tags': lambda x : self.denoise_text(x),
			'remove punctuations': lambda x: self.remove_punctuation(x),
			'transform to lowercase': lambda x: x.lower(),
			#'replace numbers': lambda x : self.replace_numbers(word_tokenize(x)),
			'remove non-ascii characters': lambda x : self.remove_non_ascii(word_tokenize(x)),
			'lemmatize verbs': lambda x : self.lemmatize_verbs(x),
			'lemmatize nouns': lambda x : self.lemmatize_nouns(x),
			'lemmatize adjectives': lambda x : self.lemmatize_adjectives(x),
			'remove stop_words': lambda x : self.remove_stop_words(x),
			'remove tokens only containing numbers or two char': lambda x : self.remove_one_char_and_number_words(x),
			#'keep only common words': lambda x : self.keep_only_common(x),
			#'stemming': lambda x: self.stemming(x, PorterStemmer()),
			'join tokens': lambda x: ' '.join(x),
		}

		i = 0
		for key, val in pipeline.items():
			i += 1
			self.data[NEWCOLNAME] = self.data[NEWCOLNAME].apply(val)

		#Drop empty rows
		self.data.drop(self.data[self.data[NEWCOLNAME] == np.nan].index, inplace=True)
		self.data.drop(self.data[self.data[NEWCOLNAME] == ''].index, inplace=True)
