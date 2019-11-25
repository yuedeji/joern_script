from joern.all import JoernSteps

j = JoernSteps()
j.setGraphDbURL('http://localhost:7474/db/data/')
j.connectToDatabase()

#ids =  j.runGremlinQuery('getAllStatements().id')
#print ids

#CHUNK_SIZE = 256
#for chunk in j.chunks(ids, CHUNK_SIZE):
#    query = """ idListToNodes(%s).astNodes().id """ % (chunk)
#    for r in j.runGremlinQuery(query):
#        print r
