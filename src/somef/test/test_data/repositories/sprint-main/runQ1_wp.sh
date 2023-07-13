#!/bin/bash

echo  "run,elapsed_time,kernel_mode,User_mode,memory_max,memory_average,file" >>timeQ1.csv

for i in 1 2 3 4 5 7 8 9 10
do

time  -f "Run,elapsed_time,kernel_mode,user_mode,memory_max,memory_average\n${i},%e,%S,%U,%M,%K," -o tmp_time.csv curl -G 'http://localhost:5001/sparql' \
     --data-urlencode query='
PREFIX dcat: <http://www.w3.org/ns/dcat#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT *
WHERE {
?d a dcat:Dataset .
?d dct:qualFreq ?qf .
?d dct:metadataDate ?md .
OPTIONAL {
?d a dcat:Dataset .
?d dct:qualFreq ?qf .
?d dct:metadataDate ?md .
?d_ a dcat:Dataset .
?d_ dct:qualFreq ?qf_ .
?d_ dct:metadataDate ?md_ .
FILTER (?qf_ <= ?qf && ?md_ >= ?md && (?qf_ < ?qf || ?md_ > ?md)) }
FILTER(! BOUND(?d_))
}'


tail -1 tmp_time.csv>> timeQ1.csv

done
rm tmp_time.csv
