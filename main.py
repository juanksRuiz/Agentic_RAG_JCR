from dotenv import load_dotenv
import os

# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings


from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_astradb import AstraDBVectorStore
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain import hub
from text_retrieval import load_pages

from note import note_tool

load_dotenv()

def connect_to_vstore():
    """Crea embeddings y una vector database con Astra db"""
    # Creation of set of embeddings
    embeddings = OpenAIEmbeddings() # funciona con OPENAI-API-KEY
    # Creación de un conjunto de embeddings usando HuggingFaceEmbeddings
    # embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # Modelo gratuito popular de Hugging Face
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None

    vstore = AstraDBVectorStore(
        embedding=embeddings
        ,collection_name='agentic_rag_jcr'
        ,api_endpoint=ASTRA_DB_API_ENDPOINT
        ,token=ASTRA_DB_APPLICATION_TOKEN
        ,namespace=ASTRA_DB_KEYSPACE
    )
    return vstore

# print(os.getenv("OPENAI_API_KEY"))
#print(f"ASTRA_DB_API_ENDPOINT: {os.getenv('ASTRA_DB_API_ENDPOINT')}")
#print(f"ASTRA_DB_APPLICATION_TOKEN: {os.getenv('ASTRA_DB_APPLICATION_TOKEN')}")
#print(f"ASTRA_DB_KEYSPACE: {os.getenv('ASTRA_DB_KEYSPACE')}")


vstore = connect_to_vstore()
# Se agrega documentos a la vector DB
# Ruta relativa al PDF
pdf_path = "./data/GallagherRe_report_2024.pdf"

pages = load_pages(pdf_path)
vstore.add_documents(pages)


"""
retriever = vstore.as_retriever(search_kwargs={"k":3})
retriever_tool = create_retriever_tool(
    retriever,
    "pdf_search", # name for the tool
    "Search for the information about insurance latest trends. For any issues about insurance latest trends, you must use this tool!", #what the tool actually does
)

prompt = hub.pull('hwchase17/openai-functions-agent')

llm = ChatOpenAI()

# Tools, herramientas necesarias del agente
tools = [retriever_tool, note_tool] # listado de tools
agent = create_tool_calling_agent(llm, tools, prompt) # Creacion de agente con llm, las tools y un prompt
# Ejecutor de agente para poder usarlo - verbose es el detalle del proceso de razonamiento
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

while (question := input("Ask a question about githubissues (q to quit): ")) != "q":
    result = agent_executor.invoke({"input": question})
    print(result["output"])"
"""