from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import Tool
from langchain_core.prompts import ChatPromptTemplate , MessagesPlaceholder
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents import AgentExecutor
from langchain.memory import ChatMessageHistory

llm = ChatGroq(model="llama-3.3-70b-versatile", api_key='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')

search= DuckDuckGoSearchRun()

def duckWrapper(inputText):
    """useful for when you want to answer medical or pharmalogical problems"""
    searchResult=search.run(f"site:webmd.com {inputText}")
    return searchResult
tools=[
    Tool(
        name="Web Search",
        func=duckWrapper,
        description= "useful for when you want to answer medical or pharmalogical problems"
    )
]

llmWithTools=llm.bind_tools(tools)

prompt= ChatPromptTemplate.from_messages(
    [
        ("system","You are expert at medical field try to solve user's queries related to health if the user asks questions outside of your domain just reply that you are a medical chatbot designed to assist you in health related issues please ask questions related to health"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human","{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

agent=(
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
        "chat_history": lambda x: x["chat_history"]
    }| prompt | llmWithTools | OpenAIToolsAgentOutputParser()
)

agentex= AgentExecutor(agent=agent, tools=tools)

chat_history=ChatMessageHistory()
def calling(text):
    response=agentex.invoke({"input":text, "chat_history":chat_history.messages})
    return response['output']
# response=agentex.invoke({"input":"Im having a sprain in my anknle how to fix it", "chat_history":chat_history.messages})

# print(response['output'])