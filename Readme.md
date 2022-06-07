# Spanish QA (TranslateAlignRetrieve)

This model is obtained with the training corpus and scripts used in the project TranslateAlignRetrieve. This tool is used to obtain a Spanish version of the SQUAD dataset. The original code can be found [here](https://github.com/ccasimiro88/TranslateAlignRetrieve)

# Introduction

Instructions to train a model and build a dockerfile using the Spanish QA dataset


# Setup the project for training a Q/A model

Do this only if you want to train your own QA model

1) Setup the project first (do it only once). You can skip this part if you have a trained model

```
bash setup_project.sh
```

2) Train a mBERT like model (using nohup to leave the process in background)

```
nohup bash train_m_bert.sh  SQuAD-es-v2.0/train-v2.0-es.json SQuAD-es-v2.0/dev-v2.0-es.json v2 > nohup_squad_v2.out &

```

# Try the system without docker 

_NOTE: To try this you have to install the requirements.txt in your environment (*check setup_project.sh* script)_

Place the trained model inside the scripts folder and point the property *model_name_or_path* config file in *config/config.yml* to the trained model. 

Go to the scripts folder and execute the serve.py script

```
python serve.py
```

Try the system with the following query:

```
curl -X POST http://0.0.0.0:8866/process -H 'Content-Type: application/json' -d '{"type": "structuredText","texts":[{"content": "La capital de España es Madrid."}, {"content": "Cuál es la capital de España?"}]}'

```

This request is a *structuredText* type. The first element of *texts* is the context and the second is the query.


You will get an annotations response like this one:

```
{"response":{"type":"annotations","annotations":{"answers":[{"start":24,"end":30,"features":{"answer":"Madrid.","score":0.9910870068781747}}]}}}

```

# Build the dockerfile

Place the trained model inside the scripts folder and point the property *model_name_or_path* config file in *config/config.yml* to the trained model. 

Build the docker

```
source docker-builder.sh
```

# Run the dockerfile

```
docker run --rm -p 0.0.0.0:8866:8866 --name spanishqa elg_spanish_qa_dataset
```

# Test API (ELG Format)

In the folder `test` you have the files for testing the API according to the ELG specifications.

It uses an API that acts as a proxy with your dockerized API that checks both the requests and the responses.
For this process, follow the instructions:

1) Configure the .env file with the data of the image and your API
2) Launch the test: `docker-compose up`
3) Make the requests, instead of to your API's endpoint, to the test's endpoint:
   ```
     curl -X POST http://0.0.0.0:8866/processText/service -H 'Content-Type: application/json' -d '{"type": "structuredText","texts":[{"content": "La capital de España es Madrid."}, {"content": "Cuál es la capital de España?"}]}'

   ```
4) If your request and the API's response is compliance with the ELG API, you will receive the response.
   1) If the request is incorrect: Probably you will don't have a response and the test tool will not show any message in logs.
   2) If the response is incorrect: You will see in the logs that the request is proxied to your API, that it answers, but the test tool does not accept that response. You must analyze the logs.

## Citations
The original work of TranslateAlignRetrieve is presented in this paper :

- Carrino, C. P., Costa-jussà, M. R., & Fonollosa, J. A. (2019). Automatic spanish translation of the squad dataset for multilingual question answering. arXiv preprint arXiv:1912.05200.

The original work has MIT License