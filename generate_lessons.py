#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sheets_quickstart]
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import codecs, configparser, json

configParser = configparser.RawConfigParser()   
configFilePath = r'config.ini'
configParser.read(configFilePath)

SCOPES = configParser.get('generate_lessons', 'SCOPES')
SPREADSHEET_ID = configParser.get('generate_lessons', 'SPREADSHEET_ID')
RANGE_NAME = configParser.get('generate_lessons', 'RANGE_NAME')
lesson_dir = configParser.get('generate_lessons', 'lesson_dir')


A = 0
B = 1
C = 2
D = 3
E = 4
F = 5

try:
    # Python 2
    xrange
except NameError:
    # Python 3, xrange is now named range
    xrange = range

def iterateWords(values, row_current, rows_count):
	wordListStarted = False
	wordPairs = []
	for row_id in xrange(row_current, rows_count):
		row = values[row_id]
		if not wordListStarted and len(row) > B and row[B]:
			wordListStarted = True
		if wordListStarted:
			if len(row) > B and row[B]:
				wordPairs.append({u"en": row[B], u"ru": row[C]})
			else:
				break
	return wordPairs

def exportIndex(title, index):
	filename = lesson_dir + 'index.json'
	with codecs.open('{}'.format(filename), 'w', encoding="utf-8") as outfile:
		obj = {
			u"title": title,
			u"lessons": index,
		}
		json.dump(obj, outfile, ensure_ascii=False, indent=4)

def exportLesson(title, lessonId, lessonTitle, schemes):
	filename = lesson_dir + lessonId + '.json'
	with codecs.open('{}'.format(filename), 'w', encoding="utf-8") as outfile:
		obj = {
			u"lesson": title,
			u"title": lessonTitle,
			u"schemes": schemes,
		}
		json.dump(obj, outfile, ensure_ascii=False, indent=4)

def iterateRows(values):
	title = values[0][D]
	seekLessonId = True
	seekLessonSubtitle = False
	seekSchemes = False
	index = []
	rows_count = len(values)
	for row_id in xrange(1, rows_count):
		row = values[row_id]
		if seekLessonId and len(row) > A and row[A]:
			schemes = []
			lessonId = row[A]
			lessonTitle = row[D]
			index.append({u"id": lessonId, u"title": lessonTitle})
			seekLessonId = False
			seekLessonSubtitle = True
			continue
		elif seekLessonSubtitle and len(row) > D and row[D]:
			schemePairs = []
			lessonSubitle = row[D]
			seekLessonSubtitle = False
			seekSchemes = True
			dictionaryPairs = iterateWords(values, row_id, rows_count)
			schemes.append({u"title": lessonSubitle, u"words": dictionaryPairs})
			if len(row) > E and row[E]:
				schemeId = row[E]
		if seekSchemes:
			if len(row) > F and row[F]:
				schemePairs.append({u"en": row[E], u"ru": row[F]})
			elif len(row) > E and row[E]:
				schemes.append({u"title": lessonSubitle, u"words": schemePairs})
				schemePairs = []
				if row[D]:
					lessonSubitle = row[D]
				schemeId = row[E]
			if row_id == rows_count - 1 or len(values[row_id+1]) == D + 1 and not values[row_id+1][C]:
				schemes.append({u"title": lessonSubitle, u"words": schemePairs})
				exportLesson(title, lessonId, lessonTitle, schemes)
				seekSchemes = False
				seekLessonId = True
	exportIndex(title, index)

def main():
	"""Shows basic usage of the Sheets API.
	Prints values from a sample spreadsheet.
	"""
	# The file token.json stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	store = file.Storage('token.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))

	# Call the Sheets API
	sheet = service.spreadsheets()
	result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
								range=RANGE_NAME).execute()
	values = result.get('values', [])

	if not values:
		print('No data found.')
	else:
		iterateRows(values)
	print('Lessons generated in: ' + lesson_dir )

if __name__ == '__main__':
	main()
# [END sheets_quickstart]
