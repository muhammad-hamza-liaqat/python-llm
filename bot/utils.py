import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DB_DIR = os.path.join(os.getcwd(), "chroma_db")


def get_embeddings():

    return OpenAIEmbeddings()


def get_vectorstore():
    return Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=get_embeddings()
    )


def save_to_vectorstore(content_list, metadatas):

    embeddings = get_embeddings()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    texts = []
    metadata_chunks = []
    for content, metadata in zip(content_list, metadatas):
        chunks = splitter.split_text(content)
        texts.extend(chunks)
        metadata_chunks.extend([metadata] * len(chunks))

    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )

    vectorstore.add_texts(texts=texts, metadatas=metadata_chunks)

    return vectorstore


def search_in_vectorstore(query, k=3):

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    results = retriever.invoke(query)
    return results
