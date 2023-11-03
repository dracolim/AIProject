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

#GLOBAL LOADER SPLITTER
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


def getResponse(question: str) -> str:
    """
    A repeated implementation of the langchain code in Week 5
    This code is purposely built to be inefficient! 
    Refer to project requirements and Week 5 Lab if you need help
    """    
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
        return "Chat Cleared! Ask me anything about life in Singapore, or any questions! \n"
    print(question)
    

    # # Code below will enable tracing so we can take a deeper look into the chain
    # os.environ["LANGCHAIN_TRACING_V2"] = "true"
    # os.environ["LANGCHAIN_ENDPOINT"] = "https://api.langchain.plus"
    # os.environ["LANGCHAIN_PROJECT"] = "Chatbot"

    # Define template prompt
    template = """
        Act as a friendly chatbot who is trying to help a migrant worker settle down in Singapore and as a chatbot,
        you are suppose to provide concise, substantial, useful and easy to understand answers with sufficient information that can help them.
        Use the following pieces of context to answer the questions.
        If you don't know the answer or the question is out of context, just say "If I am not able to address your enquiry, you may visit to https://www.healthserve.org.sg/ for more information or contact us at +65 3129 5000", don't try to make up an answer.
        -----------
        <ctx>
        {context}
        </ctx>
        -----------
        Question: {question}
        Answer:
    """""

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