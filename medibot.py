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
    searchResult=search.run(f"site:who.int {inputText}")
    return f"Search results: {searchResult}"

def duckWrapperLoc(inputText):
    """useful when you weant to search for best clinics near a location"""
    searchResult=search.run(f"{inputText}")
    return f"Search results: {searchResult}"
tools=[
    Tool(
        name="Web SearchMD",
        func=duckWrapper,
        description= "useful for when you want to answer medical or pharmalogical problems"
    ),
    Tool(
        name="Web Search",
        func=duckWrapperLoc,
        description= "useful when you weant to search for best clinics near a location"
    )
]

llmWithTools=llm.bind_tools(tools)

prompt= ChatPromptTemplate.from_messages(
    [
       
("system","""You are a helpful medical symptom checker. Solve health-related queries and ask for symptoms using tools where needed.Analyse all the sysmptoms given to come to a decision/conclusion,Also give hints for symstoms.Always provide clear, concise final answers without showing the tool invocation format. Dont exceed 250 words.Only answer to medical related queries.Don't say consult a doctor until you have reached a conclusion from the symptoms.Ask for symptoms by giving the list of symptoms you want to know about."""),
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


def calling(lst):
    chat_history=ChatMessageHistory()
    if len(lst) == 1:
           response=agentex.invoke({"input":lst[0], "chat_history":chat_history.messages})
           return response['output']        
    else: 
        for  i in range(0,len(lst)-1):
            if i % 2 == 0:
                  chat_history.add_user_message(lst[i])
            else:
                  chat_history.add_ai_message(lst[i])
        response=agentex.invoke({"input":lst[len(lst)-1], "chat_history":chat_history.messages})
        return response['output']     
