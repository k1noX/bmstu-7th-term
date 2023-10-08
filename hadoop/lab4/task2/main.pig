REGISTER hdfs:///tmp/piggybank.jar;
DEFINE CSVLoader org.apache.pig.piggybank.storage.CSVLoader();

tweets = LOAD '/user/hduser/lab4/task2/tweets.csv' using CSVLoader() AS (tweet_id: long, tweet: chararray, login: chararray);
users = LOAD '/user/hduser/lab4/task2/users.csv' using CSVLoader() AS (login: chararray, user_name: chararray, state: chararray);

grouped_tweets = GROUP tweets BY login;
login_with_tweet_count = FOREACH grouped_tweets GENERATE $0 as login, COUNT($1) as tweet_count;
filtered_logins = FILTER login_with_tweet_count BY tweet_count >= 2;
joined_logins = JOIN filtered_logins BY login, users BY login;
user_tweet_count = FOREACH joined_logins GENERATE users::user_name, filtered_logins::tweet_count;
result = ORDER user_tweet_count BY $1 DESC;

RMF /user/hduser/lab4/task2-output;
STORE result INTO '/user/hduser/lab4/task2-output' using PigStorage(',');
DUMP result;