# hugging-face-text-embedding
Docker image to expose a basic text embedding API using all-MiniLM-L6-v2 model

# Repository

https://github.com/jgquiroga/hugging-face-text-embedding


# To run locally without docker

## For Windows

It is recommended to create a virtual environment.

To create a Virtual Environment:

```bash
python -m venv c:\path\to\myenv
```

To activate the Virtual Environment

```bash
.\.venv\Scripts\Activate.ps1
```

## Prerequisites

Install requirements:

```bash
pip install -r ./requirements.txt
```

## Run the application using uvicorn

```bash
uvicorn app.main:app --reload --port 8080 --host 0.0.0.0
```

# To build the image

```bash
docker build -t jgquiroga/hugging-face-text-embedding:v0.4.0 .
```

# To Push the image

```bash
docker push jgquiroga/hugging-face-text-embedding:v0.4.0
```

# To run the image
```bash
docker run --rm --name hugging-face-text-embedding -p 8080:80 jgquiroga/hugging-face-text-embedding:v0.4.0
```

# To test the api

## Open API

http://localhost:7860/docs

## Example Calls

```
curl --location 'http://127.0.0.1:8080/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2' \
--header 'Accept: application/json' \
--header 'Content-Type: application/json' \
--data '{
    "inputs": ["This is a test sentence"]
}'
```
# Usage with Semantic Kernel in dotnet

### usings:

```csharp
using System.Linq;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Embeddings;
using Microsoft.SemanticKernel.Memory;
using Microsoft.SemanticKernel.Connectors.HuggingFace;
```

```csharp
// Memory functionality is experimental
#pragma warning disable SKEXP0001, SKEXP0010, SKEXP0050

// HuggingFace functionality is experimental
#pragma warning disable SKEXP0020, SKEXP0070

var kernelBuilder = Kernel.CreateBuilder();

kernelBuilder.AddHuggingFaceTextEmbeddingGeneration(
    model: "sentence-transformers/all-MiniLM-L6-v2",
    endpoint: new Uri("http://127.0.0.1:8080")
);

var kernel = kernelBuilder.Build();

var memoryBuilder = new MemoryBuilder();
memoryBuilder.WithTextEmbeddingGeneration(kernel.GetRequiredService<ITextEmbeddingGenerationService>());
memoryBuilder.WithMemoryStore(new VolatileMemoryStore());
var memory = memoryBuilder.Build();
```

### Adding memories to a collection

```csharp
const string MemoryCollectionName = "aboutMe";

await memory.SaveInformationAsync(MemoryCollectionName, id: "info1", text: "My name is Andrea");
await memory.SaveInformationAsync(MemoryCollectionName, id: "info2", text: "I currently work as a tourist operator");
await memory.SaveInformationAsync(MemoryCollectionName, id: "info3", text: "I currently live in Seattle and have been living there since 2005");
await memory.SaveInformationAsync(MemoryCollectionName, id: "info4", text: "I visited France and Italy five times since 2015");
await memory.SaveInformationAsync(MemoryCollectionName, id: "info5", text: "My family is from New York");

```

### Searching the memory

```csharp
var questions = new[]
{
    "what is my name?",
    "where do I live?",
    "I live in",
    "where is my family from?",
    "where have I travelled?",
    "what do I do for work?",
};

foreach (var q in questions)
{
    
    var response = await memory.SearchAsync(MemoryCollectionName, q, minRelevanceScore: 0.5).FirstOrDefaultAsync();

    if (response == null)
    {
        Console.WriteLine(q + " " + "Not found");
    }
    else
    {
        Console.WriteLine(q + " " + response?.Metadata.Text);
    }
}
```