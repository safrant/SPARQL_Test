from time import time
import requests
from requests.auth import HTTPBasicAuth
import sys
from argparse import ArgumentParser
import json
import logging

SPARQL_ENDPOINT="https://sparql-evs.nci.nih.gov/sparql"
GRAPH="<http://NCIt>"

SPARQL_USER = "na"
SPARQL_PASSWORD = "na"

prefix = '''
PREFIX :<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX ncit:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX base:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
'''

def run_sparql_query(query):
    logging.basicConfig(level=logging.DEBUG)
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.post(SPARQL_ENDPOINT,
            headers=headers,data={ "query": query },
            auth=HTTPBasicAuth(SPARQL_USER,SPARQL_PASSWORD))
    if r.status_code != 200:
        sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
        sys.exit(1)
   
    return r.json()

def getAll():
    print("Get all entries from database")
    QUERY='''SELECT * where { ?var1 ?var2 ?var3 }'''
    query = prefix + QUERY
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

def getLargeLimit():
    print("Get large limit, > 10000")
    QUERY='''SELECT * where { ?var1 ?var2 ?var3 } LIMIT 15000'''
    query = prefix + QUERY
    print (query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

if __name__ == "__main__":
    parser = ArgumentParser(
             prog="checkEndpoint",
             description="Do mod_security tests.")
    
    args = parser.parse_args()
    
    results = getAll()
    print(json.dumps(results,indent=2))
    
    results = getLargeLimit()
    print(json.dumps(results,indent=2))