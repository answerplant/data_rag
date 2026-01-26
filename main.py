import os
import ollama
import chromadb
from docx_parser import DocumentParser
from langchain_text_splitters import RecursiveCharacterTextSplitter

DB_PATH = 'db/'
IN_PATH = 'test_docs/'
EMBEDDINGS_MODEL = 'mxbai-embed-large' #'nomic-embed-text'
CHAT_MODEL = 'llama3'

documents = []
text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)

for file in os.listdir(IN_PATH):
  filename = os.fsdecode(file)
  if filename.endswith(".docx"):
    parsed_document = DocumentParser(IN_PATH + filename)
    for _type, item in parsed_document.parse():
      if _type == "paragraph":
        if item["style_id"] == 'Normal':
          #documents.append(text_splitter.split_text(item["text"]))
          #print(text_splitter.split_text(item["text"]))
          chunk_list = text_splitter.split_text(item["text"])
          for chunk in chunk_list:
            documents.append(chunk)


#client = chromadb.PersistentClient(path=DB_PATH)
client = chromadb.Client()
collection = client.create_collection(name="data_docs")

# store each document in a vector embedding database
for i, d in enumerate(documents):
  response = ollama.embed(model=EMBEDDINGS_MODEL, input=d)
  embeddings = response["embeddings"]
  collection.add(
    ids=[str(i)],
    embeddings=embeddings,
    documents=[d]
  )

# an example input
#print("Enter a prompt:")
#question = input().strip()
question = "Has Answer Digital worked with NHS England Analytical teams?"

# generate an embedding for the input and retrieve the most relevant doc
response = ollama.embed(
  model=EMBEDDINGS_MODEL,
  input=question
)

results = collection.query(
  query_embeddings=[response["embeddings"][0]], # Index relevant depending on document structure
  n_results=1
)
data = results['documents'][0][0]

# generate a response combining the prompt and data we retrieved in step 2
output = ollama.generate(
  model=CHAT_MODEL,
  prompt=f"Using this data: {data}. Respond to this prompt: {input}"
)

print(output['response'])
