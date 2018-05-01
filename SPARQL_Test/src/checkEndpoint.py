'''
Created on Jul 22, 2016

@author: ongk
'''
#!/usr/bin/env python

import sys
import os
import json
import requests
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser


SPARQL_ENDPOINT="https://sparql-evs.nci.nih.gov/sparql"

SPARQL_USER = "NA"
SPARQL_PASSWORD = "NA"

prefix = '''
PREFIX :<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX base:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX owl:<http://www.w3.org/2002/07/owl#>
PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs:<http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd:<http://www.w3.org/2001/XMLSchema#>
PREFIX ncit:<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
'''

'''
# run_sparql_query
'''
def run_sparql_query(query):
    headers = {'Accept': 'application/sparql-results+json'}
    r = requests.post(SPARQL_ENDPOINT,
            headers=headers,data={ "query": query },
            auth=HTTPBasicAuth(SPARQL_USER,SPARQL_PASSWORD))

    if r.status_code != 200:
        sys.stderr.write("Problem Status Code: " + str(r.status_code) + "\n")
        sys.exit(1)

    return r.json()

#
# get_concept
#
concept_query = '''
SELECT ?concept ?concept_label
WHERE {
   ?concept a owl:Class .
   ?concept ncit:NHC0"CONCEPT_CODE" .
   ?concept rdfs:label ?concept_label
}
'''
# concept_query = '''
# SELECT ?concept ?concept_label
# FROM <http://NCIT_NG1>
# WHERE {
#    ?concept a owl:Class .
#    ?concept rdfs:label ?concept_label
# }
# '''
def get_concept(concept_uri):
    query = prefix + concept_query
    query = query.replace("CONCEPT_CODE",concept_uri)
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

#
# get_concept_annotation_properties
#
concept_annotation_properties_query = '''
SELECT ?property ?property_code ?property_label ?property_value
WHERE { ?concept a owl:Class .
        ?concept :code "CONCEPT_CODE" .
        ?property a owl:AnnotationProperty .
        ?property rdfs:label ?property_label .
        ?property :code ?property_code .
        ?concept ?property ?property_value
}
ORDER BY ?property_label
'''

def get_properties(concept_uri):
    query = prefix + concept_annotation_properties_query
    query = query.replace("CONCEPT_CODE",concept_uri)
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']

#
# get_concept_axioms
#
concept_axioms_query = '''
SELECT DISTINCT ?annotated_property ?annotated_target ?term_source
                ?term_group ?source_code ?def_source ?subsource_name ?code
WHERE {
  ?axiom a owl:Axiom .
  ?axiom owl:annotatedSource :CONCEPT_URI .
  OPTIONAL {?axiom owl:annotatedProperty ?annotated_property} .
  OPTIONAL {?axiom owl:annotatedTarget ?annotated_target} .
  OPTIONAL {?axiom :term-source ?term_source} .
  OPTIONAL {?axiom :term-group ?term_group} .
  OPTIONAL {?axiom :source-code ?source_code} .
  OPTIONAL {?axiom :def-source ?def_source} .
  OPTIONAL {?axiom :subsource-name ?subsource_name } .
  OPTIONAL {?axiom :code ?code }
}
'''

def get_axioms(concept_uri):
    query = prefix + concept_axioms_query
    query = query.replace("CONCEPT_URI",concept_uri)
    print(query)
    obj = run_sparql_query(query)
    return obj['results']['bindings']



if __name__ == "__main__":
    parser = ArgumentParser(
             prog="checkEndpoint",
             description="Check the SPARQL Endpoint.")

    args = parser.parse_args()
    print("Concept")
    print("==========================================================")
    results = get_concept("C7928")
    print(json.dumps(results,indent=2))

#     print("Concept Properties")
#     print("==========================================================")
#     results = get_properties("C7928")
#     print(json.dumps(results,indent=2))
#  
#     print("Concept Axioms")
#     print("==========================================================")
#     results = get_axioms("Childhood_Germ_Cell_Neoplasm")
#     print(json.dumps(results,indent=2))
