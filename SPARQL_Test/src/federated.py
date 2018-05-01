'''
Created on Aug 4, 2016

@author: safrant
'''
from argparse import ArgumentParser

ENDPOINT = []
PROXY = []
GRAPHNCI = []
GRAPHGO = []

SERVICEHOST="http://sparql-evs-dev.nci.nih.gov/sparql"

if __name__ == '__main__':
        parser = ArgumentParser(
             prog="checkEndpoint",
             description="Federated Query test.")
        
        args = parser.parse_args()
        
        