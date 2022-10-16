from __future__ import print_function

import sys
import json
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.streaming import StreamingContext
import pyspark
from pyspark.conf import SparkConf
from pyspark import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.sql.functions import from_json, struct, to_json
from pyspark.streaming import StreamingContext
import pyspark.sql.types as tp
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.feature import StopWordsRemover, Word2Vec, RegexTokenizer
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import Row
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.dataframe import DataFrame
from elasticsearch import Elasticsearch
import os
import time
import sys


es = Elasticsearch(hosts="http://host.docker.internal:9200")

tweetStruct = tp.StructType([
    tp.StructField(name = 'message', dataType= tp.StringType(), nullable = True)
])

tweetStruct2 = tp.StructType([
    tp.StructField(name = 'id', dataType= tp.StringType(), nullable = True),
    tp.StructField(name = 'text', dataType= tp.StringType(), nullable = True),
    tp.StructField(name = 'timestamp', dataType= tp.StringType(), nullable = True)
])

# Training Set Schema
schema = tp.StructType([
    tp.StructField(name= 'id', dataType= tp.StringType(), nullable = True),
    tp.StructField(name= 'text', dataType= tp.StringType(), nullable = True),
    tp.StructField(name= 'positive', dataType= tp.IntegerType(), nullable = True)
])

sc = SparkContext(appName="TweetGameSentimentAnalysis")
spark = SparkSession(sc)
sc.setLogLevel("WARN")

conf = SparkConf(loadDefaults=False)

training_set = spark.read.option("multiline","true").json('../../../opt/tap/.dataset/new_dataset.txt')
training_set.show()

tokenizer = Tokenizer(inputCol="text", outputCol="words")
hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
lr = LogisticRegression(labelCol= 'positive', maxIter=10, regParam=0.001)
pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

print("Pipeline done")

pipelineFit = pipeline.fit(training_set)

modelSummary=pipelineFit.stages[-1].summary
print("Accuracy:")
print(modelSummary.accuracy)

def elaborate(batch_df: DataFrame, batch_id: int):
    
    batch_df.show(truncate=False)
    if batch_df.rdd.isEmpty():
      print("Waiting for data ...")
    if not batch_df.rdd.isEmpty():
        print("Data received")

        data2=pipelineFit.transform(batch_df)
        #data2.show()
        
        data2.foreach(sendToEs)

def sendToEs(tweet):
    es = Elasticsearch(hosts="10.0.100.51")
    print("Sending to ES")

    jsonTweet={"doc": {"tweet":tweet.text,"prediction":tweet.prediction,"timestamp":tweet.timestamp}}
    print(jsonTweet)
    es.create(index="tweets", id=tweet.id, body=jsonTweet, ignore=409)

kafkaServer="kafkaServer:9092"
topic = "tap"

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafkaServer) \
  .option("subscribe", topic) \
  .option("startingOffsets", "earliest") \
  .option("maxOffsetsPerTrigger", 100) \
  .load()


df.printSchema()


df.selectExpr("CAST(value AS STRING)") \
    .select(from_json("value", tweetStruct, {"mode" : "FAILFAST"}).alias("data")) \
    .select("data.*") \
    .selectExpr("CAST(message AS STRING)") \
    .select(from_json("message", tweetStruct2, {"mode" : "FAILFAST"}).alias("data0")) \
    .select("data0.*") \
    .writeStream \
    .format("es") \
    .foreachBatch(elaborate) \
    .start() \
    .awaitTermination()
 