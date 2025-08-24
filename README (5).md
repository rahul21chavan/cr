# Deloitte GenAI & Python Interview Prep Guide

This guide covers **core GenAI concepts**, **practical RAG (Retrieval-Augmented Generation) questions**, and a set of **Python coding interview problems** often used in consulting, GenAI, and data engineering interviews (such as those at Deloitte). Each coding question includes a detailed solution and example.

---

## Core Concept Questions & Answers

### 1. What is a Large Language Model (LLM)?

A Large Language Model (LLM) is a type of deep learning model trained on vast amounts of text data to understand, generate, and manipulate human language. LLMs (like GPT-4, PaLM, LLaMA) use neural network architectures (often Transformers) to learn patterns in text and generate responses to prompts, answer questions, summarize documents, etc.

---

### 2. What is the Transformer architecture and how does it work?

The Transformer is an attention-based neural network architecture introduced in the paper ["Attention Is All You Need" (Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762). It replaces recurrence with self-attention mechanisms that allow the model to weigh the importance of different words in the input sequence. The architecture consists of encoder and decoder blocks, each with multi-head self-attention and feed-forward layers, enabling efficient parallelization and better context understanding.

---

### 3. What is Retrieval-Augmented Generation (RAG)?

RAG is a technique that combines information retrieval and language generation. Instead of relying solely on a language model's internal knowledge, RAG systems fetch relevant documents from an external database (retriever) and use them as context to generate more accurate, up-to-date, or domain-specific responses (generator). This boosts factuality and enables handling larger context windows.

---

### 4. What frameworks are commonly used to implement RAG?

- **Hugging Face Transformers** (with RAG models)
- **LlamaIndex** (formerly GPT Index)
- **Haystack**
- **LangChain**
- **OpenAI API** (with custom retriever logic)
- **Weaviate / Pinecone / Chroma** (vector databases)

---

### 5. How do you connect an external database in a RAG pipeline?

You connect a retriever (e.g., vector search, SQL query, Elasticsearch) that queries the external database for documents relevant to the user's question. The retrieved information is then passed as context to the LLM for generation. In frameworks like Haystack or LangChain, this involves configuring a retriever object with database connection details and embedding logic.

---

### 6. What are token limitations in LLMs?

Each LLM has a maximum context window (number of tokens it can process at once, e.g., 4k, 8k, 32k tokens). Inputs exceeding this are truncated or rejected. This impacts document handling, prompt engineering, and the amount of context you can provide to the model.

---

### 7. What are different chunking strategies in RAG?

- **Fixed-size chunking:** Split text into equal token/word-size chunks.
- **Recursive chunking:** Split large text recursively, aligning with logical boundaries (e.g., paragraphs).
- **Semantic chunking:** Use semantic similarity or topic modeling to split text at meaningful points.
- **Sliding window:** Overlap chunks to maintain context continuity across boundaries.

---

### 8. What evaluation metrics are used to assess a RAG system?

**Retrieval metrics:**
- Precision@k, Recall@k
- Mean Average Precision (MAP)
- Normalized Discounted Cumulative Gain (NDCG)

**Generation metrics:**
- ROUGE, BLEU (text similarity)
- Factuality (human or model-based)
- Faithfulness (does output reflect retrieved context)
- Human evaluation (accuracy, helpfulness)

---

### 9. What is a prompt in LLMs?

A prompt is the input text (question, instruction, context) provided to an LLM to guide its output. Prompt engineering involves crafting prompts to elicit desired behavior from the model.

---

### 10. Explain zero-shot learning.

Zero-shot learning is when an LLM performs a task without seeing any explicit examples in the prompt. The model generalizes from its training data.

---

### 11. Explain few-shot learning.

Few-shot learning is when you provide a handful of task-specific examples in the prompt to demonstrate how the model should behave.

---

### 12. What is chain-of-thought prompting and why is it important?

Chain-of-thought (CoT) prompting encourages the LLM to reason step-by-step (showing intermediate reasoning) before arriving at an answer. It is important because it improves reasoning and accuracy for complex problems.

---

## Applied / Practical Usage Questions & Answers

### 1. How would you handle documents larger than the LLM’s token limit in a RAG setup?

- Chunk the document using one of the chunking strategies.
- Store chunks in a retrievable database (vector DB, Elasticsearch).
- Retrieve relevant chunks for each query and pass only those to the LLM.

---

### 2. What challenges do you face when connecting an enterprise database to a RAG system?

- Security & authentication
- Schema mapping and data normalization
- Latency and scalability
- Data privacy & governance
- Handling unstructured vs. structured data

---

### 3. How would you evaluate retrieval quality in a production-grade RAG pipeline?

- Use labeled queries to measure precision/recall.
- Monitor real user feedback.
- Track retrieval latency and coverage.
- Perform regular audits for drift and relevance.

---

### 4. What role does a vector database play in RAG?

A vector DB stores embeddings (vector representations) of documents for fast similarity search. It enables scalable, semantic retrieval of relevant chunks or passages, crucial for RAG.

---

### 5. How do you ensure data privacy and governance in enterprise GenAI systems?

- Secure data access (authentication, RBAC)
- Audit logs
- Data masking & anonymization
- Compliance (GDPR, HIPAA)
- Prompt filtering to prevent leakage

---

### 6. How does Deloitte typically apply RAG and LLMs in real-world consulting projects?

- Document summarization (extracting key points from lengthy docs)
- Expert Q&A assistants
- Knowledge management (searching across enterprise data)
- Automated report generation
- Creating knowledge graphs from text

---

## Python Coding Interview Questions (with Answers & Examples)

### 1. Merge and Sort Lists

**Q:** Declare two lists, merge them, remove duplicates, and sort descending.

```python
# Solution
list1 = [1, 3, 5, 7]
list2 = [2, 3, 5, 8]

merged = list(set(list1 + list2))
sorted_desc = sorted(merged, reverse=True)
print(sorted_desc)     # Output: [8, 7, 5, 3, 2, 1]
```

---

### 2. String Reversal Check (Palindrome)

**Q:** Check if a string is a palindrome.

```python
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]

print(is_palindrome("Level"))  # Output: True
print(is_palindrome("Rahul"))  # Output: False
```

---

### 3. Word Frequency Counter

**Q:** Count word frequency in a string, return dictionary sorted by frequency.

```python
from collections import Counter

def word_freq(s):
    words = s.lower().split()
    freq = Counter(words)
    return dict(freq.most_common())

print(word_freq("the cat and the dog and the mouse"))
# Output: {'the': 3, 'and': 2, 'cat': 1, 'dog': 1, 'mouse': 1}
```

---

### 4. Find Missing Number

**Q:** Given a list from 1 to n with one missing, find the number.

```python
def find_missing(nums, n):
    return set(range(1, n+1)).difference(nums).pop()

print(find_missing([1,2,4,5], 5))  # Output: 3
```

---

### 5. Flatten Nested List

**Q:** Flatten a nested list ([[1,2],[3,4],[5,[6,7]]]) to [1,2,3,4,5,6,7]

```python
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([[1,2],[3,4],[5,[6,7]]]))  # Output: [1,2,3,4,5,6,7]
```

---

### 6. Top N Elements

**Q:** Find the top 3 largest numbers in a list without using sorted().

```python
def top_n(lst, n=3):
    result = []
    for _ in range(n):
        if lst:
            m = max(lst)
            result.append(m)
            lst.remove(m)
    return result

print(top_n([4,1,7,2,9,8]))  # Output: [9,8,7]
```

---

### 7. Anagram Check

**Q:** Check if two strings are anagrams.

```python
def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())

print(is_anagram("listen", "silent"))  # Output: True
print(is_anagram("hello", "world"))    # Output: False
```

---

### 8. Remove Stopwords

**Q:** Remove stopwords from a sentence.

```python
def remove_stopwords(sentence, stopwords):
    return ' '.join([w for w in sentence.split() if w.lower() not in stopwords])

stopwords = ["is", "the", "a", "an"]
print(remove_stopwords("This is the best example", stopwords)) # Output: 'This best example'
```

---

### 9. Matrix Transpose

**Q:** Transpose a 2D matrix.

```python
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

print(transpose([[1,2,3],[4,5,6]]))  # Output: [[1,4],[2,5],[3,6]]
```

---

### 10. JSON Flattening

**Q:** Flatten nested JSON/dict to dot-separated keys.

```python
def flatten_json(d, parent_key='', sep='.'):
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items

data = {"user": {"name": "Rahul", "location": {"city": "Mumbai"}}}
print(flatten_json(data))
# Output: {'user.name': 'Rahul', 'user.location.city': 'Mumbai'}
```

---

## Extra GenAI Python Basics (Frequently Asked)

### 11. Convert Text to Embeddings (using OpenAI or Hugging Face)

```python
# Using Hugging Face Transformers
from transformers import AutoTokenizer, AutoModel
import torch

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()

print(get_embedding("GenAI is transforming enterprise search."))
```

---

### 12. Cosine Similarity Between Embeddings

```python
from numpy import dot
from numpy.linalg import norm

def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))

# Usage with get_embedding() from above
# emb1 = get_embedding("Text 1")
# emb2 = get_embedding("Text 2")
# print(cosine_similarity(emb1, emb2))
```

---

### 13. Simple Prompt Template for LLM

```python
def build_prompt(question, context):
    return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
```

---

### 14. Store Embeddings in a Vector Database (Pseudo-code Example)

```python
# Pseudocode for storing embeddings in Pinecone
import pinecone

pinecone.init(api_key="YOUR_KEY", environment="us-west1-gcp")
index = pinecone.Index("genai-demo")

def store_embedding(id, embedding):
    index.upsert([(id, embedding.tolist())])
```

---

## Interview Sheet (for Practice)

---

**Instructions:** Use this sheet in mock interviews. Write your answers in the blank spaces provided.

---

### Core Concept Questions

1. What is a Large Language Model (LLM)?
   - _____________________________________________________________

2. What is the Transformer architecture and how does it work?
   - _____________________________________________________________

3. What is Retrieval-Augmented Generation (RAG)?
   - _____________________________________________________________

4. What frameworks are commonly used to implement RAG?
   - _____________________________________________________________

5. How do you connect an external database in a RAG pipeline?
   - _____________________________________________________________

6. What are token limitations in LLMs?
   - _____________________________________________________________

7. What are different chunking strategies in RAG?
   - _____________________________________________________________

8. What evaluation metrics are used to assess a RAG system?
   - _____________________________________________________________

9. What is a prompt in LLMs?
   - _____________________________________________________________

10. Explain zero-shot learning.
    - _____________________________________________________________

11. Explain few-shot learning.
    - _____________________________________________________________

12. What is chain-of-thought prompting and why is it important?
    - _____________________________________________________________

---

### Applied / Practical Usage Questions

1. How would you handle documents larger than the LLM’s token limit in a RAG setup?
   - _____________________________________________________________

2. What challenges do you face when connecting an enterprise database to a RAG system?
   - _____________________________________________________________

3. How would you evaluate retrieval quality in a production-grade RAG pipeline?
   - _____________________________________________________________

4. What role does a vector database play in RAG?
   - _____________________________________________________________

5. How do you ensure data privacy and governance in enterprise GenAI systems?
   - _____________________________________________________________

6. How does Deloitte typically apply RAG and LLMs in real-world consulting projects?
   - _____________________________________________________________

---

### Python Coding Practice

Write code or pseudocode for any of the following:

1. Merge and Sort Lists
2. String Reversal Check (Palindrome)
3. Word Frequency Counter
4. Find Missing Number
5. Flatten Nested List
6. Top N Elements (without sorted)
7. Anagram Check
8. Remove Stopwords
9. Matrix Transpose
10. JSON Flattening
11. Text to Embedding
12. Cosine Similarity
13. Prompt Template
14. Store Embeddings in Vector DB

---

**Good luck! Practice these questions and solutions to ace GenAI/Data Engineering interviews.**