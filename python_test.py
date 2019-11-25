from joern.all import JoernSteps
#from sets import Set

j = JoernSteps()
j.setGraphDbURL('http://localhost:7474/db/data/')
j.connectToDatabase()

#res =  j.runGremlinQuery('getFunctionsByName("*")')
#res =  j.runCypherQuery('')
#print res
#query = 'getAllSatements().id'
#ids = j.runGremlinQuery(query)
#print ids

#for one in ids:
#    print one.o

#for one in res:
#    print one

#print main_nodes

#for one in main_nodes:
#one = main_nodes[0]
#print dir(one)
#print one


## BFS from a single source
def bfs(source):
    level = 0
    queue = []
    queue.append(source)
#    queue = main_nodes
    temp_queue = []
    print queue

    visited = set()

    while len(queue) != 0:
        print "level,", level
        while len(queue) != 0:
            cur = queue[0]
            if cur._Node__id not in visited:
                visited.add(cur._id)
                if cur._id > -1:
                    print cur.properties
                    query = 'g.v('+str(cur._id)+').code'
                    print j.runGremlinQuery(query)
                    query = 'g.v('+str(cur._id)+').out'
                    #print query
                    s = j.runGremlinQuery(query)
                    print len(s)
                    neighbor_vs = []
                    for one in s:
                        neighbor_vs.append(one._id)
                    print neighbor_vs
#                    print s
                    temp_queue.extend(s)
            del queue[0]
        queue = temp_queue
        temp_queue = []
        level = level + 1

    print "Depth, ", level


if __name__ == '__main__':
    main_nodes = j.runGremlinQuery('getFunctionsByName("main")')
    bfs(main_nodes[0])
