from sentence_transformers import SentenceTransformer
import os

from config import GroupingConfig


class Grouper:
    def __init__(self, grouping_configs: list[GroupingConfig]):
        self.grouping_configs = grouping_configs
        self.model = SentenceTransformer('thenlper/gte-large')
    
    def _read_files(self):
        directory = os.path.join(os.getcwd(), "/Transcription/Standup")
        print(directory)
        texts = []
            
        for filename in directory:
            if not filename.endswith(".txt"):
                with open(os.path.join(directory, filename), 'r') as file:
                    texts.append(file.read())
                        
        return texts

    def group_by_topic(self):
        texts = self._read_files()  # temporary
        print(len(texts))
        if not texts: return None
            
        embeddings = self.model.encode(texts, show_progress_bar=True)  
        
        from sklearn.metrics.pairwise import cosine_similarity
        for i in range(len(texts)):
            for j in range(i+1, len(texts)):
                similarity = cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                print("Similarity between '{}' and '{}': {:.2f}%".format(texts[i], texts[j], similarity*100))
