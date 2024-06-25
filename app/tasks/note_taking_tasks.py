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
            expected_output="A markdown-formatted document as per the given instructions.",
        )

    def create_normal_md_note(self, agent, transcript):
        return Task(
            description=dedent(
                f"""\
                    You are an AI assistant tasked with converting transcripts into well-organized markdown notes. Given the following transcript, perform the following tasks:

                    1. **Organize Content**: Divide the content into clear, logical sections such as "Introduction," "Main Points," "Discussion," and "Conclusion."
                    2. **Generate Diagrams**: Identify any parts of the content that could be represented better with diagrams. Create diagrams in Mermaid JS format and include them in the appropriate sections using the markdown code block denoted by ```mermaid```.
                    3. **Formatting**: Ensure the markdown note is properly formatted with headers, bullet points, and code blocks where necessary.

                    Here is the transcript:

                    {transcript}

                    Output the markdown note with organized sections and diagrams.

                    ### Example Output
                    # [Title of the Note]
                    ## Introduction
                    [Introduction content]

                    ## Main Points
                    - Point 1
                    - Point 2
                    ```mermaid
                    graph TD;
                        A-->B;
                        A-->C;
                        B-->D;
                        C-->D;
                    ```
                    ## Discussion
                    [Discussion content]

                    ## Conclusion
                    > [Conclusion content]

                    ### Instructions

                    - Ensure all sections are clearly defined.
                    - Generate at least one Mermaid JS diagram where applicable.
                    - Use proper markdown syntax for headers, lists, and code blocks."""
            )
        )
