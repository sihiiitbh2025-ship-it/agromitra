from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import hashlib

class RAG:
    def __init__(self, index_path=None, data_path=None):
        # Project root = folder containing "app"
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Default paths
        self.index_path = index_path or os.path.join(project_root, "vectorstore", "index.faiss")
        self.data_path = data_path or os.path.join(project_root, "app", "data", "knowledge.txt")
        self.hash_path = self.index_path.replace(".faiss", ".hash")  # store data file hash

        # Embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        # Ensure folders exist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)

        # Decide whether to rebuild index
        rebuild_needed = True
        if os.path.exists(self.index_path) and os.path.exists(self.hash_path):
            # Compare current file hash with saved hash
            current_hash = self.file_hash(self.data_path)
            with open(self.hash_path, "r") as f:
                saved_hash = f.read().strip()
            rebuild_needed = current_hash != saved_hash

        if rebuild_needed:
            print("🔄 Rebuilding index because knowledge.txt changed or index missing...")
            self.docs = self.load_docs()
            self.index = self.build_index(self.docs)
            self.save_index()
            # Save the new hash
            with open(self.hash_path, "w") as f:
                f.write(self.file_hash(self.data_path))
            print("✅ Index built successfully!")
        else:
            print("🔹 Loading existing index...")
            self.index, self.docs = self.load_index()

    def file_hash(self, path):
        """Compute MD5 hash of a file"""
        with open(path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def load_docs(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"❌ Data file not found: {self.data_path}")
        with open(self.data_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]

    def build_index(self, docs):
        embeddings = self.model.encode(docs, convert_to_numpy=True)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(np.array(embeddings))
        return index

    def save_index(self):
        faiss.write_index(self.index, self.index_path)
        with open(self.index_path.replace(".faiss", ".pkl"), "wb") as f:
            pickle.dump(self.docs, f)

    def load_index(self):
        index = faiss.read_index(self.index_path)
        with open(self.index_path.replace(".faiss", ".pkl"), "rb") as f:
            docs = pickle.load(f)
        return index, docs

    def query(self, text, k=3):
        q_vec = self.model.encode([text], convert_to_numpy=True)
        D, I = self.index.search(np.array(q_vec), k)
        results = []

        for dist, idx in zip(D[0], I[0]):
            if idx < len(self.docs):
                results.append({"doc": self.docs[idx], "score": float(dist)})

        return results

    def rebuild_index(self):
        """Force rebuild index from data file"""
        print("🔄 Rebuilding index...")
        self.docs = self.load_docs()
        self.index = self.build_index(self.docs)
        self.save_index()
        # Update hash
        with open(self.hash_path, "w") as f:
            f.write(self.file_hash(self.data_path))
        print("✅ Index rebuilt successfully!")
