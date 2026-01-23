import os
import ollama
import chromadb
from docx_parser import DocumentParser

documents = []
inpath = 'test_docs/'
#infile = 'test_docs/test_file.docx'

for file in os.listdir(inpath):
  filename = os.fsdecode(file)
  if filename.endswith(".docx"):
    parsed_document = DocumentParser(inpath + filename)
    for _type, item in parsed_document.parse():
      #print(_type, item["text"])
      print(filename, _type)
      if _type == "paragraph":
        print(item)
        if item["style_id"] == 'Normal':
          documents.append(item["text"])

print(documents)
"""
client = chromadb.Client()
collection = client.create_collection(name="data_docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embed(model="nomic-embed-text", input=d)
  embeddings = response["embeddings"]
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    documents=[d]
  )

# an example input
print("Enter a prompt:")
question = input().strip()

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model="nomic-embed-text",
  input=question
)

results = collection.query(
  query_embeddings=[response["embeddings"][0]], # Index relevant depending on document structure
  n_results=1
)
data = results['documents'][0][0]

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama3",
  prompt=f"Using this data: {data}. Respond to this prompt: {input}"
)

print(output['response'])
"""