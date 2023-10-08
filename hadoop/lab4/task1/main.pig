raw_data = LOAD '/user/hduser/lab4/task1/test.txt' USING PigStorage('\n') AS (line:chararray);
with_indices = RANK raw_data;
words_with_indices = FOREACH with_indices GENERATE $0, FLATTEN(TOKENIZE(line, ' '));
grouped_words = GROUP words_with_indices BY $1;
result = FOREACH grouped_words GENERATE $0 as word, BagToTuple($1.$0) as indices;

RMF /user/hduser/lab4/task1-output;
STORE result INTO '/user/hduser/lab4/task1-output' using PigStorage(',');
DUMP result;