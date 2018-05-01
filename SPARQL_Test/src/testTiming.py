'''
Created on Jul 22, 2016

@author: safrant
'''

from time import time
import requests
from requests.auth import HTTPBasicAuth
import sys
from argparse import ArgumentParser
import json
import logging






SPARQL_ENDPOINT="https://sparql-evs.nci.nih.gov/sparql"
GRAPH="<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl>"

SPARQL_USER = "NA"
SPARQL_PASSWORD = "NA"



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
    print(r.status_code)
    if r.status_code != 200:
        sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
        sys.exit(1)
   
    return r.json()

# def run_large_sparql_query(query):
#     headers = {'Accept': 'application/sparql-results+json'}
#     r = urllib3.post(SPARQL_ENDPOINT,
#             headers=headers,data={ "query": query },
#             auth=HTTPBasicAuth(SPARQL_USER,SPARQL_PASSWORD))
#     print(r.status_code)
#     if r.status_code != 200:
#         sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
#         sys.exit(1)
# 
#     opener.open(url).close() # raise an exception if the authentication fails
#     

def getTop50(GRAPH):
    print("top 50 from NCIt graph")
    QUERY='''SELECT * 
    FROM $GRAPH where { ?s ?p ?o } LIMIT 50'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']


def getGeneTransitiveClosure():
    print("Gene transitive closure")
    QUERY='''SELECT ?subject ?role ?object
    WHERE {
        ?subject rdfs:subClassOf ?an .
        ?an owl:onProperty ?role .
        ?an owl:someValuesFrom ?object .
        ?subject rdfs:subClassOf* ncit:C16612
        }
    ORDER BY asc(?subject)
    
    LIMIT 100
    '''
    query = prefix + QUERY
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def getGeneTransitiveClosureFromGraph(GRAPH):
    print("Gene transitive closure from graph")
    QUERY='''SELECT ?subject ?role ?object
    FROM $GRAPH
    WHERE {
        ?subject rdfs:subClassOf ?an .
        ?an owl:onProperty ?role .
        ?an owl:someValuesFrom ?object .
        ?subject rdfs:subClassOf* ncit:C16612
        }
    order by asc(?subject)
    '''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def humanIncomingRelationships():
    print("Incoming relationships to HUMAN")
    QUERY='''SELECT ?subject ?p
    WHERE {
        ?subject ?p ncit:C14225 .
        }
    order by asc(?subject)'''
    query = prefix + QUERY
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def humanIncomingRelationshipsFromGraph(GRAPH):
    print("Incoming relationships to HUMAN from Graph")
    QUERY='''SELECT ?subject ?p
    FROM $GRAPH
    WHERE {
        ?subject ?p ncit:C14225 .
        }
    order by asc(?subject)'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']


def  PropertyTest1():
    print("Testing from GF 1")
    QUERY='''SELECT ?subject ?role ?object 
    WHERE { ?subject rdfs:subClassOf ?an . 
       ?an owl:onProperty ?role . 
       ?an owl:someValuesFrom 
       ?object . 
       ?subject rdfs:subClassOf* ncit:C16612 } 
    order by asc(?subject) limit 5'''
    query = prefix + QUERY
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def PropertyTest2():
    print("Testing from GF 2")
    QUERY='''SELECT ?subject ?p 
    WHERE { ?subject ?p ncit:C14225 . } 
    order by asc(?subject) LIMIT 5'''
    query = prefix + QUERY
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def OpenLinkTest1(GRAPH):
    print("Testing from Open Link 1")
    QUERY='''SELECT ?subject ?role ?object
    FROM $GRAPH
    WHERE
        {
            ?subject rdfs:subClassOf ?an .
            ?an owl:onProperty ?role .
            ?an owl:someValuesFrom ?object .
            ?subject rdfs:subClassOf* ncit:C18120
        }
        
      ORDER BY asc(?subject)'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def OpenLinkTest2(GRAPH):
    print("Testing from Open Link 2")
    QUERY='''SELECT ?subject ?role ?object
      FROM
        $GRAPH
          WHERE
            {
              ?subject rdfs:subClassOf ?an .
              ?an owl:onProperty ?role .
              ?an owl:someValuesFrom ?object .
              ?subject rdfs:subClassOf+ ncit:C16612
            }
        
      ORDER BY asc(?subject)'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def OpenLinkTest3(GRAPH):
    print("Testing from Open Link 3")
    QUERY='''SELECT ?subject ?role ?object
      FROM
        $GRAPH
          WHERE
            {
              ?subject rdfs:subClassOf ?an .
              ?an owl:onProperty ?role .
              ?an owl:someValuesFrom ?object .
              ?subject rdfs:subClassOf+ ncit:C16612
            }
        
      ORDER BY asc(?subject)
      LIMIT 50'''
    query = QUERY.replace("$GRAPH",GRAPH)
    query = prefix + query
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']


if __name__ == "__main__":
    parser = ArgumentParser(
             prog="checkEndpoint",
             description="Do SPARQL timings.")
    
    args = parser.parse_args()
#    GRAPH="<http://NCIt_NG1>"
#     GRAPH="<http://ncicb.nci.nih.gov/owl/EVS/Thesaurus.owl>"
    
    print("time queries from " + SPARQL_ENDPOINT);
    print("==========================================================")
    
    T0 = time()
    results = getTop50(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    print(json.dumps(results,indent=2))
    
    print("==========================================================")
    
    T0 = time()
    results = getGeneTransitiveClosure()
    T1 = time()
    DIFF = (T1 - T0)
    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = getGeneTransitiveClosureFromGraph(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = humanIncomingRelationships()
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = humanIncomingRelationshipsFromGraph(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = PropertyTest1()
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = PropertyTest2()
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = OpenLinkTest1(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = OpenLinkTest2(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)
    
    print("==========================================================")
    
    T0 = time()
    results = OpenLinkTest3(GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
#    print(json.dumps(results,indent=2))
    print(DIFF)