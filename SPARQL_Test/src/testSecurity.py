'''
Created on Feb 2, 2017

@author: safrant
'''

from time import time
import requests
from requests.auth import HTTPBasicAuth
import sys
from argparse import ArgumentParser
import json
import logging





# use below to query STARDOG directly
SPARQL_ENDPOINT="https://sparql-evs.nci.nih.gov/sparql"
# or use below to query stardog via reverse proxy






SPARQL_USER = "NA"
SPARQL_PASSWORD = "NA"

SPARQL_ADMIN_USER = "NA"
SPARQL_ADMIN_PASSWORD = "NA!"


prefix = '''
PREFIX :<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX ncit:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX base:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
'''

    
'''
# run_sparql_query
'''

def run_sparql_query(query):
    logging.basicConfig(level=logging.DEBUG)
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.post(SPARQL_ENDPOINT,
        headers=headers,data={ "query": query },
        auth=HTTPBasicAuth(SPARQL_USER,SPARQL_PASSWORD))
    print(r.content)
    if r.status_code != 200:
        sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
#             sys.exit(1)
    else:
        return r.json()

def run_admin_sparql_query(query):
    logging.basicConfig(level=logging.DEBUG)
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.post(SPARQL_ENDPOINT,
            headers=headers,data={ "query": query },
            auth=HTTPBasicAuth(SPARQL_ADMIN_USER,SPARQL_ADMIN_PASSWORD))
    print(r.content)
    if r.status_code != 200:
        sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
    else:
        return r.json()

def creategraph(admin, GRAPH):
    print("create GRAPH")
    QUERY='''CREATE GRAPH $GRAPH'''
    query1 = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query1
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def insertIntoNamedGraph(admin, GRAPH):
    print("insert into Graph")
    QUERY='''INSERT DATA
    {
    GRAPH $GRAPH {ncit:Security_Example_NG ncit:FULL_SYN "Example";
    ncit:FULL_SYN "example" }
    }'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def queryGraph(GRAPH):
    print("query graph")
    QUERY='''SELECT * 
    FROM $GRAPH where { ?s ?p ?o } LIMIT 50'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def loadGraph(admin, GRAPH):
    print("insert into Graph")
    QUERY='''LOAD <http://www.berkeleybop.org/ontologies/zfs.owl> INTO GRAPH $GRAPH'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def copyGraph(admin, sGRAPH, tGRAPH):
    print("insert into Graph")
    QUERY='''COPY $sGRAPH TO $tGRAPH'''
    query1 = QUERY.replace("$sGRAPH",sGRAPH)
    query = query1.replace("$tGRAPH", tGRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def clearGraph(admin, GRAPH):
    print("insert into Graph")
    QUERY='''CLEAR GRAPH $GRAPH'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def insertIntoNamedGraph2(admin, GRAPH):
    print("insert into Graph")
    QUERY='''INSERT DATA
    {
    GRAPH $GRAPH {ncit:Security_Example_NG2 ncit:FULL_SYN "Example_2";
    ncit:code "C11111" }
    }'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def addDataToGraph(admin, sGRAPH, tGRAPH):
    print("add data to Graph")
    QUERY='''ADD $sGRAPH TO $tGRAPH'''
    query1 = QUERY.replace("$sGRAPH",sGRAPH)
    query = query1.replace("$tGRAPH", tGRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def moveGraph(admin, sGRAPH, tGRAPH):
    print("add data to Graph")
    QUERY='''MOVE $sGRAPH TO $tGRAPH'''
    query1 = QUERY.replace("$sGRAPH",sGRAPH)
    query = query1.replace("$tGRAPH", tGRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def deleteFromGraph(admin, GRAPH):
    print("delete from Graph")
    QUERY='''DELETE DATA
    {
    GRAPH $GRAPH {ncit:Security_Example_NG ncit:FULL_SYN "Example"}
    }'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

def dropGraph(admin, GRAPH):
    print("drop Graph")
    QUERY='''DROP GRAPH $GRAPH'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    if admin == True:
        obj = run_admin_sparql_query(query)
    else:
        obj = run_sparql_query(query)
#     return obj['results']['bindings']

if __name__ == "__main__":
    parser = ArgumentParser(
             prog="checkEndpoint",
             description="Do SPARQL security tests.")
    
    args = parser.parse_args()
#    GRAPH="<http://NCIt_NG1>"
#     GRAPH="<http://ncicb.nci.nih.gov/owl/EVS/Thesaurus.owl>"
    GRAPH1="<http://TEST_GRAPH1>"
    GRAPH2="<http://TEST_GRAPH2>"
    
    print("security queries from " + SPARQL_ENDPOINT);
    print("==========================================================")
    print("Test read only user attempt to create graph")
    T0 = time()
    results = creategraph(False,GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    print(json.dumps(results,indent=2))
    
    print("==========================================================")
    print("Create graphs as admin for use in the next test")
    T0 = time()
    results = creategraph(True,GRAPH1)
    results = creategraph(True,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    print(json.dumps(results,indent=2))
    
    print("==========================================================")
    
    T0 = time()
    results = insertIntoNamedGraph(False, GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = insertIntoNamedGraph(True, GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = loadGraph(False,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = loadGraph(True,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = copyGraph(False,GRAPH1,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = copyGraph(True,GRAPH1,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = insertIntoNamedGraph2(False,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = insertIntoNamedGraph2(True,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = addDataToGraph(False,GRAPH1,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = addDataToGraph(True,GRAPH1,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = moveGraph(False,GRAPH2,GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH1)
    results = queryGraph(GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = deleteFromGraph(False,GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = deleteFromGraph(True,GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = queryGraph(GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = dropGraph(False,GRAPH1)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = dropGraph(True,GRAPH1)
    results = dropGraph(True,GRAPH2)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)