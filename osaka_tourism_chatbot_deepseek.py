import streamlit as st
import os
from haystack import Pipeline
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from haystack_integrations.document_stores.mongodb_atlas import MongoDBAtlasDocumentStore
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack_integrations.components.retrievers.mongodb_atlas import MongoDBAtlasEmbeddingRetriever

from haystack.utils import Secret
import re

os.environ["MONGO_CONNECTION_STRING"] = "MONGO_CONNECTION"

# Initialize session state for document store and pipeline store if they don't exist
if 'document_store' not in st.session_state:
    st.session_state.document_store = MongoDBAtlasDocumentStore(
        database_name="keisuu",
        collection_name="osaka_tourism_en",
        vector_search_index="vector_index",
    )

if 'pipeline_retrieve' not in st.session_state:
    template = """
    given these documents, answer the question below. Documents:
    {% for document in documents %}
        {{ document.content }}
    {% endfor %}
    Question: {{query}}

    please answer the question directly and don't use intro like: "The answer to your question is "
    """
    pipeline_retrieve = Pipeline()
    pipeline_retrieve.add_component("embedder",SentenceTransformersTextEmbedder())
    pipeline_retrieve.add_component("retriever",MongoDBAtlasEmbeddingRetriever(document_store=st.session_state.document_store,top_k=5))
    pipeline_retrieve.add_component("builder",PromptBuilder(template=template))
    pipeline_retrieve.add_component("generator",OllamaGenerator(model="llama3.2:1b",url="http://IP_ADDRESS:11434/api/generate",generation_kwargs={
        "num_predict":-2,
        "temperature":0.9,
    },timeout=1200))
    pipeline_retrieve.connect("embedder","retriever")
    pipeline_retrieve.connect("retriever","builder")
    pipeline_retrieve.connect("builder","generator")
    st.session_state.pipeline_retrieve = pipeline_retrieve

    

# Retrieve from session state
document_store = st.session_state.document_store
pipeline_retrieve = st.session_state.pipeline_retrieve
st.title("RAG Demo")
st.header("Osaka Tourism Information (with DeepSeek-R1:1.5b)", divider="rainbow")
query = st.text_input("Enter your question here")
if st.button("Generate Answer"):
    result = pipeline_retrieve.run({
        "embedder":{"text":query},
        "builder":{"query":query}
    })
    result_text = result["generator"]["replies"][0]
    only_answer = clean_text = re.sub(r"<think>.*?</think>\s*", "", result_text, flags=re.DOTALL)
    st.write(only_answer)
    # st.write(result)