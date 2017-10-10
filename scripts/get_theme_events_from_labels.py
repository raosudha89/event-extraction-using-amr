import sys, os
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

def add_theme_event(amr_id, path, interaction_nx_node, entity_nx_node):
	if event_log.has_key((amr_id, interaction_nx_node, entity_nx_node)):
		return event_log[(amr_id, interaction_nx_node, entity_nx_node)]	
	
	#theme_path_info: { amr_id: {interaction_nx_node: [entity_nx_node]}} s.t. there is a an interaction between interaction_nx_node and each of entity_nx_node

	#if interaction_info[amr_id][interaction_nx_node].type not in ["Regulation", "Positive_regulation", "Negative_regulation"]:
	if interaction_info[amr_id][interaction_nx_node].type not in ["Regulation", "Positive_regulation", "Negative_regulation", "Phosphorylation"]:
		e = Event(interaction_id=interaction_info[amr_id][interaction_nx_node].id, interaction_type=interaction_info[amr_id][interaction_nx_node].type, theme_id=entity_info[amr_id][entity_nx_node].id, cause_id=None)
		if interaction_info[amr_id][interaction_nx_node] not in output_interactions:
			output_interactions.append(interaction_info[amr_id][interaction_nx_node])
		output_events[e.id] = e
		event_log[(amr_id, interaction_nx_node, entity_nx_node)] = e.id
		return e.id

	for i in range(1, len(path)-1):
		nx_node = path[i]
		if theme_path_info[amr_id].has_key(nx_node): #nx_node is a interaction node
			if entity.nx_node in theme_path_info[amr_id][nx_node]: #there is a positive interaction with nx_node as interaction and entity.nx_node as entity
				event_id = add_theme_event(amr_id, path[i:], nx_node, entity_nx_node)
				e = Event(interaction_id=interaction_info[amr_id][interaction_nx_node].id, interaction_type=interaction_info[amr_id][interaction_nx_node].type, theme_id=event_id, cause_id=None)
				if interaction_info[amr_id][interaction_nx_node] not in output_interactions:
					output_interactions.append(interaction_info[amr_id][interaction_nx_node])
				output_events[e.id] = e
				event_log[(amr_id, interaction_nx_node, entity_nx_node)] = e.id
				return e.id
	e = Event(interaction_id=interaction_info[amr_id][interaction_nx_node].id, interaction_type=interaction_info[amr_id][interaction_nx_node].type, theme_id=entity_info[amr_id][entity_nx_node].id, cause_id=None)
	if interaction_info[amr_id][interaction_nx_node] not in output_interactions:
		output_interactions.append(interaction_info[amr_id][interaction_nx_node])
	output_events[e.id] = e
	event_log[(amr_id, interaction_nx_node, entity_nx_node)] = e.id
	return e.id

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "usage: python get_events_from_label_v3.py data_theme_labels.p data_theme_event_info.p amr_nx_graphs.p output_a2_file"
		sys.exit(4)
	data_theme_labels = p.load(open(sys.argv[1], 'rb'))
	data_theme_event_info = p.load(open(sys.argv[2], 'rb'))
	amr_nx_graphs = p.load(open(sys.argv[3], 'rb'))
	output_a2_file = open(sys.argv[4], 'w')
	#theme_path_info: { amr_id: {interaction_nx_node: [entity_nx_node]}} s.t. there is a an interaction between interaction_nx_node and each of entity_nx_node
	
	for i in range(len(data_theme_event_info)):
		if data_theme_labels[i] == 0:
			continue
		[amr_id, interaction, entity, org_event] = data_theme_event_info[i]
		for interaction_type, label in interaction_type_label.iteritems():
			if label == data_theme_labels[i]:
				interaction.type = interaction_type
				break 
		data_theme_event_info[i] = [amr_id, interaction, entity, org_event] 
		
		if not theme_path_info.has_key(amr_id):
			theme_path_info[amr_id] = {}
		if interaction.nx_node not in theme_path_info[amr_id].keys():
			theme_path_info[amr_id][interaction.nx_node] = []
		theme_path_info[amr_id][interaction.nx_node].append(entity.nx_node)
		
		if not interaction_info.has_key(amr_id):
			interaction_info[amr_id] = {}
		interaction_info[amr_id][interaction.nx_node] = interaction
		
		if not entity_info.has_key(amr_id):
			entity_info[amr_id] = {}
		entity_info[amr_id][entity.nx_node] = entity

	for i in range(len(data_theme_labels)):
		if data_theme_labels[i] == 0:
			continue
		[amr_id, interaction, entity, org_event] = data_theme_event_info[i]
		[root, amr_nx_graph, sentence] = amr_nx_graphs[amr_id]
		try:
			path = nx.shortest_path(amr_nx_graph.to_undirected(), interaction.nx_node, entity.nx_node)
			add_theme_event(amr_id, path, interaction.nx_node, entity.nx_node)
		except:
			print "Failed a find a path"
			data_theme_labels[i] = 0

	output_events_info = {}
	for i in range(len(data_theme_labels)):
		if data_theme_labels[i] == 0:
			continue
		[amr_id, interaction, entity, org_event] = data_theme_event_info[i]
		event_id = event_log[(amr_id, interaction.nx_node, entity.nx_node)]
		output_events_info[event_id] = (amr_id, interaction, entity, org_event)

	for interaction in output_interactions:
		output_a2_file.write(interaction.get_display_string()+"\n")

	for event in output_events.values():
		output_a2_file.write(event.get_display_string()+"\n")

	output_dir = os.path.dirname(sys.argv[1])
	output_filename = os.path.basename(sys.argv[4]).split('.')[0]
	p.dump(output_interactions, open(os.path.join(output_dir, output_filename+"_output_interactions.p"), 'wb'))
	p.dump(output_events, open(os.path.join(output_dir, output_filename+"_output_theme_events.p"), 'wb'))
	p.dump(output_events_info, open(os.path.join(output_dir, output_filename+"_output_theme_events_info.p"), 'wb'))	
