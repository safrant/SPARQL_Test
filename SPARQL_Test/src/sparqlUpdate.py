'''
Created on Jul 22, 2016

@author: safrant
'''
from argparse import ArgumentParser

# use below to query STARDOG directly
SPARQL_ENDPOINT="https://sparql-evs.nci.nih.gov/sparql/query"
# or use below to query stardog via reverse proxy
# ENDPOINT="http://ncidb-d174-v.nci.nih.gov/TESTDB/query"
GRAPH="<http://NCIt_NG1>"

# use below to query ALLEGROGRAPH directly
# ENDPOINT="http://ncidb-d174-v.nci.nih.gov:10035/repositories/TESTDB"

# use below to query VIRTUOSO directly
# ENDPOINT=http://ncidb-d174-v.nci.nih.gov:8890/sparql
# GRAPH="<http://localhost:8890/vocab/NCIt>"

prefix = '''
PREFIX :<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX ncit:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX base:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
'''

'''PREFIX foaf:  <http://xmlns.com/foaf/0.1/>

WITH <http://example/addresses>
DELETE { ?person foaf:givenName 'Bill' }
INSERT { ?person foaf:givenName 'William' }
WHERE
  { ?person foaf:givenName 'Bill' }
'''
GRAPH_NCI="<http://ncicb.nci.nih.gov/owl/EVS/Thesaurus.owl>"

def testUpdate1_NCI():
    print("Testing update of NCI Thesaurus 1")
    
def reverseUpdate1_NCI(): 
    print("Reversing changes made in testUpdate1_NCI")
    
def testUpdate2_NCI():
    print("Testing update of NCI Thesaurus 2")


def reverseUpdate2_NCI():
    print("Reversing changes made in testUpdate2_NCI")


if __name__ == "__main__":
    parser = ArgumentParser(
             prog="checkEndpoint",
             description="Do SPARQL update.")
    
    