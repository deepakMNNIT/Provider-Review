from flask import Flask,render_template,request
import pickle
from nltk.classify import ClassifierI
from statistics import mode
from nltk.tokenize import word_tokenize

from py_files.NegationHandling import AntonymReplacer
from py_files.database import engine, db_session, init_db
#from schema import schema
import py_files.schema
import json

from flask_graphql import GraphQLView

app = Flask(__name__)
app.debug = True

def init():
    global connection, cursor
    connection = engine.raw_connection()
#    connection = psycopg2.connect(database="postgres", user = "postgres", password = "8991Ngu@007", host = "localhost", port = 5432)
    cursor = connection.cursor()
    
    class VoteClassifier(ClassifierI):
        def __init__(self, *classifiers):
            self._classifiers = classifiers
    
        def classify(self, features):
            votes = []
            for c in self._classifiers:
                v = c.classify(features)
                votes.append(v)
            return mode(votes)
    
        def confidence(self, features):
            votes = []
            for c in self._classifiers:
                v = c.classify(features)
                votes.append(v)
    
            choice_votes = votes.count(mode(votes))
            conf = choice_votes / len(votes)
            return conf
     
        
    word_features = pickle.load(open("pickled_algos/word_features5k.pickle", "rb"))

    classifier = pickle.load(open("pickled_algos/originalnaivebayes5k.pickle", "rb"))

    MNB_classifier = pickle.load(open("pickled_algos/MNB_classifier5k.pickle", "rb"))

    BernoulliNB_classifier = pickle.load(open("pickled_algos/BernoulliNB_classifier5k.pickle", "rb"))

    LogisticRegression_classifier = pickle.load(open("pickled_algos/LogisticRegression_classifier5k.pickle", "rb"))

    LinearSVC_classifier = pickle.load(open("pickled_algos/LinearSVC_classifier5k.pickle", "rb"))


    class X :
        global find_features, sentiment
        def find_features(document):
            words = word_tokenize(document)
            features = {}
            for w in word_features:
                features[w] = (w in words)       
            return features
        
        def sentiment(text):
            rep = AntonymReplacer()
            text = rep.negreplacer(text)
            feats = find_features(text)        
            return voted_classifier.classify(feats)#,voted_classifier.confidence(feats)
         
    voted_classifier = VoteClassifier(
                                      classifier,
                                      LinearSVC_classifier,
                                      MNB_classifier,
                                      BernoulliNB_classifier,
                                      LogisticRegression_classifier)


example_query = """
query{
  allProviderReviews(pId: 1000){
    edges{
      node{
        pId
        review
        result
        provider{
          providerId
          firstName
          lastName
        }
      }
    }
  }
}
"""

mutation_query = """
mutation{
    addReview(pId : 1003, review: "It's rude, misleading and utter junk.", result:"") {
         post {
                pId
                review
              }
  }  
}
"""


q = """
query{ 
  allProviderReviews(pId: $pId){
    edges{
      node{
        pId,
        review,
        result
        }
      }
    }
  }
"""
variables = {"pId": "1000"}
def function(query , occurrence , substr):
 inilist = [i for i in range(0, len(query)) 
 if query[i:].startswith(substr)] 
 return inilist[occurrence-1]

@app.route('/', methods = ['POST'])
def graphql():
    
    if(request.method == 'POST'):
        request_query = request.get_json()
        query = request_query['query']
        if(query.find('mutation') > -1):   
                var = request_query['variables']
                provId = var['pId']
                rvw = var['review']                
                if(rvw != ''):
                    rslt = sentiment(rvw) #calculated result
                else:
                    rslt = var['result']
                
                mut_string = '''
                mutation addResult($pId : Int!, $review : String!, $result : String!){
                    addReview(pId : $pId, review : $review, result : $result) {
                        post {
                            pId,
                            review,
                            result
                        }
                    }
                }
                '''
                fin_result = py_files.schema.schema.execute(mut_string,variables={
                    
                        'pId': provId,
                        'review': rvw,
                        'result': rslt
                    
                },)
                
                d = json.dumps(fin_result.data)
                d = json.loads(d)
                
                d1 = {}
                d1["data"] = d
                return d1
                
                # d = json.dumps(fin_result.data)
                # return '{}'.format(d)
           
        elif(query.find('allProviderReviews')>-1):
                var1 = request_query['variables']
                fin_result1 = py_files.schema.schema.execute(query, variables = var1,)
                dd = json.dumps(fin_result1.data)
                dd = json.loads(dd)
                
                d2 = {}
                d2["data"] = dd
                return d2
        else :
                fin_result2 = py_files.schema.schema.execute(query)
                dd = json.dumps(fin_result2.data)
                dd = json.loads(dd)
                
                d3 = {}
                d3["data"] = dd
                return d3

# app.add_url_rule('/', 'graphql', graphql)
# app.view_functions['graphql'] = graphql     

# app.add_url_rule(
#     '/',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=schema.schema,
#         #graphiql=True # for having the GraphiQL interface
#     )
# )

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
#    init_db()
   init()
   app.run()
