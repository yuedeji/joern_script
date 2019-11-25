from joern.all import JoernSteps
j = JoernSteps()
j.setGraphDbURL('http://localhost:7474/db/data/')
j.connectToDatabase()

#query = """
#getArguments('strcpy', '1').sideEffect{ argument = it.code;}.unsanitized({it._().or(_().isCheck('.*' + argument + '.*'), _().codeContains('.*min.*'))}).locations()
#"""

#query = """
#getCallsTo('memcpy').ithArguments('0').astNodes()
#"""

#query = """
#getArguments('memcpy', '2').uses()
#.filter{it.code == 'len'}
#.filter{
#        it.in('USES')
#        .filter{it.type == 'Condition'}.toList() == []
#}
#"""

#query = """
#getArguments('memcpy', '1')
#"""
#.sideEffect{ paramName = '.*len.*' }
#.filter{ it.code.matches(paramName) }
#.unsanitized{ it.isCheck( paramName ) }"""
#.params( paramName )

query = "getFilesByName('*')"
results = j.runGremlinQuery(query)
print "[+] Number of files:", len(results)
for i in range(len(results)):
    cur = results[i]
    print i, results[i], results[i].properties
    #query = 'g.v(' + str(cur._id) + ').out().{it.type == "Function"}'
    query = 'g.v(' + str(cur._id) + ').out' #().{it.type == "Function"}'
    s = j.runGremlinQuery(query)

    for node in s:
        if node['type'] == 'Function':
            print node

#    print s
#    if i > 0:
    break
exit()

query = "getCallsTo('???cpy')"
#query = "getFunctionsByName('???cpy')"
print "[+] Running query!"
results = j.runGremlinQuery(query)

print "[+] Number of results: " + str(len(results))
i = 0
for r in results:
    print r
#    if i == 0:
#        i += 1

query = "getCallsTo('????cpy')"
print "[+] Running query!"
results = j.runGremlinQuery(query)

print "[+] Number of results: " + str(len(results))
i = 0
for r in results:
    print r
#        print dir(r)
