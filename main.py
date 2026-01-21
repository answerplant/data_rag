import ollama
import chromadb
from docx_parser import DocumentParser

documents = []
infile = 'test_docs/test_file.docx'
parsed_document = DocumentParser(infile)

"""
# Single document
document_builder_string = ''
for _type, item in parsed_document.parse():
    #print(_type, item["text"])
    if item["style_id"] == 'Normal':
      document_builder_string += (item["text"] + ' ')
print(document_builder_string)
documents.append(document_builder_string)
"""

# Multiple documents
for _type, item in parsed_document.parse():
    #print(_type, item["text"])
    if item["style_id"] == 'Normal':
      documents.append(item["text"])

client = chromadb.Client()
collection = client.create_collection(name="docs")

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
question = "Describe the MVP in 100 words."

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model="nomic-embed-text",
  input=question
)

results = collection.query(
  query_embeddings=[response["embeddings"][0]],
  n_results=1
)
data = results['documents'][0][0]

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model="llama2",
  prompt=f"Using this data: {data}. Respond to this prompt: {input}"
)

print(output['response'])
