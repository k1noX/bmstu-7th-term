#!/bin/bash
PRE_MAPPER="pre_mapper.py"
MAPPER="mapper.py"
POST_MAPPER="post_mapper.py"
REDUCER="reducer.py"
INPUT=$1
OUTPUT="/user/hduser/lab3_output"
iteration=0
MAX_ITERATIONS=10
echo "[SCRIPT] Removing Output $OUTPUT..."
/usr/local/hadoop/bin/hdfs dfs -rm -r -f $OUTPUT
iteration=$((iteration + 1))
echo "[SCRIPT] Starting MapReduce Job For $INPUT: $iteration/$MAX_ITERATIONS"
/usr/local/hadoop/bin/hdfs dfs -rm -r -f "$OUTPUT.$iteration"
/usr/local/hadoop/bin/mapred streaming -input "$INPUT" -output "$OUTPUT.$iteration" -mapper $PRE_MAPPER -reducer $REDUCER

for i in $(seq $((iteration + 1)) $MAX_ITERATIONS)
do
  echo "[SCRIPT] Starting MapReduce Job For $OUTPUT.$i: $i/$MAX_ITERATIONS"
  /usr/local/hadoop/bin/hdfs dfs -rm -r -f "$OUTPUT.$i"
  /usr/local/hadoop/bin/mapred streaming -input "$OUTPUT.$((i-1))/part-00000" -output "$OUTPUT.$i" -mapper $MAPPER -reducer $REDUCER
done

echo "[SCRIPT] Starting Final MapReduce Job For $OUTPUT.$MAX_ITERATIONS..."
/usr/local/hadoop/bin/hdfs dfs -rm -r -f "$OUTPUT"
/usr/local/hadoop/bin/mapred streaming -D mapred.text.key.comparator.options=-nr -input "$OUTPUT.$MAX_ITERATIONS/part-00000" -output "$OUTPUT" -mapper $POST_MAPPER

/usr/local/hadoop/bin/hdfs dfs -cat "$OUTPUT/part-00000" | sort -r