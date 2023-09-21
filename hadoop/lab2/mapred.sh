#!/bin/bash
MAPPER="mapper.py"
REDUCER="reducer.py"
INPUT=$1
OUTPUT="/user/hduser/lab2_output"
echo "[SCRIPT] Removing Output $OUTPUT..."
/usr/local/hadoop/bin/hdfs dfs -rm -r -f $OUTPUT
echo "[SCRIPT] Starting MapReduce Job For $INPUT..."
/usr/local/hadoop/bin/mapred streaming -input $INPUT -output $OUTPUT -mapper $MAPPER -reducer $REDUCER
/usr/local/hadoop/bin/hdfs dfs -head "$OUTPUT/part-00000"