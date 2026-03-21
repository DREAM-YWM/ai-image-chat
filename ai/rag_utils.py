from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Tongyi

def init_rag():
    try:
        loader = TextLoader("house_knowledge.txt", encoding="utf-8")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        splits = text_splitter.split_documents(documents)

        embeddings = DashScopeEmbeddings(
            model="text-embedding-v1",
            dashscope_api_key="sk-372806411bad482289fb6a0bfa24c426"
        )

        vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)

        llm = Tongyi(
            model="qwen-turbo",
            dashscope_api_key="sk-372806411bad482289fb6a0bfa24c426",
            temperature=0.1
        )

        return {"vectorstore": vectorstore, "llm": llm}
    except Exception as e:
        print(f"❌ RAG 初始化失败: {str(e)}")
        return None

def get_rag_knowledge(rag_components, query):
    if not rag_components:
        return ""
    vectorstore = rag_components["vectorstore"]
    llm = rag_components["llm"]

    docs = vectorstore.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])
    prompt = f"根据以下内容回答问题：\n{context}\n\n问题：{query}\n答案："

    try:
        answer = llm.invoke(prompt)
    except AttributeError:
        answer = llm(prompt)
    return answer