import os

import streamlit as st
from crewai import Crew
from crewai_tools import (
    FileReadTool,
    MDXSearchTool,
    ScrapeWebsiteTool,
    SerperDevTool,
)
from dotenv import load_dotenv
from PIL import Image

from agents import MultiAgents
from tasks import MultiTasks

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
agents = MultiAgents()
tasks = MultiTasks()

imagem_icon = Image.open("src/assistente-de-robo.png")


def save_uploaded_file(uploaded_file):
    """
    Salva o arquivo carregado temporariamente e retorna o caminho do arquivo.

    Args:
        uploaded_file (UploadedFile): O arquivo carregado pelo Streamlit.

    Returns:
        str: O caminho do arquivo salvo.
    """
    temp_dir = "tempDir"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    temp_file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path


def read_file(file_path):
    """
    Lê o conteúdo de um arquivo PDF ou DOCX usando FileReadTool e retorna o
    texto contido nele.

    Args:
        file_path (str): O caminho do arquivo a ser lido.

    Returns:
        str: O texto extraído do arquivo.
    """
    file_read_tool = FileReadTool(file_path=file_path)
    return file_read_tool


def main():
    with st.sidebar:
        st.title("Olá, Sou o Taylor IA,  seu consultor de carreira:")
        st.write(
            """Estou aqui para ajudá-lo a destacar suas habilidades e
            experiências para o mercado de trabalho."""
        )
        st.image(imagem_icon, use_column_width=True)

    st.header("Consultor de Carreira")
    candidate_name = st.text_input("Digite seu nome:")
    job_posting_url = st.text_input("Informe a URL da vaga desejada:")
    github_url = st.text_input("Informe a URL do seu Github:")
    uploaded_resume = st.file_uploader(
        "Por favor, faça o upload do seu currículo nos formatos PDF ou DOCX.",
        type=["pdf", "docx"],
    )
    resume_text = ""
    if uploaded_resume:
        if uploaded_resume.type == "application/pdf":
            temp_file_path = save_uploaded_file(uploaded_resume)
            resume_text = read_file(temp_file_path)
            os.remove(temp_file_path)

    if st.button("Realizar Análise"):
        if (
            candidate_name
            and uploaded_resume
            and job_posting_url
            and github_url
        ):

            read_resume = resume_text
            semantic_search_resume = MDXSearchTool(resume_text)
            search_tool = SerperDevTool()
            scrape_tool = ScrapeWebsiteTool()

            # Agents
            researcher = agents.researcher(search_tool, scrape_tool)
            profile_creator = agents.profile_creator(
                search_tool, scrape_tool, read_resume, semantic_search_resume
            )
            professional_consultant = agents.professional_consultant(
                search_tool, scrape_tool, read_resume, semantic_search_resume
            )
            interview_preparer = agents.interview_preparer(
                search_tool, scrape_tool, read_resume, semantic_search_resume
            )

            # Tasks
            research_task = tasks.research_task(researcher, job_posting_url)
            profile_manager_task = tasks.profile_manager_task(
                profile_creator, github_url
            )
            resume_adaptation_task = tasks.resume_adaptation_task(
                candidate_name, professional_consultant, profile_manager_task
            )
            interview_preparation_task = tasks.interview_preparation_task(
                interview_preparer,
                research_task,
                profile_manager_task,
                resume_adaptation_task,
            )

            crew = Crew(
                agents=[
                    researcher,
                    profile_creator,
                    professional_consultant,
                    interview_preparer,
                ],
                tasks=[
                    research_task,
                    profile_manager_task,
                    resume_adaptation_task,
                    interview_preparation_task,
                ],
                verbose=True,
            )

            st.sucess(f"Obrigado, {candidate_name}! Aguarde a análise...")

        else:
            st.error(
                """Por favor, preecha todas as informações e faça o upload do
                currículo"""
            )

            inputs = {
                "candidate_name": candidate_name,
                "job_posting_url": job_posting_url,
                "github_url": github_url,
                "uploaded_resume": uploaded_resume,
            }

            st.write(crew.kickoff(inputs=inputs))


if __name__ == "__main__":
    main()
