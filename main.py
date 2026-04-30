import os 
import scrape
import streamlit as st
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import ConversationalRetrievalChain

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize Streamlit page config
st.set_page_config(page_title="AI Tutor Chatbot", page_icon="🤖", layout="wide")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "chain" not in st.session_state:
    st.session_state.chain = None

try:
    q_embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-2-preview"
    )
    
    gemini = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0, 
        max_tokens=None,
        timeout=None,
    )
except Exception as e:
    st.error(f"Failed to initialize AI models: {str(e)}")
    st.info("Please check your API keys in the .env file")
    st.stop()

try:
    qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_URL"), 
        api_key=os.getenv("QDRANT_API_KEY"),
        timeout=300
    )
except Exception as e:
    st.error(f"Failed to connect to Qdrant: {str(e)}")
    st.info("Please verify your QDRANT_URL and QDRANT_API_KEY in the .env file")
    st.stop()
qa_prompt = ChatPromptTemplate.from_template("""You are an AI Tutor and Assistant specialized in Artificial Intelligence, Machine Learning, Deep Learning, and related technologies.

Your role is to act like a knowledgeable, friendly, and patient teacher who helps users understand AI concepts clearly and intuitively.
BEHAVIOR & TONE:

Always respond in a teaching style (clear, structured, and beginner-friendly when needed)
Be polite, calm, and encouraging
Use simple explanations first, then go deeper if required
Provide examples and analogies where helpful
Avoid unnecessary technical jargon unless the user asks for it

KNOWLEDGE SOURCES PRIORITY:

PRIMARY SOURCE (RAG CONTEXT):
If the provided context contains relevant information, use it as your main source
Base your answer primarily on the retrieved content

ANSWER FORMAT:
- Use clear, structured responses
- Include examples where helpful
- Keep answers concise but informative

Document Context:
{context}

Question: {question}

Answer:""")

def initialize_chain():
    """Initialize the conversational retrieval chain"""
    try:
        vector_store = QdrantVectorStore(
            client=qdrant_client,
            collection_name="AI_DATA",
            embedding=q_embeddings,
        )
        
        retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 5})
        chain = ConversationalRetrievalChain.from_llm(
            llm=gemini,
            retriever=retriever,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            return_source_documents=False,
        )
        return chain, vector_store
    except Exception as e:
        st.error(f"Failed to initialize chain: {str(e)}")
        return None, None

def display_chat_history():
    """Display conversation history"""
    for i, msg in enumerate(st.session_state.chat_history):
        if isinstance(msg, tuple) and len(msg) == 2:
            role, content = msg
            if role.lower() == "human":
                with st.chat_message("user"):
                    st.write(content)
            else:
                with st.chat_message("assistant"):
                    st.write(content)

def main():
    st.title("🤖 AI Tutor Chatbot")
    st.markdown("*Specialized in AI, Machine Learning, Deep Learning, and Technology*")
    
    # Sidebar info
    with st.sidebar:
        st.header("ℹAbout")
        st.write("This chatbot helps you learn about AI and ML concepts through interactive conversations.")
        st.divider()
        
        if st.session_state.vector_store:
            try:
                collection_info = qdrant_client.get_collection("AI_DATA")
                st.metric("Knowledge Base Size", f"{collection_info.points_count} documents")
            except:
                pass
        
        st.divider()
        st.markdown("**How to use:**\n1. Ask any AI/ML question\n2. Get instant answers based on knowledge base\n3. Continue the conversation naturally")
    
    # Initialize chain and vector store on first load
    if st.session_state.chain is None or st.session_state.vector_store is None:
        with st.spinner("Initializing AI Tutor..."):
            try:
                collection_info = qdrant_client.get_collection("AI_DATA")
                
                # If collection is empty, scrape and populate data
                if collection_info.points_count == 0:
                    st.info("First-time setup: Scraping educational content...")
                    scraped_data = scrape.main()
                    
                    if scraped_data:
                        text_splitter = RecursiveCharacterTextSplitter(
                            chunk_size=1000,   
                            chunk_overlap=100,
                            length_function=len,
                        )
                        texts = text_splitter.split_documents(scraped_data)
                        
                        # Initialize vector store and add documents
                        vector_store = QdrantVectorStore(
                            client=qdrant_client,
                            collection_name="AI_DATA",
                            embedding=q_embeddings,
                        )
                        vector_store.add_documents(texts)
                        st.success(f"Knowledge base initialized with {len(texts)} document chunks")
                        st.session_state.vector_store = vector_store
                    else:
                        st.error("Failed to scrape data. Please check your internet connection.")
                        st.stop()
                else:
                    st.success(f"Connected to knowledge base ({collection_info.points_count} documents)")
                
                chain, vector_store = initialize_chain()
                if chain:
                    st.session_state.chain = chain
                    st.session_state.vector_store = vector_store
                else:
                    st.stop()
                    
            except Exception as e:
                st.error(f"Initialization error: {str(e)}")
                st.stop()
    
    display_chat_history()

    if user_input := st.chat_input("Ask me anything about AI and technology..."):
        # Display user message
        with st.chat_message("user"):
            st.write(user_input)
        
        # Add to chat history
        st.session_state.chat_history.append(("human", user_input))
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    formatted_history = [
                        (msg[1], st.session_state.chat_history[i+1][1]) if msg[0].lower() == "human" else None
                        for i, msg in enumerate(st.session_state.chat_history[:-1]) if i < len(st.session_state.chat_history) - 1
                    ]
                    formatted_history = [h for h in formatted_history if h is not None]
                    
                    response = st.session_state.chain(
                        {"question": user_input, "chat_history": formatted_history}
                    )
                    answer = response.get("answer", "Sorry, I couldn't generate a response.")
                    st.write(answer)
                    
                    st.session_state.chat_history.append(("ai", answer))
                    
                except Exception as e:
                    error_msg = f"Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_history.append(("ai", error_msg))

if __name__ == "__main__":
    main()
