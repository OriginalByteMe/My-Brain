from crewai import Task
from textwrap import dedent


class NoteTakingTasks:
    def create_prd_md_note(self, agent, transcript):
        return Task(
            description=dedent(
                f"""\
        You will be given a transcript, you must analyze this transcript.
        Use your expertise to analyze its contents and organize it like a Product Requirement Documentation.
        
        Create different sections and sub-sections as needed, and also determine if a section would benefit from diagram,
        if so, use mermaidjs syntax to create a relevant diagram.
        
        You must write this entire doc using markdown format.
        
        TRANSCRIPT
        ----------
        {transcript}
        
        You do not answer questions, you do not ask questions, you simply produce a document as specified from the transcript given.
        """
            ),
            agent=agent,
            expected_output="A markdown-formatted document as per the given instructions."
        )
