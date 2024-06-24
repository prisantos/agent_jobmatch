from textwrap import dedent

from crewai import Task


class MultiTasks:
    def job_research_task(self, agent, job_posting_url):
        description = dedent(
            """Examine a URL do anúncio do emprego fornecido
                ({job_posting_url}) para extrair as habilidades, experiências
                e qualificações essenciais exigidas. Utilize as ferramentas
                disponíveis para coletar e analisar o conteúdo, identificando
                e categorizando os requisitos de forma eficiente."""
        )
        expected_output = dedent(
            """Uma lista estruturada de requisitos do trabalho, incluindo
                as habilidades, qualificações e experiências necessárias."""
        )
        job_research_task = Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            async_execution=True,
        )
        return job_research_task

    def profile_manager_task(self, agent, github_url):
        description = dedent(
            """Elabore um perfil pessoal e profissional detalhado a partir dos
            URLs do GitHub ({github_url}. Utilize ferramentas especializadas
            para extrair e sintetizar informações dessas fontes de forma
            eficiente
            """
        )
        expected_output = dedent(
            """Um perfil detalhado que abrange habilidades, experiências em
            projetos, contribuições, interesse e estilo de comuniçação.
            """
        )
        profile_manager_task = Task(
            description=description,
            expected_output=expected_output,
            agent=agent,
            async_execution=True,
        )
        return profile_manager_task

    def resume_adaptation_task(
        self,
        candidate_name,
        agent,
        tarefa_pesquisador,
        tarefa_gerenciador_perfil,
    ):
        description = dedent(
            """Usando o perfil e os requisitos de trabalho obtidos em tarefas
            anteriores, adapte o currículo para destacar ao máximo áreas
            relevantes. Utilize ferramentas para ajustar e melhorar o
            conteúdo, assegurando que este seja o melhor currículo possível
            sem inventar nenhuma informação. Atualize todas as seções,
            incluindo o resumo inicial, experiência profissional, habilidades
            e educação, para refletir melhor as habilidades do candidato e
            alinhar-se aos requisitos do anúncio de emprego."""
        )
        expected_output = dedent(
            """Um currículo atualizado que destaque efetivamente as
            qualificações, características e experiências relevantes do
            candidato para o trabalho."""
        )
        resume_adaptation_task = Task(
            description=description,
            expected_output=expected_output,
            context=[tarefa_pesquisador, tarefa_gerenciador_perfil],
            output_file=f"curriculo_personalizado_{candidate_name}.md",
            agent=agent,
        )
        return resume_adaptation_task

    def interview_preparation_task(
        self,
        agent,
        tarefa_pesquisador,
        tarefa_gerenciador_perfil,
        tarefa_curriculo,
    ):
        description = dedent(
            """Crie um conjunto de poss´vieis perguntas para entrevistas e
            pontos de discussão com base no currículo personalizado e nos
            requisitos do trabalho. Utilize ferramentas para gerar questões e
            tópicos relevantes. Certifique-se de que essas perguntas e pontos
            de discussão ajudem o candidato a destacar os principais pontos do
            currículo e como eles correspondem ao anúncio de emprego."""
        )
        expected_output = dedent(
            """Um documento contendo perguntas-chave e pontos de discussão que
            o candidato deve se preparar para a entrevista inicial."""
        )
        interview_preparation_task = Task(
            description=description,
            expected_output=expected_output,
            context=[
                tarefa_pesquisador,
                tarefa_gerenciador_perfil,
                tarefa_curriculo,
            ],
            agent=agent,
        )
        return interview_preparation_task
