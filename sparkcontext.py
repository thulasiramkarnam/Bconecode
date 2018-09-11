
import pyspark
#import pandas
from pyspark import SparkContext
from pyspark.sql import SQLContext
sc = SparkContext(appName="PythonPi")
ab = sc.parallelize([1,2,3,4])
cd = ab.collect()
print (cd)
print ("After cd")
# sc = SparkContext("local", "simpleapp")
# df = pandas.read_excel(r"C:\Users\thulasiram.k\files\dummy.xlsx")
# sqlCtx = SQLContext(sc)
# print ("Before showing")
# sqlCtx.createDataFrame(df).show()