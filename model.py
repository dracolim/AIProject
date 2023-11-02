import os
import openai
import sys
import numpy as np
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
import langid
from deep_translator import GoogleTranslator

# to feed into the LLM model
def translateToEnglish(text: str) -> str:
    source = langid.classify(text)[0]
    #bergali => bangla
    if source == 'zh':
        source = 'zh-CN'
    if source == "en":
        return text

    answer = GoogleTranslator(source=source, target="en").translate(text)
    return answer

def clearChat():
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        input_key='question',
        output_key='answer'
    )
    return memory


def getResponse(question: str) -> str:
    """
    A repeated implementation of the langchain code in Week 5
    This code is purposely built to be inefficient! 
    Refer to project requirements and Week 5 Lab if you need help
    """    
    #load memory
    memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            input_key='question',
            output_key='answer'
    )

    #detect language (if it is not english, translate to english)
    question = translateToEnglish(question)
    if (question == "New Chat 🧹"):
        #clear memory
        memory.clear()
        return "Chat Cleared! Ask me anything about life in Singapore, or if you need help! \n"
    
    print(question)

    load_dotenv('./.env')

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LANGCHAIN_API_KEY = os.getenv('LANGSMITH_API_KEY')

    loader = PyPDFDirectoryLoader("./docs")
    index = VectorstoreIndexCreator().from_loaders([loader])
    pages = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len
    )

    splits = text_splitter.split_documents(pages)

    # Your experiment can start from this code block which loads the vector store into variable vectordb
    embedding = OpenAIEmbeddings()

    persist_directory = './vectordb'

    # Perform embeddings and store the vectors
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=persist_directory 
    )

    # query it
    query = "How many migrants are there in singapore?"
    docs = vectordb.similarity_search(query)


    # # Code below will enable tracing so we can take a deeper look into the chain
    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
    # os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

    # Define template prompt
    template = """You are a friendly chatbot that helps sad university students cope with their immense stress. 
    Use the following pieces of context to answer the question at the end.
    {context}
    Question: {question}
    Helpful Answer:"""

    your_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=template
    )

    # Define parameters for retrival
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    retriever=vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .8, "k": 5})

    # Define template prompt
    your_prompt = your_prompt

    # Execute chain
    qa = ConversationalRetrievalChain.from_llm(
        llm,
        combine_docs_chain_kwargs={"prompt": your_prompt},
        retriever=retriever,
        return_source_documents=True,
        memory=memory
    )


    # Evaluate your chatbot with questions
    result = qa({"question": question})

    print(result["answer"])
    return result['answer']