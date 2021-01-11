from elasticsearch import Elasticsearch
from flask import Flask, render_template, jsonify, request
from transformers import pipeline, AlbertTokenizer, AlbertForQuestionAnswering
import torch

import json
import collections

indexName = 'triviaqa_wiki'

#Init Albert pipeline
qa_pipeline = pipeline('question-answering', model="ktrapeznikov/albert-xlarge-v2-squad-v2", tokenizer="albert-xlarge-v2", device=0)
question = "What is the capital of the Netherlands?"
context = r"The four largest cities in the Netherlands are Amsterdam, Rotterdam, The Hague and Utrecht.[17] Amsterdam is the country's most populous city and nominal capital,[18] while The Hague holds the seat of the States General, Cabinet and Supreme Court.[19] The Port of Rotterdam is the busiest seaport in Europe, and the busiest in any country outside East Asia and Southeast Asia, behind only China and Singapore."

initQA = qa_pipeline(question=question, context=context)

print(initQA)

# Grab Elasticsearch instance
config = {'host':'mc.ocbe.de', 'port':9200}
es = Elasticsearch([config])

# test connection
es.ping()

app = Flask(__name__)

@app.route("/")
def serve_app():
    return render_template('index.html')

@app.route("/upload")
def upload():
    return render_template('upload.html')

@app.route("/answer")
def answer():
    question = request.args.get('question')
    contextNString = request.args.get('context')
    print(question)
    print(contextNString)
    contextN = int(contextNString) 
    ## ElasticSearch part
    query = {
            'query': {
                'match': {
                    'text: ': question
                    }
                }
            }

    # execute query - Query Size K
    K = 10
    result = es.search(index=indexName, body=query, size=K) 

    predData = result['hits']['hits'][contextN]['_source']['text: ']

    predictions = qa_pipeline(question=question, context=predData)

    result = {'answer': predictions['answer'], 'prob': predictions['score']}

    return jsonify(result)

if __name__ == '__main__':
    app.run()