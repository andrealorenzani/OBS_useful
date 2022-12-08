#!/usr/bin/env python3

class TarotsUI():
	
	def __init__(self):
		""" Create a new object """
		print("Init")
		self.cards = None
		self.celtic_group = ['Significator', 'First', 'Second', 'Third', 'Fourth', 'Fifth', 'Sixth', 'Seventh', 'Eight', 'Nineth', 'Tenth']
		self.fewcards_group = ['Past', 'Present', 'Future', 'Jolly']
	
	def generateUI(self):
		import PySimpleGUI as sg
		
		layout = [self.generateLayout()]
		self.window = sg.Window(title="Hello World", layout=layout, margins=(150,50), return_keyboard_events=True)
		
		while True:
			event, values = self.window.read()
			print(event)
			# End program if user closes window or
			# presses the OK button
			if event == "OK" or event == sg.WIN_CLOSED:
				break
			if event.startswith('-CLEAR-'):
				cards = []
				self.window["FullResult"].update('')
				if event == '-CLEAR-celtic':
					cards = self.celtic_group
				if event == '-CLEAR-3Cards':
					cards = self.fewcards_group
				for cardT in cards:
					print("Cleaning "+cardT)
					self.window['-SEL-'+cardT+'-CARD-'].update('')
					self.window['-REV-'+cardT+'-CARD-'].update(False)
					self.window[cardT].update('')
			if event.startswith('-GO-'):
				cards=[]
				self.window["FullResult"].update('')
				if event == '-GO-celtic':
					cards = self.celtic_group
				if event == '-GO-3Cards':
					cards = self.fewcards_group
				for cardT in cards:
					self.checkCards(cardT, values)
				import random
				random.shuffle(values['all_cards'])
				for cardT in cards:
					self.fillCards(cardT, values)
				self.window["FullResult"].update(values['FullResult'])
					
		self.window.close()
		
	def generateLayout(self):
		import PySimpleGUI as sg
		return [
			sg.TabGroup([
				[sg.Tab("Celtic mode", self.__genTab__(self.celtic_group, "celtic")),
				 sg.Tab("3 cards mode", self.__genTab__(self.fewcards_group, "3Cards")),
				 sg.Tab("Result", [[sg.Multiline('', key="FullResult", disabled=True, size=(90,25))]])]
			])
		]
	
	def checkCards(self, card, values):
		value = values["-SEL-"+card+"-CARD-"]
		checked = values['-REV-'+card+'-CARD-']
		currentCards = list(self.readCards()['dritte'].keys())
		if value.strip().startswith('(') and value.strip().endswith(')'):
			value = value[1:-1]
			checked = True
		if self.readCards()['dritte'].get(value) is not None:
			self.window["-SEL-"+card+"-CARD-"].update(value)
			values["-SEL-"+card+"-CARD-"] = value
			self.window['-REV-'+card+'-CARD-'].update(checked)
			values['-REV-'+card+'-CARD-'] = checked
			currentCards.remove(value)
		else:
			self.window["-SEL-"+card+"-CARD-"].update('')
			values["-SEL-"+card+"-CARD-"] = ''
		values['all_cards'] = currentCards
		
	def fillCards(self, card, values):
		if values["-SEL-"+card+"-CARD-"] == '':
			print(values)
			value = values['all_cards'].pop()
			values["-SEL-"+card+"-CARD-"] = value
			self.window["-SEL-"+card+"-CARD-"].update(value)
			import random
			if random.randint(1, 100) < 21:
				values["-REV-"+card+"-CARD-"] = True
				self.window["-REV-"+card+"-CARD-"].update(True)
		msg = ""
		if values["-REV-"+card+"-CARD-"]:
			msg = self.cards['desc'].get(card.lower()) + self.cards['rovesce'].get(values["-SEL-"+card+"-CARD-"])
		else:
			msg = self.cards['desc'].get(card.lower()) + self.cards['dritte'].get(values["-SEL-"+card+"-CARD-"])
		self.window[card].update(msg)
		values['FullResult'] += msg+"\n\t"
		
		
			
	def __genTab__(self, card_group, tab):
		cards = list(self.readCards()['dritte'].keys())
		import PySimpleGUI as sg
		return [[
			sg.Column([
			[
				sg.Text(card, size=(14, 1)),
				sg.Combo(cards, key='-SEL-'+card+'-CARD-'),
				sg.Checkbox("", key='-REV-'+card+'-CARD-'),
				sg.InputText(readonly=True, key=card, do_not_clear=True)
			]
			for card in card_group
		])],
		[
			sg.Button('GO!!!', key="-GO-" + tab), sg.Button('Clear', key="-CLEAR-"+tab )
		]]
				
			
		
	def readCards(self):
		if self.cards is not None:
			return self.cards
		from configparser import ConfigParser
		config = ConfigParser()
		config.read('tarots.properties')
			
		self.cards = {
			"dritte": {x:y for (x,y) in config.items('Dritte')},
			"rovesce": {x:y for (x,y) in config.items('Rovesciate')},
			"desc": {x:y for (x,y) in config.items('Carte')}
		}
		return self.cards


if __name__ == "__main__": 
	
	tarotsUI = TarotsUI()
	tarotsUI.generateUI()