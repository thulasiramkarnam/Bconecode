
import pyspark
import requests
import pandas
import boto3
from pyspark import SparkContext
from pyspark.sql import SQLContext

df = pandas.read_excel(r"https://s3-eu-west-1.amazonaws.com/thulasi-ram-dum/dummy.xlsx")
sqlCtx = SQLContext(sc)
sqlCtx.createDataFrame(df).show()