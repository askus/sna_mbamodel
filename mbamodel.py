
import networkx as nx

from networkx.algorithms.distance_measures import diameter
from random import choice
from networkx.generators.classic import complete_graph
from networkx.algorithms.cluster import average_clustering
from networkx.algorithms.mixing import degree_assortativity 
from networkx.algorithms.components.connected import connected_components 
class MBAModel:
	_network= None
	_round = None
	_max_nid = None
	_nodes_start = None 
	_nodes_end = None
	_m = None
	def init(self, m_0, m ):
		self._round = 0
		self._network  = complete_graph( m_0 )
		self._max_nid = m_0
		self._nodes_start = dict()
		self._nodes_end = dict()
		self._m = m 

		for v in self._network.nodes() :
			self._nodes_start[ v] =  self._round;
		self._round += 1

	def birth(self ):
		new_v = self._max_nid 
		self._max_nid += 1

		self._network.add_node( new_v )
		self._nodes_start[ new_v ] = self._round 

		linked_candidates = set( )

		#prepare choice list
		l = list()
		for v in self._network.nodes():
			for i in range( self._network.degree( v ) ):
				l.append( v )

		while len( linked_candidates ) < self._m :
			linked_candidates.append( choice( l ) ) 
		for old_v in linked_candidates:
			self.add_edge( new_v , old_v ) 

		self._round += 1 

	def death(self ):
		deleted_v =  choice( self._network.nodes )
		self._network.remove_node( deleted_v )
		self._nodes_end[ deleted_v ] = self._round 

	def node_edge(self ): # return # of nodes and # of edges
		return ( self._network.number_of_nodes()  , self._network.number_of_edges() )
	def diameter(self ):
		return diameter( self._network )
	def deg_dist():
		ret =dist()
		for v in self._network.nodes():
			deg=  self._network.degree( v )
			if not ret.has_key( deg ) :
				ret[ deg ] = 0
			ret[ deg ] +=1 
		return ret 
	def cc(self ):
		return average_clustering( self._network ) 
	def assortativity(self ):
		return degree_assortativity( self._network )
	def gcc_ratio(self ):
		cc_sizes = list()
		for cc in connected_components( self._network ):
			cc_sizes.append( len( cc) ) 
		return  float( max( cc_sizes ) )/ float( self._network.number_of_nodes() )
	def age_dist(self):
		ret = dict()
		for v in self._nodes_start:
			start_time = self._nodes_start[ v ] 
			if self._nodes_end.has_key( v ):
				end_time = self._nodes_end[v] 
			else:
				end_time = self._round 

			age = end_time - start_time 
			if not ret.has_key( age ) :
				ret[age] = 0
			ret[age] +=1 
		return ret 
			
