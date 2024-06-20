from crewai import Crew

from app.agents.note_agent import NoteAgent
from app.tasks.note_taking_tasks import NoteTakingTasks


class NoteTakingCrew:
    def __init__(self, llm, transcript) -> None:
        note_agent_instance = NoteAgent()
        note_taking_tasks_instance = NoteTakingTasks()
        self.note_maker_agent = note_agent_instance.note_maker_agent(llm=llm)
        self.prd_note_task = note_taking_tasks_instance.create_prd_md_note(agent=self.note_maker_agent, transcript=transcript)

    def kickoff(self):
        crew = Crew(
            agents=[self.note_maker_agent], tasks=[self.prd_note_task], verbose=True
        )

        results = crew.kickoff()

        return results
