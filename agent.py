import requests
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

# Initialize the Ollama LLM via the UNCW server
llm = LLM(
    model="ollama/llama3.2", 
    base_url="http://lambda2.uncw.edu:11434/api/generate"
)

# Define two agents
search_agent = Agent(
    role="NASA Context Reader",
    goal="Read NASA APOD info and provide relevant context for space questions",
    backstory="Astronomy expert who understands NASA images and space concepts",
    llm=llm,
    verbose=False
)

synthesizer_agent = Agent(
    role="Answer Synthesizer",
    goal="Take the output from search agent and generate a clear, informative answer",
    backstory="Skilled in explaining astronomy topics in a simple way",
    llm=llm,
    verbose=False
)

def ask_space_agent(title: str, explanation: str, question: str) -> str:
    from crewai import Agent, Task, Crew, Process, LLM

    llm = LLM(
        model="ollama/llama3.2", 
        base_url="http://lambda2.uncw.edu:11434/api/generate"
    )

    search_agent = Agent(
        role="NASA Context Reader",
        goal="Read NASA APOD info and provide relevant context for space questions",
        backstory="Astronomy expert who understands NASA images and space concepts",
        llm=llm,
        verbose=False
    )

    synthesizer_agent = Agent(
        role="Answer Synthesizer",
        goal="Take the output from search agent and generate a clear, informative answer",
        backstory="Skilled in explaining astronomy topics in a simple way",
        llm=llm,
        verbose=False
    )

    search_content = f"""
NASA Image Title: {title}
NASA Image Description: {explanation}

User Question: {question}
"""
    search_task = Task(
        description=f"Analyze this info and provide context: {search_content}",
        agent=search_agent,
        expected_output="Relevant context or facts for the user's question"
    )

    synthesis_task = Task(
        description=f"Using previous output, give a clear answer to: {question}",
        agent=synthesizer_agent,
        expected_output="A comprehensive, human-readable answer"
    )

    crew = Crew(
        agents=[search_agent, synthesizer_agent],
        tasks=[search_task, synthesis_task],
        process=Process.sequential,
        verbose=False
    )

    result = crew.kickoff()
    return result.raw