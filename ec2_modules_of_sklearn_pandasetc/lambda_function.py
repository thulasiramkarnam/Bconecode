import json
import logging
from bs4 import BeautifulSoup
import urllib
import requests
import re
import itertools
import pandas as pd 
import bs4
import sys
import imp
import sys
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
import nltk
from textblob import TextBlob
import textblob
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
logger = logging.getLogger()
logger.setLevel(logging.INFO)
def lambda_handler(event, context):
    # TODO implement
    try:
        
    logger.info(event)
    logger.info(type(event))
    logger.info("After event")
    return {
        "statusCode": 200,
        "body": json.dumps('Hello from Lambda!')
    }
