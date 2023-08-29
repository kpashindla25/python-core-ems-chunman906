from abc import ABC, abstractmethod
import os
from datetime import datetime


class Event:
	def __init__(self, event_id, event_name, location, event_date, allow_parking):
		self.event_id = event_id
		self.event_name = event_name
		self.location = location
		self.event_date = event_date
		self.allow_parking = allow_parking

	@property
	def event_date(self):
		return self.__event_date.strftime("%d-%m-%Y")

	@event_date.setter
	def event_date(self, event_date):
		format_date = datetime.strptime(event_date, "%d-%m-%Y")
		self.__event_date = format_date

	def display(self):
		print(f'The event is <{self.event_name}> which will be held at {self.location} on {self.event_date}.')
		print('The event provide car parking.') if self.allow_parking else print('The event will have no car parking place.')

	def edit_details(self):
		choice = input('Do you want to change the details of the name / location / date / car parking for the event? ').strip().lower()
		while True:
			if choice == 'name':
				self.event_name = str(input('what is the new name for the event? '))
			elif choice == 'location':
				self.location = str(input('what is the new location for the event? '))
			elif choice == 'date':
				try:
					self.event_date = input('what is the new date for the event? ')
				except ValueError:
					print("Invalid date format. Expected DD-MM-YYYY")
					continue
			elif choice == 'carparking' or choice == 'car parking':
				try:
					self.allow_parking = check_boolean(input('Is it allow parking now? type: True/ False '))
				except ValueError as err:
					print(err)
					continue
			else:
				print('You have incorrect input! Please try again! ')
				break
			print('you have changed the details successfully!')
			break


# Abstract class
class Attendee(ABC):
	def __init__(self, att_id, name, gender, age, email):
		self.att_id = att_id
		self.name = name
		self.gender = gender
		self.age = age
		self.email = email

	@abstractmethod
	def display(self):
		pass


# Implementation class
class Adult(Attendee):
	def __init__(self, att_id, name, gender, age, email, have_car):
		super().__init__(att_id, name, gender, age, email)
		self.have_car = have_car

	def display(self):
		print(f'The adult attendee is {self.name}, Gender: {self.gender}, Age: {self.age}, Email: {self.email}, have car: {self.have_car}')


class Children(Attendee):
	def __init__(self, att_id, name, gender, age, email, free_entry):
		super().__init__(att_id, name, gender, age, email)
		self.free_entry = free_entry

	def display(self):
		print(f'The children attendee is {self.name}, Gender: {self.gender}, Age: {self.age}, Email: {self.email}, Free entry: {self.free_entry}')


# use for exit the nested loop in any class method by (Try, Except)
class ExitNestedLoop(Exception):
	pass


# Abstract class
class System(ABC):
	def __init__(self, file):
		self.file = file

	@abstractmethod
	def save_file(self):
		pass

	@abstractmethod
	def load_file(self):
		pass


class EventSystem(System):
	def __init__(self, file):
		super().__init__(file)
		self.event_list = []
		self.event_id = 0
		self.load_file()

# add event into the list
	def add_event(self, event):
		self.event_list.append(event)

	def create_event(self):
		print('You are now creating event in the system ... ')
		while True:
			event_name = str(input('Enter the event name: '))
			location = str(input('Where is the location to hold the event? '))
			event_date = input('When is the event date? ')
			allow_parking = input('Is there car parking available? Input True or False: ')
			try:
				allow_parking = check_boolean(allow_parking)
			except ValueError as err:
				print(err)
				continue
			self.event_id += 1
			event = Event(self.event_id, event_name, location, event_date, allow_parking)
			self.event_list.append(event)
			print(f'You have created <{event_name}> event at {location} on {event_date} in the system.')
			break

# list all the event in the system
	def list_events(self):
		print('The list of events are as follow: ')
		self.event_list.sort(key=lambda e_event: e_event.event_id)
		for each_event in self.event_list:
			print(f'Event ID: {each_event.event_id} - {each_event.event_name}, {each_event.location}')

# List an individual event
	def show_event(self):
		self.list_events()
		choice = int(input('Which event do you want to check further details? Input the event ID number: \n'))
		if choice <= len(self.event_list):
			return self.event_list[choice-1].display()
		else:
			print('You have input a wrong selection number')

# Edit an Event
	def edit_event(self):
		choice = int(input('Which event do you want to edit the details? Input the event ID number: '))
		if choice <= len(self.event_list):
			self.event_list[choice - 1].edit_details()
		else:
			print('You have input a wrong selection number')

# Delete event from the list
	def remove_event(self):
		choice = int(input('Which event do you want to delete? Input the event ID number: '))
		if choice <= len(self.event_list):
			self.event_list.pop(choice-1)
			print('You have already deleted the event. ')
			self.list_events()
		else:
			print('You have input a wrong selection number')

# Save event data by File handling
	def save_file(self):
		try:
			with open(self.file, 'w') as file:
				try:
					for each_event in self.event_list:
						file.write(f'{each_event.event_name},{each_event.location},{each_event.event_date},{each_event.allow_parking}\n')
				finally:
					file.close()
		except Exception as err:
			print(err)
		else:
			print('Goodbye. <event> data has been saved on txt file. ')

# Load event data by File handling
	def load_file(self):
		try:
			if os.path.exists("event.txt"):
				with open(self.file, 'r') as file:
					line = file.readlines()
					for each_line in line:
						event_name, location, event_date, allow_parking = each_line.strip().split(',')
						self.event_id += 1
						self.event_list.append(Event(self.event_id, event_name, location, event_date, check_boolean(allow_parking)))
		except Exception as err:
			print(err)
		finally:
			file.close()


class AttendeeSystem(System):
	def __init__(self, file):
		super().__init__(file)
		self.attendee_list = {}
		self.att_id = 0
		self.load_file()

	def check_age(self, age):
		if isinstance(age, int):
			return age
		else:
			raise ValueError('Expected the age is integer value! Try again.')

# Add attendees into the event
	def add(self, attendee):
		self.attendee_list = attendee

	def create_attendee(self):
		while True:
			event_id = str(input('Which event are you attending? input Event ID: '))
			name = str(input('What is the name of the attendee? '))
			gender = str(input('What is the gender of the attendee? M / F : '))
			email = str(input('What is the contact email? '))
			try:
				age = int(input(('What is the age? ')))
				# age = self.check_age(int(input(('What is the age? ')))
			except ValueError:
				print('Expected the age is integer value! Try again.')
				continue
			self.att_id += 1
			if age >= 18:
				try:
					have_car = check_boolean(input('Would you drive a car to attend? True / False: '))
				except ValueError as err:
					print(err)
					continue
				a_att_id = self.att_id
				attendee_adult = Adult(a_att_id, name, gender, age, email, have_car)
				attendee_adult.display()
				if event_id in self.attendee_list:
					self.attendee_list[event_id].append(attendee_adult)
				else:
					a_list = [attendee_adult]
					self.attendee_list[event_id] = a_list
				break
			else:
				free_entry = True if age < 12 else False
				c_att_id = self.att_id
				attendee_child = Children(c_att_id, name, gender, age, email, free_entry)
				attendee_child.display()
				if event_id in self.attendee_list:
					self.attendee_list[event_id].append(attendee_child)
				else:
					c_list = [attendee_child]
					self.attendee_list[event_id] = c_list
				break
		print('You have added the attendee successfully. ')

# list the attendees attending an event
	def list_attendee(self):
		for event, attendees in self.attendee_list.items():
			for attendee in attendees:
				print(f'Event ID: {event} - Attendee ID: {attendee.att_id} Attendee Name: {attendee.name}, Gender: {attendee.gender}, Age: {attendee.age}, Email: {attendee.email}')

# Delete attendee from an event.
# Used Exception to handle nested loop break.
	def delete_attendee(self):
		choice = int(input('Who do you want do delete from the system? type the Attendee ID:  '))
		try:
			for event, attendees in self.attendee_list.items():
				for attendee in attendees:
					if attendee.att_id == choice:
						attendees.remove(attendee)
						print(f'you have removed <{attendee.name}> successfully.')
						raise ExitNestedLoop
		except ExitNestedLoop:
			pass
		else:
			print('wrong input! please enter the attendee ID correctly.')

# Save attendee data by File handling
	def save_file(self):
		try:
			with open(self.file, 'w') as file:
				try:
					for event, attendees in self.attendee_list.items():
						for attendee in attendees:
							if isinstance(attendee, Adult):
								file.write(
									f'{event},{attendee.name},{attendee.gender},{attendee.age},{attendee.email},{attendee.have_car}\n')
							else:
								file.write(
									f'{event},{attendee.name},{attendee.gender},{attendee.age},{attendee.email},{attendee.free_entry}\n')
				finally:
					file.close()
		except Exception as err:
			print(err)
		else:
			print('Goodbye. <attendee> data has been saved on txt file. ')

	def load_file(self):
		try:
			if os.path.exists("attendee.txt"):
				with open(self.file, 'r') as file:
					line = file.readlines()
					for each_line in line:
						event, name, gender, age, email, bool_var = each_line.strip().split(',')
						age_int = int(age)
						self.att_id += 1
						try:
							if age_int >= 18:
								att_obj = Adult(self.att_id, name, gender, age_int, email, bool_var)
							else:
								att_obj = Children(self.att_id, name, gender, age_int, email, bool_var)
						finally:
							if event in self.attendee_list:
								self.attendee_list[event].append(att_obj)
							else:
								att_list = [att_obj]
								self.attendee_list[event] = att_list
		except Exception as err:
			print(err)
		finally:
			file.close()


# Master control panel
class Router:
	def __init__(self):
		self.running = True
		self.eventsystem = EventSystem('event.txt')
		self.attendeesystem = AttendeeSystem('attendee.txt')

	def run(self):
		self.logo()
		self.command_view()
		while self.running:
			choice = input('Please input the instruction of what you need to do. Type the number for above option: \n')
			if choice == '1':
				self.eventsystem.list_events()
			elif choice == '2':
				self.eventsystem.show_event()
			elif choice == '3':
				self.eventsystem.create_event()
			elif choice == '4':
				self.eventsystem.edit_event()
			elif choice == '5':
				self.eventsystem.remove_event()
			elif choice == '6':
				self.attendeesystem.list_attendee()
			elif choice == '7':
				self.attendeesystem.create_attendee()
			elif choice == '8':
				self.attendeesystem.delete_attendee()
			else:
				self.eventsystem.save_file()
				self.attendeesystem.save_file()
				self.running = False

	def logo(self):
		print('------------------------------------------------------------------')
		print(' ')
		print('Welcome to the web application system of event management company.')
		print(' ')
		print('------------------------------------------------------------------')

	def command_view(self):
		print('1. List all the event from the system')
		print('2. List an individual event ')
		print('3. Create an event ')
		print('4. Edit an event details ')
		print('5. Delete an event ')
		print('6. List the attendees attending an event')
		print('7. Add an attendee to an event')
		print('8. Delete an attendee from an event')
		print('<Press any other key to exit the app>')
		print('-------------------------------------------------------------------')


# custom function with Exception handling for any class
def check_boolean(user_input):
	if user_input.lower() == 'true':
		return True
	elif user_input.lower() == 'false':
		return False
	else:
		raise ValueError('Expected boolean value: True / False! ')


# Start the application
app = Router()
app.run()


# Notes:
# Create class Event
# Create class Attendee(abstract), Adult, Children
# use controller(System) - to create functions for read, adding, updating and delete events
# create Event inside attendee

# how to put multiple values into the same key in dictionary? for attendee list
# after that work on delete item

# create router class -> make the program work and link with different functions
# use the file opening to insert initial data & save data -> txt file
# fix the event and attendee ID issue for default input
