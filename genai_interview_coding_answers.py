# 1. Merge and Sort Lists
list1 = [1, 3, 5, 7]
list2 = [2, 3, 5, 8]
merged_sorted = sorted(set(list1 + list2), reverse=True)
print("1. Merge and Sort Lists:", merged_sorted)
# Output: [8, 7, 5, 3, 2, 1]

# 2. String Reversal Check (Palindrome)
def is_palindrome(s):
    s = s.lower()
    return s == s[::-1]
print("2. Palindrome Check:", is_palindrome("Level"))  # Output: True

# 3. Word Frequency Counter
from collections import Counter
def word_freq(s):
    words = s.lower().split()
    freq = Counter(words)
    return dict(freq.most_common())
print("3. Word Frequency:", word_freq("the cat and the dog and the mouse"))
# Output: {'the': 3, 'and': 2, 'cat': 1, 'dog': 1, 'mouse': 1}

# 4. Find Missing Number
def find_missing(nums, n):
    return set(range(1, n+1)).difference(nums).pop()
print("4. Missing Number:", find_missing([1,2,4,5], 5))  # Output: 3

# 5. Flatten Nested List
def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
print("5. Flattened List:", flatten([[1,2],[3,4],[5,[6,7]]]))  # Output: [1,2,3,4,5,6,7]

# 6. Top N Elements (without sorted)
def top_n(lst, n=3):
    result = []
    temp_lst = lst[:]
    for _ in range(n):
        if temp_lst:
            m = max(temp_lst)
            result.append(m)
            temp_lst.remove(m)
    return result
print("6. Top 3 Elements:", top_n([4,1,7,2,9,8]))  # Output: [9,8,7]

# 7. Anagram Check
def is_anagram(a, b):
    return sorted(a.lower()) == sorted(b.lower())
print("7. Anagram Check:", is_anagram("listen", "silent"))  # Output: True

# 8. Remove Stopwords
def remove_stopwords(sentence, stopwords):
    return ' '.join([w for w in sentence.split() if w.lower() not in stopwords])
stopwords = ["is", "the", "a", "an"]
print("8. Remove Stopwords:", remove_stopwords("This is the best example", stopwords))
# Output: 'This best example'

# 9. Matrix Transpose
def transpose(matrix):
    return [list(row) for row in zip(*matrix)]
print("9. Matrix Transpose:", transpose([[1,2,3],[4,5,6]]))  # Output: [[1,4],[2,5],[3,6]]

# 10. JSON Flattening
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
print("10. Flatten JSON:", flatten_json(data))
# Output: {'user.name': 'Rahul', 'user.location.city': 'Mumbai'}

# 11. Text to Embedding (using HF Transformers - pseudocode)
def get_embedding(text):
    """
    Pseudocode: In practice, use HuggingFace or OpenAI API
    tokenizer = AutoTokenizer.from_pretrained('model')
    model = AutoModel.from_pretrained('model')
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    """
    return [0.1, 0.2, 0.3]  # Example embedding vector
print("11. Text to Embedding:", get_embedding("GenAI is transforming enterprise search."))

# 12. Cosine Similarity
from numpy import dot
from numpy.linalg import norm
def cosine_similarity(a, b):
    return dot(a, b) / (norm(a) * norm(b))
emb1 = [1, 2, 3]
emb2 = [2, 4, 6]
print("12. Cosine Similarity:", cosine_similarity(emb1, emb2))  # Output: 1.0

# 13. Prompt Template
def build_prompt(question, context):
    return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
print("13. Prompt Template:", build_prompt("What is GenAI?", "GenAI is Generative AI."))

# 14. Store Embeddings in Vector DB (Pseudocode)
def store_embedding(id, embedding):
    """
    Pseudocode for Pinecone:
    pinecone.init(api_key="YOUR_KEY")
    index = pinecone.Index("genai-demo")
    index.upsert([(id, embedding)])
    """
    print(f"Stored embedding for {id}: {embedding}")
store_embedding("doc1", [0.1, 0.2, 0.3])