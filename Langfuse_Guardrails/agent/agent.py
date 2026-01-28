import re
from dotenv import load_dotenv
from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM
from langfuse.langchain import CallbackHandler
from guardrails import Guard, OnFailAction
from guardrails.hub import RegexMatch
from tools.tools import web_search_tool
from langfuse import get_client

load_dotenv()

langfuse = get_client()

langfuse_handler = CallbackHandler()

SAFETY_REGEX = r"(?i)\b(hack|hacking|steal|fraud|scam|phish|bypass|bank\s*robbery|cybercrime|illegal|breach|crack|attack|malware)\b"

compiled_regex = re.compile(SAFETY_REGEX)

guard = Guard().use(
    RegexMatch,
    regex=SAFETY_REGEX,
    on_fail=OnFailAction.EXCEPTION
)

llm = OllamaLLM(
    model="llama3"
)

tools = [web_search_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3
)

def run_agent(user_input: str):
    try:
        if compiled_regex.search(user_input):
            return "This request violates safety policies and cannot be processed."

        result = agent.invoke(
            {"input": user_input},
            config={"callbacks": [langfuse_handler]}
        )

        response = result["output"]

        if compiled_regex.search(response):
            return "Generated content violates safety policies."

        return response

    except Exception as e:
        return f"System error: {str(e)}"
