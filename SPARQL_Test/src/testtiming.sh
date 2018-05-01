# prefixes
#	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
#	prefix owl:  <http://www.w3.org/2002/07/owl#>
#	prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
#	prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#	prefix dc:	<http://purl.org/dc/elements/1.1/>
#	prefix dct:	<http://purl.org/dc/terms/>


# use below to query STARDOG directly
 ENDPOINT="https://sparql-evs.nci.nih.gov/sparql/query"
# or use below to query stardog via reverse proxy
# ENDPOINT="http://sparql-evs-dev.nci.nih.gov/sparql"
 GRAPH="<http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl>"

 
 
 
echo time queries from $ENDPOINT

T0=$(date +%s.%N)
echo top 5000 from NCIt graph 
QUERY="query=
	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
	SELECT * 
	FROM $GRAPH where { ?s ?p ?o } LIMIT 5000"
curl -s -X POST -H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
	-H "Accept: application/sparql-results+json" \
	$ENDPOINT --data-urlencode "$QUERY" \
	> /dev/null
T1=$(date +%s.%N)

DIFF=$(gawk "BEGIN {print $T1 - $T0 ; exit }" )
echo $DIFF


T0=$(date +%s.%N)
echo  existential restrictions on all the classes in a primitive transitive closure of prefixed NCIt Gene	
QUERY="query=
	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
	prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
	prefix owl:  <http://www.w3.org/2002/07/owl#>
	SELECT ?subject ?role ?object
	WHERE {
		?subject rdfs:subClassOf ?an .
		?an owl:onProperty ?role .
		?an owl:someValuesFrom ?object .
		?subject rdfs:subClassOf* ncit:Gene
		}
	order by asc(?subject)"
curl -s -X POST -H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
	-H "Accept: application/sparql-results+json" \
	$ENDPOINT --data-urlencode "$QUERY" \
	> /dev/null
T1=$(date +%s.%N)
DIFF=$(gawk "BEGIN {print $T1 - $T0 ; exit }" )
echo $DIFF

T0=$(date +%s.%N)
echo  as above but on the NCIt graph	
QUERY="query=
	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
	prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#>
	prefix owl:  <http://www.w3.org/2002/07/owl#>
	SELECT ?subject ?role ?object
	FROM $GRAPH
	WHERE {
		?subject rdfs:subClassOf ?an .
		?an owl:onProperty ?role .
		?an owl:someValuesFrom ?object .
		?subject rdfs:subClassOf* ncit:Gene
		}
	order by asc(?subject)"
curl -s -X POST -H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
	-H "Accept: application/sparql-results+json" \
	$ENDPOINT --data-urlencode "$QUERY" \
	> /dev/null

T1=$(date +%s.%N)
# DIFF=$(gawk "BEGIN {print $T1 - $T0 ; exit }" )
((DIFF = $T1 - $T0))
echo $DIFF

T0=$(date +%s.%N)
echo  all incoming relations to prefixed NCIt Human
QUERY="query=
	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
	SELECT ?subject ?p
	WHERE {
		?subject ?p ncit:Human .
		}
	order by asc(?subject)"
curl -s -X POST -H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
	-H "Accept: application/sparql-results+json" \
	$ENDPOINT --data-urlencode "$QUERY" \
	> /dev/null

T1=$(date +%s.%N)
DIFF=$(gawk "BEGIN {print $T1 - $T0 ; exit }" )
echo $DIFF


T0=$(date +%s.%N)
echo  as above but on the NCIt graph
QUERY="query=
	prefix ncit:  <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
	SELECT ?subject ?p
	FROM $GRAPH
	WHERE {
		?subject ?p ncit:Human .
		}
	order by asc(?subject)"
curl -s -X POST -H "Authorization: Basic dHJpcGxlcmVhZG9ubHk6dHJpcGxlcmVhZG9ubHk=" \
	-H "Accept: application/sparql-results+json" \
	$ENDPOINT --data-urlencode "$QUERY" \
	> /dev/null

T1=$(date +%s.%N)
DIFF=$(gawk "BEGIN {print $T1 - $T0 ; exit }" )
echo $DIFF



