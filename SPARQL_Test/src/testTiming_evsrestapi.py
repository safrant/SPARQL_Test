from time import time
import requests
from requests.auth import HTTPBasicAuth
import sys
from argparse import ArgumentParser
import json
import logging






SPARQL_ENDPOINT="http://sparql-evs-dev.nci.nih.gov/sparql"
GRAPH="<http://NCIt>"
CODE="C4872"



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
prefix franzOption_logQuery: <franz:yes>
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


def constructConceptLabelQuery(CODE,GRAPH):
    print("constructConceptLabelQuery")
    QUERY='''SELECT ?conceptLabel
    { GRAPH $GRAPH
        { ?concept a owl:Class .
          ?concept :NHC0 "$CODE" .
          ?concept rdfs:label ?conceptLabel
        }
    }
    '''
    QUERY2 = QUERY.replace("$CODE",CODE)
    query = QUERY2.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

    
def constructConceptLabelQuery2(CODE,GRAPH):
    print("constructConceptLabelQuery")
    QUERY='''SELECT ?conceptLabel
    { GRAPH $GRAPH
        { ncit:$CODE rdfs:label ?conceptLabel
        }
    }
    '''
    QUERY2 = QUERY.replace("$CODE",CODE)
    query = QUERY2.replace("$GRAPH",GRAPH)
    query = prefix + query
    print (query)
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
    results = constructConceptLabelQuery(CODE,GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    print(json.dumps(results,indent=2))
    
    print("==========================================================")
    
    print("time queries from " + SPARQL_ENDPOINT);
    print("==========================================================")
    
    T0 = time()
    results = constructConceptLabelQuery2(CODE,GRAPH)
    T1 = time()
    DIFF = (T1 - T0)
    print(DIFF)
    print(json.dumps(results,indent=2))
    
 