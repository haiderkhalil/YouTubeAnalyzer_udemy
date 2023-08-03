from langchain.embeddings.openai import OpenAIEmbeddings 
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
import os
import youtube_transcriptor as trans
import shutil
from dotenv import load_dotenv
import requests_cache
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI


load_dotenv()

def create_db_and_analye(video_url):
    

    os.environ["OPENAI_API_KEY"] = os.environ.get('OPENAI_API_KEY')
    if os.path.exists('db'):
        shutil.rmtree('db')
    requests_cache.clear()
    transcript=trans.get_transcript(video_url)

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    texts = text_splitter.split_text(transcript)

    embeddings = OpenAIEmbeddings()

    db = Chroma.from_texts(texts, 
                                embeddings, 
                                metadatas=[{"source": f"Text chunk {i} of {len(texts)}"} for i in range(len(texts))], 
                                persist_directory="db")
    db.persist()


    docsearch = Chroma(persist_directory="db", embedding_function=embeddings)

    chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), 
                                                        chain_type="stuff", 
                                                        retriever=docsearch.as_retriever(search_kwargs={"k": 1}))
    
    user_query = "Summarize the content and give me a brief summary."
    result = chain({"question": user_query}, return_only_outputs=True)
    print(result["answer"])
    db = None
    return result["answer"]



    
 