from pyspark.sql import SparkSession
from pyspark.sql import Row


def loadMoviesNames():
    moviesNames = {}
    with open("ml-100k/u.ITEM") as f: 
        for line in f:
            fields = line.split('|')
            moviesNames[int(fields[0])]=fields[1]
    return moviesNames
    
    
spark = SparkSession.builder.config("spark.sql.warehouse.dir","file:///C:/temp").appName("FilmsPopulaires").getOrCreate()

nameDict = loadMoviesNames()

lines = spark.sparkContext.textFile("file:///spark_course/ml-100k/u.data")

movies =  lines.map(lambda x:Row(movieID=int(x.split()[1])))

MovieDataSet = spark.createDataFrame(movies).cache()

topMovies = MovieDataSet.groupBy("movieID").count().orderBy("count", ascending=False).cache()
topMovies.show()





