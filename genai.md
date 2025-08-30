# Deloitte GenAI Engineer Interview Cheat Sheet
*Generative AI Agents & LLM Workflows with LangChain, Bedrock, OpenAI & Hugging Face*

---

## Table of Contents
- [Section 1: Beginner Q&A (Fundamentals)](#beginner)
- [Section 2: Intermediate Q&A (Implementation)](#intermediate)
- [Section 3: Advanced Q&A (Enterprise, Orchestration)](#advanced)
- [Section 4: Hugging Face Q&A (Ecosystem & Deployment)](#huggingface)
- [Section 5: Quick Revision Table](#revision-table)

---

<a name="beginner"></a>
## 🔹 Section 1: Beginner Q&A (Conceptual Fundamentals)

**Q1. What is LangChain and why is it important for GenAI?**  
LangChain is an open-source framework for building LLM-powered apps. It offers chains, memory, agents, tools, and retrieval, abstracting complexity and enabling modular, scalable, production-ready GenAI workflows.

**Q2. What is AWS Bedrock and how does it compare to OpenAI?**  
Bedrock: Multi-model, managed GenAI service (Claude, Cohere, Titan, etc.)  
OpenAI: Single-vendor, proprietary models (GPT-4, GPT-3.5).  
Bedrock is enterprise-friendly, integrates with AWS infra, OpenAI is high-performing but less flexible.

**Q3. Generative AI agents vs LLM chatbots?**  
Chatbot: Text responder.  
Agent: Decides actions, calls APIs/tools, executes workflows (e.g., booking flights, fetching data).

**Q4. Why do enterprises use LangChain + Bedrock/OpenAI?**  
Raw LLMs = limited context.  
LangChain: Enables RAG, agents, orchestration.  
Bedrock/OpenAI: Secure, scalable model hosting.

---

<a name="intermediate"></a>
## 🔹 Section 2: Intermediate Q&A (Implementation & Workflows)

**Q5. RAG with LangChain?**  
- Load Data (PDFs, DBs, S3)
- Chunk & Embed (vector embeddings)
- Store in Vector DB (FAISS, Pinecone, Kendra)
- Retrieve relevant docs
- Chain: Feed context + query to LLM

**Q6. How do agents call tools?**  
Agents use LLM reasoning (ReAct). Thought → decide tool → execute → observe → repeat.

**Q7. Workflow: OpenAI + LangChain + Bedrock?**  
E.g., Knowledge Assistant: Retrieve data via Bedrock + Kendra, summarize with GPT-4, deliver structured output.

**Q8. Prompt engineering in enterprise GenAI?**  
Techniques: Zero-shot, Few-shot, Chain-of-thought, Guardrails, Dynamic prompts (LangChain templates).

---

<a name="advanced"></a>
## 🔹 Section 3: Advanced Q&A (Deployment, Scaling & Orchestration)

**Q9. Deploying LLM workflow on AWS?**  
- Bedrock for models
- Vector DB: OpenSearch/DynamoDB
- APIs: Lambda/ECS/EKS
- Secure endpoints: API Gateway
- Monitoring: CloudWatch + LangSmith
- CI/CD: CodePipeline

**Q10. Security & compliance in GenAI?**  
- Mask PII
- Use compliant infra (Bedrock SOC2/GDPR)
- IAM roles, API Gateway auth
- Guardrails, content moderation
- Audit logs (CloudWatch/DynamoDB)

**Q11. Performance tuning in LangChain?**  
- Cache embeddings/responses
- Streaming outputs
- Batch embeddings
- Model selection (fast vs reasoning)
- Hybrid retrieval: keyword + vector

**Q12. LangChain Agents vs Orchestration tools?**  
Agents: Real-time, dynamic, reasoning-driven  
Airflow/Step Functions: Static, DAG-based, deterministic  
Best: Combine for reliability + intelligence

**Q13. Monitoring/debugging GenAI apps?**  
- LangSmith for logs, traces, evals
- Track token usage, latency, accuracy
- Unit-tests for prompts, red-teaming

---

<a name="huggingface"></a>
## 🔹 Section 4: Hugging Face Q&A (Ecosystem & Deployment)

**Q38. What is Hugging Face?**  
Open-source AI platform:  
- Transformers library for LLMs  
- Model and Dataset hubs  
- Inference APIs  
Democratizes AI, accelerates enterprise adoption.

**Q39. Hugging Face vs OpenAI/Bedrock?**  
OpenAI: Closed, proprietary  
Bedrock: Managed, multi-vendor  
Hugging Face: Open-source, flexible, local deployment

**Q40. Hugging Face Transformers library?**  
Easy API for tasks: classification, summarization, QA, embeddings  
```python
from transformers import pipeline
qa = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
qa(question="What is Deloitte?", context="Deloitte is a consulting firm...")
```

**Q41. HF models in LangChain workflows?**  
```python
from langchain.llms import HuggingFaceHub
llm = HuggingFaceHub(repo_id="google/flan-t5-base")
response = llm("Translate this English text to French: Hello Deloitte")
```

**Q42. HF embeddings vs OpenAI embeddings?**  
HF: Open-source, local, privacy-friendly  
OpenAI: Cloud, high-quality  
Deloitte: HF for confidential on-prem data

**Q43. Deploy HF models on AWS Bedrock/SageMaker?**  
Bedrock: No direct HF hosting  
SageMaker: Deploy HF endpoints  
HF: Managed endpoints via Inference API

**Q44. Hugging Face PEFT (Parameter-Efficient Fine-Tuning)?**  
Fine-tune small adapter layers (LoRA, QLoRA, Prefix Tuning)  
90%+ cost reduction vs full fine-tuning  
E.g., adapt Flan-T5 for audit summarization

**Q45. Choosing HF open-source vs proprietary models?**  
HF: Privacy, cost, custom tuning  
Proprietary: Best accuracy, no infra management  
Hybrid approach for Deloitte

**Q46. Enterprise challenges with HF deployment?**  
- Inference latency  
- GPU infra scaling  
- Model governance  
- Security  
Solution: SageMaker + HF Toolkit + Bedrock Guardrails

**Q47. HF + LangChain for multi-agent systems?**  
HF: Specialized models (summarizer, embedding, QA)  
LangChain: Orchestration  
E.g., Summarizer agent (Flan-T5), Embedding agent (MiniLM), Reasoning agent (Claude)

**Q48. HF Inference API in enterprise?**  
Hosted endpoints for any HF model  
Use: Deploy falcon-7b-instruct for bulk audits  
Comparison: More choice, less compliance than Bedrock

**Q49. Evaluating HF models for enterprise?**  
- Domain accuracy  
- Latency  
- Scalability  
- Security compliance  
- Support for PEFT/quantization

**Q50. What is DistilBERT? Why use it over BERT?**  
DistilBERT: 40% smaller, 60% faster, ~97% accuracy of BERT  
Ideal for real-time Deloitte apps (fraud detection, sentiment analysis)

---

## 🔹 Quick Revision Table

| Concept/Tech         | Key Features                                 | Enterprise Advantage                | Example Use Case              |
|----------------------|----------------------------------------------|-------------------------------------|-------------------------------|
| **LangChain**        | Chains, Agents, RAG, memory, tools           | Modular, scalable orchestration     | Knowledge Assistant, RAG      |
| **Bedrock**          | Managed multi-model (Claude, Titan, Cohere)  | Compliance, AWS integration         | Secure LLM hosting            |
| **OpenAI**           | Proprietary (GPT-4, GPT-3.5)                 | Best-in-class accuracy/reasoning    | Summarization, chat           |
| **Hugging Face**     | Open-source LLMs, datasets, Inference API    | Privacy, cost, custom fine-tuning   | On-prem audit summarizer      |
| **RAG**              | Retrieval + LLM generation                   | Reduces hallucination, token limits | Enterprise search             |
| **Agents**           | Dynamic tool calling, reasoning              | Automate workflows                  | Financial analyst agent       |
| **PEFT**             | Efficient fine-tuning (LoRA, QLoRA)          | Low-cost domain adaptation          | Legal/finance customization   |
| **DistilBERT**       | Smaller, faster BERT                         | Real-time, cost-effective           | Fraud detection, sentiment    |
| **Guardrails**       | Policy enforcement for AI outputs            | Consistent compliance/safety        | PII filtering, moderation     |
| **Hybrid Workflow**  | Combine open-source + proprietary, multi-cloud| Flexibility, reliability            | Deloitte multi-region apps    |

---

## 🔹 Tips for Deloitte GenAI Interviews
- **Explain trade-offs**: Open-source vs managed, privacy vs performance.
- **Talk architecture**: Microservices, API Gateway, Lambda/ECS/EKS, Step Functions.
- **Use case-driven answers**: Relate concepts to Deloitte’s domains (audit, compliance, finance).
- **Mention observability & compliance**: LangSmith, CloudWatch, Guardrails, red-teaming.
- **Show awareness of future trends**: PEFT, multi-agent systems, hybrid cloud, governance.

---

**Prepared by:**  
Rahul Chavan | GenAI Interview Prep | August 2025
