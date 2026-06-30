# import re
# import spacy

# class Parser:
#     def __init__(self):
#         # We leverage the spaCy model you already have loaded in Track 1 to analyze semantic similarity
#         self.nlp = spacy.load("en_core_web_sm")
        
#         self.ignore = {
#             "download",
#             "navigation",
#             "other resources",
#             "documentation sections:",
#             "indices, glossary, and search:",
#             "project information:"
#         }

#     def clean_text(self, paragraphs):
#         cleaned = []
#         for text in paragraphs:
#             text = re.sub(r"\s+", " ", text).strip()
#             if not text:
#                 continue
#             # FIXED: Added self. to refer to the class variable
#             if text.lower() in self.ignore:
#                 continue
#             if len(text.split()) < 4:
#                 continue
#             if text not in cleaned:
#                 cleaned.append(text)
#         return cleaned
#     def create_chunks(self, paragraphs):
#         chunks = []
        
#         for paragraph in paragraphs:
#             # Step A: Linguistic sentence boundary parsing using spaCy
#             doc = self.nlp(paragraph)
#             sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
            
#             if not sentences:
#                 continue
                
#             current_chunk = sentences[0]
            
#             # Step B: Semantic Similarity Breakpoint Analysis
#             for i in range(1, len(sentences)):
#                 next_sentence = sentences[i]
                
#                 doc1 = self.nlp(current_chunk)
#                 doc2 = self.nlp(next_sentence)
                
#                 # Check semantic distance between current group and the incoming sentence
#                 similarity = doc1.similarity(doc2)
                
#                 # If similarity drops below 0.65, meaning the topic shifted significantly,
#                 # we split the chunk. Otherwise, we continue rolling it together.
#                 if similarity < 0.65 and len(current_chunk.split()) >= 30:
#                     chunks.append(current_chunk.strip())
#                     current_chunk = next_sentence
#                 else:
#                     current_chunk += " " + next_sentence
            
#             if current_chunk:
#                 chunks.append(current_chunk.strip())
                
#         return chunks

#     def parse(self, page):
#         page["paragraphs"] = self.clean_text(page["paragraphs"])
#         page["chunks"] = self.create_chunks(page["paragraphs"])
#         page.pop("headings", None)
#         page.pop("links", None)
#         return page
    
import re


class Parser:

    def clean_text(self, paragraphs):

        cleaned = []

        ignore = {
            "download",
            "navigation",
            "other resources",
            "documentation sections:",
            "indices, glossary, and search:",
            "project information:"
        }
        for text in paragraphs:

            text = re.sub(r"\s+", " ", text).strip()

            if not text:
                continue

            if text.lower() in ignore:
                continue

            if len(text.split()) < 8:
                continue

            if text not in cleaned:
                cleaned.append(text)

        return cleaned

    def create_chunks(self, paragraphs):

        chunks = []

        for paragraph in paragraphs:

            sentences = re.split(r'(?<=[.!?])\s+', paragraph)

            chunk = ""

            for sentence in sentences:

                if len((chunk + " " + sentence).split()) <= 80:

                    chunk += " " + sentence

                else:

                    chunks.append(chunk.strip())

                    chunk = sentence

            if chunk.strip():

                chunks.append(chunk.strip())

        return chunks

    def parse(self, page):

        page["paragraphs"] = self.clean_text(page["paragraphs"])

        page["chunks"] = self.create_chunks(page["paragraphs"])

        page.pop("headings", None)
        page.pop("links", None)

        return page