import sys
import networkx as nx

from networkx.algorithms.shortest_paths.generic import average_shortest_path_length
from networkx.algorithms.distance_measures import diameter
from random import choice
from networkx.generators.classic import complete_graph
from networkx.algorithms.cluster import average_clustering
from networkx.algorithms.mixing import degree_assortativity 
from networkx.algorithms.components.connected import connected_components 
from networkx.algorithms.components.connected import connected_component_subgraphs

class MBAModel:
	_network= None
	_round = None
	_max_nid = None
	_nodes_start = None 
	_nodes_end = None
	_m = None
	_max_num = None
	_choice_list = None

	def __init__(self, m_0, m , max_num ):
		self._round = 0
		self._network  = complete_graph( m_0 )
		self._max_nid = m_0
		self._nodes_start = dict()
		self._nodes_end = dict()
		self._m = m 
		self._max_num = max_num

		self._choice_list = list() 
		for v in self._network.nodes() :
			self._nodes_start[ v] =  self._round
			for i in range( self._network.degree( v )):
				self._choice_list.append( v ) 

		self._round += 1

		

	def size(self):
		return self._network.number_of_nodes() 
	def next( self ):
		if self.size() >= self._max_num:
			print "It's Full"
			return False 
			
		self.birth()
		if self._round % 4 :
			self.death()
		return True

	def birth(self ):
		new_v = self._max_nid 
		self._max_nid += 1

		self._network.add_node( new_v )
		self._nodes_start[ new_v ] = self._round 

		linked_candidates = set( )

		while len( linked_candidates ) < self._m :
			linked_candidates.add( choice( self._choice_list ) ) 
		for old_v in linked_candidates:
			self._network.add_edge( new_v , old_v ) 
			# update choice list
			self._choice_list.append( old_v )
			self._choice_list.append( new_v )
		self._round += 1 

	def death(self ):
		deleted_v =  choice( self._network.nodes() )

		# update choice list 
		for nei in self._network.neighbors( deleted_v ):
			self._choice_list.remove( nei )

		self._network.remove_node( deleted_v )
		self._nodes_end[ deleted_v ] = self._round 
	
		while True:
			try:
		# update choice list 
				self._choice_list.remove( deleted_v )
			except:
				break

	def number_of_nodes( self ):
		return self._network.number_of_nodes()
	def number_of_edges( self ):
		return  self._network.number_of_edges() 
	def diameter(self ):
		try:
			return diameter( self._network )
		except:
			components = connected_component_subgraphs( self._network)
			biggest_c = None
			for c in components:
				if biggest_c == None:
					biggest_c = c 
					continue
				if( len( biggest_c) < len( c ) ) : 
					biggest_c = c 
					continue
			return diameter( biggest_c )
	def average_shortest_path_length( self ):
		return average_shortest_path_length( self._network)
		
	def deg_dist(self ):
		ret =dict()
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
	def gcc_size( self ):
		cc_sizes = list()
		for cc in connected_components( self._network ):
			cc_sizes.append( len(cc))
		return max( cc_sizes )
	def age_dist(self ):
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
	def remain_age_dist( self):
		ret = dict()
		for v in self._network.nodes() :
			start_time = self._nodes_start[v ]
			end_time = self._round
			age = end_time - start_time 
			if not ret.has_key(age ) :
				ret[ age] = 0
			ret[age] +=1 
		return ret 
			
def print_dist(   output_file, dist ):
	outf = open( output_file , "w") 
	for k in sorted( dist.keys() ):
		value = dist[k] 
		print >> outf , "%d\t%d" %( k , value )
	outf.close()

def main( argv ) :
	m_0 = int( argv[1] )
	m = int( argv[2] ) 
	max_num = int( argv[3] ) 
	output_dir = argv[4]

	model = MBAModel( m_0, m , max_num )
	isNext= True

	basic_outf = open( "%s/basic.txt" % output_dir, "w" )
	print >> basic_outf ,"round\tnodes\tedges\tdiameter\tavg_shortest_path\tcc\tassortativity\tgcc_ratio\tgcc_size"

	i =0 
	while isNext:
		isNext = model.next() 
		if i % 10 == 0  :
			line = "%d\t%d\t%d\t-\t-\t%.4f\t%.4f\t%.4f\t%d" %( i , model.number_of_nodes(), model.number_of_edges() ,  model.cc(), model.assortativity(), model.gcc_ratio() , model.gcc_size() )
			if i % 1000 == 0 :
				line = "%d\t%d\t%d\t%.4f\t-\t%.4f\t%.4f\t%.4f\t%d" %( i , model.number_of_nodes(), model.number_of_edges() ,  model.diameter(),  model.cc(), model.assortativity(), model.gcc_ratio() , model.gcc_size() )

			if i % 10001 == 0:
				line = "%d\t%d\t%d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%d" %( i , model.number_of_nodes(), model.number_of_edges() ,  model.diameter(),  model.average_shortest_path_length(), model.cc(), model.assortativity(), model.gcc_ratio() , model.gcc_size() )

			print >>basic_outf , line 
			print line
		
		if model.size() == max_num / 8  :
			print_dist( "%s/%d.deg_dist.txt" %( output_dir, model.size() ) , model.deg_dist() ) 
		elif model.size() == max_num /4:
			print_dist( "%s/%d.deg_dist.txt" %( output_dir, model.size() ) , model.deg_dist() ) 
		elif model.size() == max_num /2 :
			print_dist( "%s/%d.deg_dist.txt" %( output_dir, model.size() ) , model.deg_dist() ) 
		elif model.size() == max_num :
			print_dist( "%s/%d.deg_dist.txt" %( output_dir, model.size() ) , model.deg_dist() ) 
			print_dist( "%s/%d.life_time_dist.txt" %( output_dir, model.size() ) , model.age_dist() ) 
			print_dist( "%s/%d.remain.age_dist.txt"  %( output_dir, model.size() ) , model.remain_age_dist() )
		i+=1 
	basic_outf.close()
if __name__ == "__main__":
	main( sys.argv )
