import pprint
import schema
import json

def query_url():
   rvw = 'Boring and filthy.'
   rslt = 'neg'
   
   q_string = '''
    mutation addResult($pId : Int!, $review : String!, $result : String!){
        addReview(pId : $pId, review : $review, result : $result) {
            post {
                review
                result
            }
        }
    }
    '''
   result = schema.schema.execute(q_string,variables={
        
            'pId': 1000,
            'review': rvw,
            'result': rslt
        
    },)
   if result.errors:
        if len(result.errors) == 1:
            raise Exception(result.errors[0])
        else:
            raise Exception(result.errors)
   d = json.dumps(result.data)
   return '{}'.format(d)


if __name__ == "__main__":
    results = query_url()
    pprint.pprint(results)