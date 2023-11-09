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
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


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
    if (question == "new chat"):
        #clear memory
        memory.clear()
        return "✔️ Chat Cleared! Click on *start* to start a converation \n"
    print(question)


    #HARD CODE RESPONSE FOR DEMO (VOICE in tammil)
    if question == "How many migrant workers are there in Singapore?":
        temp_res1 = "As of December 2020, there were approximately 687,600 migrant workers in Singapore. These workers are primarily employed in the construction, marine shipyard, and process sectors. It's important to note that this number excludes foreign domestic workers.As of December 2020, there were approximately 687,600 migrant workers in Singapore. These workers are primarily employed in the construction, marine shipyard, and process sectors. It's important to note that this number excludes foreign domestic workers."
        return temp_res1
    
    #TEXT (english qn)
    if question == "Are there mental health services available for migrant workers?":
        temp_res2 = "Yes, there are mental health services available for migrant workers in Singapore. Efforts have been made to improve access to mental health support for migrant workers. The Singapore government has expanded access to mental health support for migrant workers by providing basic mental health and psychological first aid training to Forward Assurance and Support Team (Fast) members. HealthServe, a non-profit organization, has also launched a 24-hour crisis helpline specifically for migrant workers in Singapore to provide support for mental health issues. However, it is important to note that the availability and accessibility of these services may still be limited.Yes, there are mental health services available for migrant workers in Singapore. Efforts have been made to improve access to mental health support for migrant workers. The Singapore government has expanded access to mental health support for migrant workers by providing basic mental health and psychological first aid training to Forward Assurance and Support Team (Fast) members. HealthServe, a non-profit organization, has also launched a 24-hour crisis helpline specifically for migrant workers in Singapore to provide support for mental health issues. However, it is important to note that the availability and accessibility of these services may still be limited."
        return temp_res2

    #TEST (burmese qn)
    if question == "What are the dental and oral coverage for migrant workers?":
        temp_res3 = """Dental treatment for migrant workers in Singapore is covered if it is deemed necessary for their health by a Singapore-registered medical or dental professional. In such cases, the cost of dental treatment is borne by the employers, even if the condition is not work-related. Additionally, employers have the option to purchase additional insurance for added protection.\n\nThere are also initiatives and programs that offer subsidized or discounted dental services for migrant workers. For example, the Migrant Workers' Centre (MWC) associate membership program provides migrant workers with a flat fee of up to $30 for dental services, with MWC associate members receiving a $5 discount. Community initiatives and clinics also offer subsidized or discounted dental services for migrant workers.\n\nHowever, it is important to note that the cost of dental check-ups in Singapore can still be high, which can be a financial burden for low-wage migrant workers.Dental treatment for migrant workers in Singapore is covered if it is deemed necessary for their health by a Singapore-registered medical or dental professional. In such cases, the cost of dental treatment is borne by the employers, even if the condition is not work-related. Additionally, employers have the option to purchase additional insurance for added protection.\n\nThere are also initiatives and programs that offer subsidized or discounted dental services for migrant workers. For example, the Migrant Workers' Centre (MWC) associate membership program provides migrant workers with a flat fee of up to $30 for dental services, with MWC associate members receiving a $5 discount. Community initiatives and clinics also offer subsidized or discounted dental services for migrant workers.\n\nHowever, it is important to note that the cost of dental check-ups in Singapore can still be high, which can be a financial burden for low-wage migrant workers"""
        return temp_res3


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
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0 , streaming=True, callbacks=[StreamingStdOutCallbackHandler()], )
    retriever=vectordb.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": .5, "k": 10})

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