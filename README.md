# hugging-face-text-embedding
Docker image to expose a basic text embedding API using all-MiniLM-L6-v2 model

# Repository

https://github.com/jgquiroga/hugging-face-text-embedding

# To build the image

```bash
docker build -t jgquiroga/hugging-face-text-embedding:v0.1.0 .
```

# To Push the image

```bash
docker push jgquiroga/hugging-face-text-embedding:v0.1.0
```

# To run the image
```bash
docker run -d --name hugging-face-text-embedding -p 7860:80 jgquiroga/hugging-face-text-embedding:v0.1.0
```

# To test the api

## Open API

http://localhost:7860/docs

## Example Calls

```
curl --location 'http://127.0.0.1:7860/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "inputs": ["This is a test sentence"]
}'
```


```
curl --location 'http://127.0.0.1:7860/semantic-kernel/sentence-transformers/all-MiniLM-L6-v2' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "inputs": ["This is a test sentence"]
}'
```
