from langchain_community.llms import GPT4All
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from typing import Dict, List, Optional
import os
import warnings

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

PROMPT_TEMPLATE = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say "I don't have that information at the moment." 
Don't try to make up an answer.

Context: {context}

Question: {question}
Helpful Answer:"""

class CompanyChatbot:
    def __init__(self, model_path: str = "models/mistral-7b-instruct-v0.1.Q5_K_M.gguf",
                 chroma_dir: str = "data/chroma_db"):
        """Initialize the chatbot with language model and vector store."""
        
        # Validate model path
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found at {model_path}\n"
                "Please download a compatible GGUF model from:\n"
                "https://gpt4all.io/index.html\n"
                "Recommended model: gpt4all-j-v1.3-groovy.gguf"
            )

        # Initialize LLM with error handling
        try:
            self.llm = GPT4All(
                model=model_path,
                max_tokens=2000,
                temp=0.1,
                repeat_penalty=1.1,
                n_threads=4,
                allow_download=False,
                device='cpu',  # Force CPU to avoid CUDA errors
                verbose=False
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize LLM: {str(e)}\n"
                "Possible causes:\n"
                "1. Corrupted model file\n"
                "2. Incompatible model format\n"
                "3. Missing system dependencies"
            ) from e

        # Initialize embeddings
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': False}
        )

        # Initialize vector store
        try:
            self.vectordb = Chroma(
                persist_directory=chroma_dir,
                embedding_function=self.embedding_model
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize ChromaDB: {str(e)}\n"
                "Try deleting and recreating the chroma_db directory"
            ) from e

        # Set up QA chain
        self.qa_prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectordb.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.qa_prompt}
        )

    def query(self, question: str) -> Dict[str, object]:
        """Process a user question and return response with sources."""
        if not question.strip():
            return {"answer": "Please provide a valid question.", "sources": []}

        try:
            result = self.qa_chain.invoke({"query": question})
            
            if not result.get("source_documents"):
                return {
                    "answer": "I don't have that information at the moment.",
                    "sources": []
                }

            sources = [{
                "title": doc.metadata.get("title", "Unknown"),
                "url": doc.metadata.get("source", "#")
            } for doc in result["source_documents"]]

            return {
                "answer": result.get("result", "").strip(),
                "sources": sources
            }
            
        except Exception as e:
            return {
                "answer": f"An error occurred while processing your question: {str(e)}",
                "sources": []
            }