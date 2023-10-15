from pyspark.sql import SparkSession, functions

if __name__ == '__main__':
    spark = SparkSession.builder.appName('keyone-app').getOrCreate()

    movies_path = 'data/movies.csv'
    ratings_path = 'data/ratings.csv'
    result_path = 'data/result'

    movies = spark.read.csv(movies_path, header=True)
    ratings = spark.read.csv(ratings_path, header=True)

    average_ratings = ratings.groupBy('movieId').agg(
        functions.mean('rating').alias('avgRating')
    ).select('movieId', 'avgRating')

    joined_table = average_ratings.join(movies, 'movieId').select(
        'movieId', 'title', 'avgRating'
    )
    sorted_table = joined_table.orderBy('avgRating', ascending=False)

    result_table = sorted_table.limit(20)
    result_table.show()
    result_table.write.mode('overwrite').csv(result_path)
