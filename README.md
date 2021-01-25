# ElasticAlbert
Question answering is one of the oldest tasks of natural language processing (NLP), which is concerned with answering questions asked by users in natural language.
While the question answering area already exceeds human performance like the Retro-Reader on the Stanford Question Answering Dataset (SQuAD) 2.0, open-domain question answering is still lacking in performance.

The biggest issue of current question answering models is primarily their computing time performance which makes them unusable in real world applications. State-of-the-art question answering models which lead the SQuAD 2.0 rankings are trained to answer questions on small text corpuses, such as a single wikipedia article. With the length of the text corpus, the model’s response time increases exponentially due to increased computation time.

To reduce the response time of current question answering models, this project introduces ElasticAlbert. In order to improve the performance, a question answering model is prepended with a retriever which pre-selects only relevant articles for the question answering model.

For this purpose, ElasticAlbert uses Elasticsearch as a retriever. Elasticsearch indexes the entire document dataset in advance and delivers the best K articles or passages that match the question based on the BM25 algorithm. These best K articles are used in a second step to be evaluated by a generator like in a usual question answering model. This generator generates a specific answer to each pre-selected article and receives a score by which these are ranked. The article with the highest score is assumed to be the correct answer.

The generator used by ElasticAlbert is ALBERT. ALBERT or “A Lite BERT” is a more advanced variation of the BERT model. Like BERT, ALBERT is a sequence2sequence transformer model that can be fine-tuned to different NLP tasks. Since the generator here is responsible for question answering, an ALBERT model is used that was trained on question answering using the SQuAD 2.0 dataset.

To measure the performance of ElasticAlbert, the TriviaQA dataset is used, which is typical for open-domain question answering. TriviaQA is a dataset that contains 95 thousand question-answer pairs based on 480 thousand articles. These 480 thousand articles are divided into 80 thousand Wikipedia articles and 400 thousand articles obtained by crawling other websites. The tests focus on how the number K of articles received affects the general accuracy of ElasticAlbert. This is necessary in order to have a basis for decision for a later deployment, since a higher K increases the accuracy, but also the computing time.

The goal of ElasticAlbert is to work as an end-to-end system. As shown in a proof of concept, ElasticAlbert is thus able to answer questions from users in real time with a reasonable level of accuracy on a large decision base of over 480,000 articles. For this purpose, users can add additional articles via a RESTful API or an upload user interface. These new articles and the TriviaQA dataset can then be queried in real time via a search user interface that accepts natural queries from users.

In summary, this approach tries to make open domain question answering applicable, since the long computing time of parametric question answering systems is significantly reduced by using a non-parametric retriever.
