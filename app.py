from fastapi import FastAPI, Query
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
import os

# 🔑 Coloque sua OpenAI API Key nas variáveis de ambiente do Render depois!
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Cria a aplicação FastAPI
app = FastAPI()

# 🔥 Cria um agente
researcher = Agent(
    role="Pesquisador de dados",
    goal="Pesquisar e responder perguntas de forma precisa",
    backstory="Você é um assistente de IA altamente treinado, especialista em fornecer respostas baseadas em informações verificadas.",
    llm=ChatOpenAI(model="gpt-3.5-turbo"),
    verbose=True
)

# 🔥 Define a tarefa do agente
question_task = Task(
    description="Responder a pergunta fornecida de forma clara e precisa.",
    agent=researcher
)

# 🔥 Cria a Crew (time de agentes)
crew = Crew(
    agents=[researcher],
    tasks=[question_task],
    verbose=True
)

# 🚀 Endpoint simples
@app.get("/")
def read_root():
    return {"message": "CrewAI is running with FastAPI on Render"}

# 🚀 Endpoint para perguntar algo
@app.get("/ask")
def ask(question: str = Query(..., description="Sua pergunta")):
    # Atualiza a descrição da tarefa com a pergunta
    question_task.description = f"Responder a seguinte pergunta: {question}"
    
    # Executa o agente
    result = crew.run()
    
    return {"question": question, "response": result}

