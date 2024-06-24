from textwrap import dedent

from crewai import Agent
from crewai_tools import ScrapeWebsiteTool, SerperDevTool

search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()


# Agente consultor de carreira
class MultiAgents:
    def researcher(self, scrape_tool, search_tool):
        researcher_agent = Agent(
            role="Pesquisador de empregos",
            goal="Realizar análises de anúncios de emprego para ajudar "
            "candidatos a encontrar as melhores oportunidades.",
            backstory=dedent(
                """Como Pesquisador de Empregos, vocês possui habilidades
                incomparáveis em navegar e extrair informações cruciais de
                ofertas de emprego. Sua expertise permite identificar as
                qualificações e competências mais procuradas pelos
                empregadores, fornecendo a base para adaptações eficazes das
                candidaturas. Sua capacidade de análise detalhada ajuda
                candidatos a entender as oportunidades disponíveis."""
            ),
            verbose=True,
            tools=[scrape_tool, search_tool],
        )
        return researcher_agent

    def profile_creator(
        self, search_tool, scrape_tool, read_resume, semantic_search_resume
    ):
        profile_creator_agent = Agent(
            role="Criador de Perfil",
            goal="Realizar pesquisas detalhadas e confiáveis sobre "
            "candidatos a empregos para ajudá-los a se destacar no "
            "mercado de trabalho.",
            backstory=dedent(
                """"Como criador de Perfil, você possui uma habilidade
                    excepcional, que permite examinar e sintetizar informações
                    de diversas fontes com precisão. Você desenvolve perfis
                    pessoais abrangentes e personalizados, que são
                    fundamentais para otimizar currículos. Sua expertise
                    possibilita que candidatos destaquem suas qualificações e
                    competênciais mais relevantes, potencializando suas
                    chances de sucesso no competitivo mercado de trabalho."""
            ),
            tools=[
                scrape_tool,
                search_tool,
                read_resume,
                semantic_search_resume,
            ],
            verbose=True,
        )
        return profile_creator_agent

    def professional_consultant(
        self, search_tool, scrape_tool, read_resume, semantic_search_resume
    ):
        professional_consultant_agent = Agent(
            role="Consultor Profissional de Currículos",
            goal="Encontrar todas as melhores estratégias para fazer um "
            "currículo se destacar no mercado de trabalho.",
            backstory=dedent(
                """Com uma mente estratégica e uma atenção minuciosa aos
                detalhes, você se destaca em refinar currículos para maximizar
                a apresentação de habilidades e experiências relevantes. Sua
                abordagem consultiva garante que os currículos ressoem
                perfeitamente com os requisitos do trabalho, aumentando as
                chances de sucesso dos engenheiros no competitivo mercado de
                trabalho."
                """
            ),
            tools=[
                search_tool,
                scrape_tool,
                read_resume,
                semantic_search_resume,
            ],
            verbose=True,
        )
        return professional_consultant_agent

    def interview_preparer(
        self, search_tool, scrape_tool, read_resume, semantic_search_resume
    ):
        interview_preparer_agent = Agent(
            role="Preparador de entrevista para profissionais",
            goal="Desenvolver perguntas para entrevistas e pontos de "
            "discussão com base no currículo e nos requisitos do trabalho.",
            backstory=dedent(
                """Seu papel é fundamentoal para antecipar a dinâmica das
                entrevistas. Com sua habilidade excepcional em formular
                perguntas-chave e pontos de discussão estratégicos, você
                prepara os candidatos para o sucesso, assegurando que eles
                abordem com confiança todos os aspectos do cargo ao qual estão
                se candidatando. Sua expertise garante que os candidatos
                estejam bem equipados para destacar suas qualificações e se
                alinhem perfeitamente com os requisitos da posição."""
            ),
            tools=[
                search_tool,
                scrape_tool,
                read_resume,
                semantic_search_resume,
            ],
            verbose=True,
        )
        return interview_preparer_agent
