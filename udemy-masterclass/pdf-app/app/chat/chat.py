import random
from langchain.chat_models import ChatOpenAI
from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import set_conversation_components, get_conversation_components
from app.chat.score import random_component_by_score


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    retriever_name, retriever = select_component("retriever", retriever_map, chat_args)
    llm_name, llm = select_component("llm", llm_map, chat_args)
    memory_name, memory = select_component("memory", memory_map, chat_args)
    print(f"build chat with {retriever_name} / {llm_name} / {memory_name}")
    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        llm=llm_name,
        retriever=retriever_name,
        memory=memory_name,
    )

    # 대화 history와 현재 유저 질문을 요약해서 다른 모델로 넘길 때(condense_question_llm일 때)는
    # 스트리밍을 종료시키지 않도록 아래와 같이 별도의 llm을 만들어 사용
    # => 뒤에 오는 llm에서도 스트리밍을 사용해야하므로 앞에서 종료시키면 안됨
    condense_question_llm = ChatOpenAI(streaming=False)

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        condense_question_llm=condense_question_llm,
        memory=memory,
        retriever=retriever,
        metadata=chat_args.metadata,
    )


def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        random_name = random_component_by_score(component_type, component_map)
        builder = component_map[random_name]
        return random_name, builder(chat_args)
