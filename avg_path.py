from  mbamodel import MBAModel
import sys 

def main( argv ) :
	m_0 = int( argv[1] )
	m = int( argv[2] ) 
	max_num = int( argv[3] )

	model = MBAModel( m , m_0 , max_num )

	while model.size()< 90000 :
		model.next()
	total_avg_path_length = 0.0
	i = 0.0
	while model.size() < 100000:
		if model.size() % 10000 == 0:
			avg_path_l = model.average_shortest_path_length()
			print "model size = %d,  avg path l = %f" %(model.size() ,  avg_path_l )
			total_avg_path_length +=avg_path_l
			i +=1.0

	print "avg path length 90000~100000 = %.4f " %( total_avg_path_length / i ) 
	
if __name__ == "__main__":
	main( sys.argv )
