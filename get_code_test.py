import sys
import os
import csv
import networkx as nx
from joern.all import JoernSteps
from tqdm import tqdm

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

feature_type_list = ['short', 'int', 'long', 'char', 'float', 'double', 'bool', 'const', 'static', '*', 'void', 'unsigned', 'signed', 'struct', 'union', 'enum', 'function', 'constant', 'else']

feature_operator_list = ['+', '-', '*', '/', '%', '^', '=', '|', '&', '||', '&&', '<', '>', '<=', '>=', '==', '!=', '+=', '-=', '*=', '/=', '%=', '^=', '|=', '&=', '<<', '>>', '<<=', '>>=']

feature_keyword_list = ['auto', 'break', 'case', 'continue', 'default', 'do', 'else', 'extern', 'for', 'goto', 'if', 'register', 'return', 'sizeof', 'switch', 'typedef', 'volatile', 'while', 'null', 'eof']

feature_other = ['[', ']', '(', ')', '}', '{', '?', ':', '"', '\'', '.', ',', '->', ';']
#others: library function: malloc, memcpy

feature_list_exact = feature_type_list + feature_keyword_list
feature_list_approx = feature_operator_list + feature_other
feature_list = feature_list_exact + feature_list_approx

class code_cfg:
    def __init__(self, file_node, func_node):
        self.filepath = file_node['filepath']
        self.func_name = func_node['name']
        self.uid = ""
        self.g = nx.DiGraph()
        self.id2code = {}
        self.id2feat = {}
        self.id2type = {}
        self.gremlin2id = {}

# Add node to cfg graph
    def add_node(self, index, code_node):
        self.g.add_node(index)
        self.id2code[index] = code_node['code']
        self.id2type[index] = code_node['type']
        self.gremlin2id[code_node._id] = index

    def add_edge(self, parent, child):
        parent_id = self.gremlin2id[parent._id]
        child_id = self.gremlin2id[child._id]
        self.g.add_edge(parent_id, child_id)

    def print_graph(self):
        print self.g.nodes()
        print self.g.edges()

    def get_feature(self):
#        l = len(feature_list)
#        temp_list = []
#        for i in range(l):
#            temp_list.append(0)
#        for index in self.id2code:
#            self.id2feat[index] = temp_list

        for index in self.id2code:
            temp_list = []
            code = self.id2code[index]
            code_list = code.strip().split()
#            print code
            code_set = set()
            for code in code_list:
                code_set.add(code.lower())

            for i in range(len(feature_list_exact)):
                if feature_list_exact[i] in code_set:
#                    print feature_list_exact[i]
                    temp_list.append(1)
                else:
                    temp_list.append(0)

            for i in range(len(feature_list_approx)):
                is_in = False
                for code in code_set:
                    if feature_list_approx[i] in code:
#                        print feature_list_approx[i]
                        is_in = True
                        break
                if is_in:
                    temp_list.append(1)
                else:
                    temp_list.append(0)

            self.id2feat[index] = temp_list
#            print self.id2feat[index]
            #code = self.normalize_code(self.id2code[index])

    def dump_graph(self, output_file):
        with open(output_file, 'w') as fp:
            for edge in self.g.edges():
                fp.write(str(edge[0]) + ',' + str(edge[1]) + '\n')


    def dump_feature(self, output_file):
        with open(output_file, 'w') as fp:
            csv_write = csv.writer(fp)
            csv_write.writerow(feature_list)
            for index in sorted(self.id2feat.keys()):
                csv_write.writerow(self.id2feat[index])

    def dump_code(self, output_file):
        with open(output_file, 'w') as fp:
#            csv_write = csv.writer(fp)
#            csv_write.writerow(feature_list)
            for index in sorted(self.id2code.keys()):
                fp.write((self.id2code[index]).lower() + '\n')

    def bfs(self, source, j):
        level = 0
        queue = []
        queue.append(source)
        visited = set()
        index = 0
#        print source
        while len(queue) != 0:
#        print "level,", level
            temp_queue = []
            for cur in queue:
                if cur._id not in visited:
                    if 'isCFGNode' in cur and cur['isCFGNode'] == "True":
                        if cur._id not in self.gremlin2id:
                            self.add_node(index, cur)
                            index += 1
                    visited.add(cur._id)
                    if cur._id > -1:
                        query = 'g.v('+str(cur._id)+').out'
                        #print query
                        s = j.runGremlinQuery(query)
                        #print len(s)
                        neighbor_vs = []
                        for one in s:
                            neighbor_vs.append(one._id)
                            if 'isCFGNode' in one and one['isCFGNode'] == 'True':
                                if one._id not in self.gremlin2id:
                                    self.add_node(index, one)
                                    index += 1
                                if cur._id in self.gremlin2id:
                                    self.add_edge(cur, one)
                        temp_queue.extend(s)
            queue = temp_queue
            level = level + 1

#        print "Depth,", level
#        print

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


def get_func_cfg(file_node, j, func, uid, output_folder):
    #print func
    g = code_cfg(file_node, func)
    #print g.filepath, g.func_name
    g.bfs(func, j)
    #g.print_graph()
    g.get_feature()
#    print(output_folder)
    g.dump_graph(os.path.join(output_folder, "%s.edge_list" %(uid)))
    g.dump_feature(os.path.join(output_folder, "%s.feat" %(uid)))
    g.dump_code(os.path.join(output_folder, "%s.code" %(uid)))


def dump_file_map(file_map, output_folder):

    #print file_map
    with open(os.path.join(output_folder, "uid2funcinfo.csv"), "w") as fp:
        for i in range(len(file_map)):
            fp.write(str(i) + ',' + file_map[i][0] + ',' + file_map[i][1] + '\n')


def get_content(j, output_folder):
    query = "getFilesByName('*')"
    file_list = j.runGremlinQuery(query)
    print "[+] Number of files:", len(file_list)
    uid = 0
    file_map = []
    for i in tqdm(range(len(file_list))):
        cur = file_list[i]
#        print cur
#       print i, results[i], results[i].properties
#    #query = 'g.v(' + str(cur._id) + ').out().{it.type == "Function"}'
        query = 'g.v(' + str(cur._id) + ').out' #().{it.type == "Function"}'
        func_list = j.runGremlinQuery(query)
        print(len(func_list))
        index = 0
        for func in func_list:
            index += 1
#            print(func['type'], func['name'])
#            if index > 3:
##                break
            if func['type'] == 'Function':
                get_func_cfg(cur, j, func, uid, output_folder)
                file_map.append([cur['filepath'], func['name']])
                uid += 1
        break
#
#    dump_file_map(file_map, output_folder)

def main(db_folder, output_folder):

    if not os.path.isdir(db_folder):
        raise Exception('%s does not exist' %(db_folder))
        exit(-1)

#    stop_db()
#    start_db(db_folder)
    j = connect_db()
    get_content(j, output_folder)
#    stop_db()

if __name__ == "__main__":

    if len(sys.argv) != 3:
        print "Usage: python get_cfg.py <database> <output_folder>"

        exit(0)

    main(sys.argv[1], sys.argv[2])
