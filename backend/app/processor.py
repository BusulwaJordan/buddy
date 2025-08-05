from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
import os
import json
import warnings
from pathlib import Path

# Suppress warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning, module="torch")


class DataProcessor:
    def __init__(self, data_dir: str = "data/scraped"):
        self.data_dir = Path(data_dir)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        # Correct embedding initialization: remove duplicate show_progress_bar
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"},
            encode_kwargs={
                "batch_size": 8,
                "normalize_embeddings": False,
            },
            show_progress=True  # enable progress if the wrapper supports it
        )

    def load_scraped_data(self) -> List[Document]:
        documents = []
        if not self.data_dir.exists():
            raise FileNotFoundError(f"Data directory {self.data_dir} does not exist")
        for filename in os.listdir(self.data_dir):
            if filename.endswith(".json"):
                full_path = self.data_dir / filename
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    text = data.get("text", "")
                    if text:
                        documents.append(Document(
                            page_content=text,
                            metadata={
                                "source": data.get("url", ""),
                                "title": data.get("title", "")
                            }
                        ))
                except json.JSONDecodeError:
                    print(f"Warning: failed to parse JSON in {full_path}, skipping.")
        return documents

    def process_and_store(self, persist_directory: str = "data/chroma_db"):
        documents = self.load_scraped_data()
        if not documents:
            raise ValueError("No documents found to process")

        chunks = self.text_splitter.split_documents(documents)

        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding_model,
            persist_directory=persist_directory
        )
        # ensure persistence if needed
        try:
            vectordb.persist()
        except AttributeError:
            pass  # some versions persist automatically

        print(f"Successfully processed {len(chunks)} chunks and stored in '{persist_directory}'")
        return vectordb


if __name__ == "__main__":
    processor = DataProcessor()
    processor.process_and_store()
