from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever = build_retriever(chat_args=chat_args)
    llm = build_llm(chat_args=chat_args)

    # 대화 history와 현재 유저 질문을 요약해서 다른 모델로 넘길 때(condense_question_llm일 때)는
    # 스트리밍을 종료시키지 않도록 아래와 같이 별도의 llm을 만들어 사용
    # => 뒤에 오는 llm에서도 스트리밍을 사용해야하므로 앞에서 종료시키면 안됨
    condense_question_llm = ChatOpenAI(streaming=False)
    memory = build_memory(chat_args=chat_args)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
    )
