#/bin/bash#
# prefixes, copy as needed
#	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
#	prefix owl:  <http://www.w3.org/2002/07/owl#>
#	prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
#	prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#	prefix dc:	<http://purl.org/dc/elements/1.1/>
#	prefix dct:	<http://purl.org/dc/terms/>
#	prefix go:	<http://purl.obolibrary.org/obo/go.owl#>

declare -a ENDPOINT
declare -a PROXY
declare -a GRAPHNCI
declare -a GRAPHGO 

SERVICEHOST="http://sparql-evs-dev.nci.nih.gov/sparql"


# use below to query STARDOG directly
ENDPOINT[0]=$SERVICEHOST"/query"
# or use below to query stardog via reverse proxy
PROXY[0]=$SERVICEHOST"/sparql1"
GRAPHNCI[0]="<http://NCIt_NG1>"
GRAPHGO[0]="<http://GO_NG1>"

# use below to query ALLEGROGRAPH directly
ENDPOINT[1]=$SERVICEHOST":10035/repositories/TESTDB"
# or use below to query allegrograph via reverse proxy
PROXY[1]=$SERVICEHOST"/sparql2"
GRAPHNCI[1]="<http://NCIt_NG1>"
GRAPHGO[1]="<http://GO_NG1>"


# use below to query VIRTUOSO directly
ENDPOINT[2]=$SERVICEHOST":8890/sparql"
# or use below to query virtuoso via reverse proxy
PROXY[2]=$SERVICEHOST"/sparql3"
GRAPHNCI[2]="<http://NCIt_NG1>"
GRAPHGO[2]="<http://GO_NG1>"
 
 
echo time queries from $ENDPOINT

declare -a QUERY 

# test endpoints
QUERY[0]="query= select distinct ?g where { graph ?g { ?s ?p ?o } }"
count=0
while [ $count != 3 ]
do
	echo
	echo test of endpoint "${ENDPOINT[count]}"
	curl -s -w %{time_total}  -X POST \
		-H "Accept: application/sparql-results+json" \
		-H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
		"${ENDPOINT[count]}" --data-urlencode "${QUERY[0]}" 
	echo 
	count=$(( $count + 1 ))
done

# test proxies, no credentials in call
QUERY[0]="query= select distinct ?g where { graph ?g { ?s ?p ?o } }"
count=0
while [ $count != 3 ]
do
	echo
	echo test of proxy "${PROXY[count]}"
	curl -s -w %{time_total}  -X POST \
		-H "Accept: application/sparql-results+json" \
		"${PROXY[count]}" --data-urlencode "${QUERY[0]}" 
	echo 
	count=$(( $count + 1 ))
done

# test federation service, stardog endpoint as sender and three proxies as receivers
count=0
while [ $count != 3 ]
do
	LOCALENDPOINT=${ENDPOINT[0]}
	echo
	echo test of service call on proxy "${PROXY[count]}" from "$LOCALENDPOINT"
	QUERY[0]="query=select ?s ?p ?o where { service <${PROXY[count]}> { select ?s ?p ?o where {?s ?p ?o } limit 5 } } limit 5 "
	echo $QUERY[0]
	curl -s -w %{time_total}  -X POST \
		-H "Accept: application/sparql-results+json" \
		-H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
		$LOCALENDPOINT --data-urlencode "${QUERY[0]}" 
	echo 
	count=$(( $count + 1 ))
done


declare -a MESSAGE

LOCALENDPOINT=${ENDPOINT[0]}
MESSAGE[0]="non-federated query to get ncit-go map"
QUERY[0]="query=
prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
select ?nci ?ncilabel ?go ?gotext
where { 
	graph ${GRAPHNCI[0]} { ?nci ncit:FULL_SYN ?gotext ; rdfs:label ?ncilabel } .
	graph ${GRAPHGO[0]} { ?go rdfs:label ?gotext ; a owl:Class . }
	} limit 5"	

MESSAGE[1]="federated query to get ncit-go map"
QUERY[1]="query=
prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
select ?nci ?go ?gotext
where { 
	graph ${GRAPHNCI[0]} { ?nci ncit:FULL_SYN ?gotext ; rdfs:label ?ncilabel } 
	service <${PROXY[0]}> { graph ${GRAPHGO[0]} {?go rdfs:label ?gotext ; a owl:Class . } }
	} limit 5"	
	
count=0
while [ $count != 2 ]
do
	echo
	echo "${MESSAGE[count]}"
	echo "${QUERY[count]}"
	curl -s -w %{time_total}  -X POST \
		-H "Accept: application/sparql-results+json" \
		-H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
		$LOCALENDPOINT --data-urlencode "${QUERY[count]}"
	echo 
	count=$(( $count + 1 ))
done




#  -o result-${count}.txt
# 
