import sys
import pickle as p
import numpy as np
import networkx as nx
output_events = {}
event_log = {}
output_interactions = []
theme_path_info = {}
cause_path_info = {}
interaction_info = {}
entity_info = {}

Gene_expression = "Gene_expression"
Transcription = "Transcription"
Protein_catabolism = "Protein_catabolism"
Phosphorylation = "Phosphorylation"
Localization = "Localization"
Binding = "Binding"
Regulation = "Regulation"
Positive_regulation = "Positive_regulation"
Negative_regulation = "Negative_regulation"

interaction_type_label = {Gene_expression:1, Transcription:2, Protein_catabolism:3, Phosphorylation:4, Localization:5, Binding:6, Regulation:7, Positive_regulation:8, Negative_regulation:9}

class Entity:
	def __init__(self, id, type, term, start_index, end_index, nx_node=None):
		if id:
			self.id = id
		else:
			self.id = self.__generate_id()
		self.type = type
		self.term = term
		self.start_index = start_index
		self.end_index = end_index
		self.nx_node = nx_node

	def __generate_id(self):
		last_entity_id = int(entities[-1].id[1:])
		last_interaction_id = int(interactions[-1].id[1:])
		return "T"+str(max(last_entity_id, last_interaction_id)+1)

	def get_display_string(self):
		return self.id+"\t"+self.type+" "+str(self.start_index)+" "+str(self.end_index)+"\t"+self.term

class Event:
	def __init__(self, interaction_id=None, interaction_type=None, theme_id=None, cause_id=None):
		self.id = self.__generate_id()
		self.interaction_id = interaction_id
		self.interaction_type = interaction_type
		self.theme_id = theme_id
		self.cause_id = cause_id

	def __generate_id(self):
		#return "E"+str(int(output_events[-1].id[1:])+1)
		return "E"+str(len(output_events.keys())+1)

	def get_display_string(self):
		display_string = self.id+"\t" +self.interaction_type+":"+self.interaction_id
		if self.theme_id:
			display_string += " " +"Theme:"+self.theme_id
		if self.cause_id:
			if self.interaction_type == "Phosphorylation":
				#pass
				display_string += " " +"Cause:"+self.cause_id
			elif self.interaction_type == "Localization":
				#pass
				display_string += " " +"ToLoc:"+self.cause_id
			elif self.interaction_type == "Binding":
				display_string += " " +"Theme2:"+self.cause_id
			else:
				display_string += " " +"Cause:"+self.cause_id
		return display_string

class Interaction:
	def __init__(self, type, term=None, start_index=None, end_index=None):
		self.id = self.__generate_id()
		self.type = type
		self.term = term
		self.start_index = start_index
		self.end_index = end_index

	def __generate_id(self):
		if not interactions:
			if not entities:
				return "T1"
			else:
				return "T"+str(int(entities[-1].id[1:])+1)
		else:
			if not entities:
				last_entity_id = 0
			else:
				last_entity_id = int(entities[-1].id[1:])
			last_interaction_id = int(interactions[-1].id[1:])
			return "T"+str(max(last_entity_id, last_interaction_id)+1)

	def get_display_string(self):
		return self.id+"\t"+self.type+" "+str(self.start_index)+" "+str(self.end_index)+"\t"+self.term

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: python get_events_from_label_v3.py data_output_interactions.p data_output_theme_events.p  data_cause_labels.p data_cause_event_info.p amr_nx_graphs.p output_a2_file"
		sys.exit(0)
	data_output_interactions = p.load(open(sys.argv[1], 'rb'))
	data_theme_output_events = p.load(open(sys.argv[2], 'rb'))
	data_cause_labels = p.load(open(sys.argv[3], 'rb'))
	data_cause_event_info = p.load(open(sys.argv[4], 'rb'))
	amr_nx_graphs = p.load(open(sys.argv[5], 'rb'))
	output_a2_file = open(sys.argv[6], 'w')
	for i in range(len(data_cause_event_info)):
		if data_cause_labels[i] == 0:
			continue
		[amr_id, interaction, theme, cause, theme_event_id] = data_cause_event_info[i]
		if not data_theme_output_events.has_key(theme_event_id):
			print "MISMATCH between theme events"
			continue
		event = data_theme_output_events[theme_event_id]
		event.cause_id = cause.id
		data_theme_output_events[theme_event_id] = event	
	
	for interaction in data_output_interactions:
		output_a2_file.write(interaction.get_display_string()+"\n")

	for event in data_theme_output_events.values():
		output_a2_file.write(event.get_display_string()+"\n")

