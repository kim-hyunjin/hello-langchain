from langchain.prompts import (
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import (
    ConversationBufferMemory,
    FileChatMessageHistory,
    ConversationSummaryMemory,
)
from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(verbose=True)

# memory = ConversationBufferMemory(
#     memory_key="messages",
#     return_messages=True,
#     chat_memory=FileChatMessageHistory("messages.json"),
# )
"""
{'content': 'and 3 more?', 'messages': [HumanMessage(content='what is 1+1?'), AIMessage(content='1+1 equals 2.')], 'text': '3 more than 1+1 would be 5. (1+1 = 2, 2+3 = 5)'}
"""
memory = ConversationSummaryMemory(
    memory_key="messages", return_messages=True, llm=chat
)
"""
{'content': 'and 3 more?', 'messages': [SystemMessage(content='The human asks what 1+1 is. The AI responds that 1+1 equals 2.')], 'text': 'If you add 1+1+1, the result is 3.'}
"""

prompt = ChatPromptTemplate(
    input_variables=["content", "messages"],
    messages=[
        MessagesPlaceholder(variable_name="messages"),
        HumanMessagePromptTemplate.from_template("{content}"),
    ],
)

chain = LLMChain(llm=chat, prompt=prompt, memory=memory, verbose=True)

while True:
    content = input(">> ")

    result = chain({"content": content})

    print(f"Result: {result}")
