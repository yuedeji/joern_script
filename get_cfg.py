import sys
import os
import networkx as nx
from joern.all import JoernSteps

def change_db_folder(db_folder):
    conf_file = '../neo4j-community-2.1.5/conf/neo4j-server.properties'
    cmd = "sed -i '/org.neo4j.server.database.location=/c\org.neo4j.server.database.location=%s' %s" %(db_folder, conf_file)
    print cmd
    os.system(cmd)
#    exit(0)

def start_db(db_folder):
    change_db_folder(db_folder)
    cmd = './joern-start-db'
    print cmd
    os.system(cmd)

def stop_db():
    cmd = './joern-stop-db'
    print cmd
    os.system(cmd)

def connect_db():
    j = JoernSteps()
    j.setGraphDbURL('http://localhost:7474/db/data/')
    j.connectToDatabase()
    return j

class code_cfg:
    def __init__(self, file_node, func_node):
        self.filepath = file_node['filepath']
        self.func_name = func_node['name']
        self.uid = ""
        self.g = nx.DiGraph()
        self.id2code = {}
        self.id2feat = {}

    def bfs(self, source, j):
        level = 0
        queue = []
        queue.append(source)
#    queue = main_nodes
        #print queue
        visited = set()
        index = 0
#        print source
        while len(queue) != 0:
#        print "level,", level
            temp_queue = []
            for cur in queue:
#        while len(queue) != 0:
#            cur = queue[0]
                if cur._id not in visited:
                    if 'isCFGNode' in cur and cur['isCFGNode'] == "True":
# TODO: Print this node
                        print cur
                    #print cur.properties
                    visited.add(cur._id)
                    if cur._id > -1:
                        query = 'g.v('+str(cur._id)+').out'
                        #print query
                        s = j.runGremlinQuery(query)
                        #print len(s)
                        neighbor_vs = []
                        for one in s:
                            neighbor_vs.append(one._id)
#                    print neighbor_vs
#                    print s
                        temp_queue.extend(s)
#            del queue[0]
            queue = temp_queue
#        temp_queue = []
            level = level + 1

        print "Depth,", level
        print

#                    print(cur)
#                    print cur.properties
#                    query = 'g.v('+str(cur._id)+').code'
#                    print j.runGremlinQuery(query)
#                    print(query)
#                    print len(s)
# Mine edges to build AST
#                    query = 'g.v('+str(cur._id)+').outE'
#                    #print query
#                    s = j.runGremlinQuery(query)
#                    print s
#
#                    query = 'g.v('+str(cur._id)+').in'
#                    print query
#                    s = j.runGremlinQuery(query)
#                    print("# of parents", len(s))

def get_func_cfg(file_node, j, func):
    #print func
    g = code_cfg(file_node, func)
    print g.filepath, g.func_name
    g.bfs(func, j)

#    query = 'getAllStatements(%s).astNodes()' %(func._id)
#    func_child_list = j.runGremlinQuery(query)
#    print(func_child_list)
#    exit()

    #query = 'g.v(' + str(func._id) + ').out'
    #func_child_list = j.runGremlinQuery(query)
    #print(func_child_list)
    #for cfg_node in func_child_list:
    #    query = 'g.v(' + str(cfg_node._id) + ').out' #"AST_EDGE")'
    #    cfg_node_list = j.runGremlinQuery(query)
    #    print(cfg_node_list)
    #exit()


def get_content(j, output_folder):
    query = "getFilesByName('*')"
    file_list = j.runGremlinQuery(query)
    print "[+] Number of files:", len(file_list)
    for i in range(len(file_list)):
        cur = file_list[i]
#        print cur
#       print i, results[i], results[i].properties
#    #query = 'g.v(' + str(cur._id) + ').out().{it.type == "Function"}'
        query = 'g.v(' + str(cur._id) + ').out' #().{it.type == "Function"}'
        func_list = j.runGremlinQuery(query)
        index = 0
        for func in func_list:
            index += 1
            if index > 3:
                break
            if func['type'] == 'Function':
                get_func_cfg(cur, j, func)

        break

def main(db_folder, output_folder):

    if not os.path.isdir(db_folder):
        raise Exception('%s does not exist' %(db_folder))
        exit(-1)

#    start_db(db_folder)

    j = connect_db()
    get_content(j, output_folder)

#    stop_db()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Usage: python get_cfg.py <database> <output_folder>"

        exit(0)

    main(sys.argv[1], sys.argv[2])
