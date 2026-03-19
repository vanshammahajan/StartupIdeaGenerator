# StartupIdeaGenerator
Tool that extracts problems from Reddit posts and generates startup ideas


# Overview
Startup Idea Generator is a Python application that extracts real-world problems from Reddit and uses a Large Language Model (LLM) to generate potential startup ideas.
The goal of this project is to automatically identify problems people discuss online and convert them into possible business opportunities.


# Simple Architecture
```
Reddit API
     ↓
Fetch Posts
     ↓
Problem Detection 
     ↓   
Idea Generator
     ↓
Display Results
```

# Project Structure
```
startup-idea-generator
│
├── app.py              # Main application
├── access.py           # Reddit API credentials
├── .env                # LLM access token 
├── requirements.txt    # Project dependencies
├── ideas.txt           # Generated startup ideas
└── .gitignore          # Ignore sensitive files
```
Sensitive Files (Ignored via .gitignore)
The .gitignore file ensures that sensitive data is not pushed to GitHub.
It contains:
- .env
- access.py
```
Contents of Sensitive Files
.env 
  - HUGGINGFACEHUB_ACCESS_TOKEN = "ACCESS_TOKEN"
access.py
  - client_id = "YOUR_CLIENT_ID"
  - client_secret = "YOUR_SECRET"
  - user_agent = "startup-idea-generator"
 ```
# Technologies Used
- Python
- PRAW (Reddit API)
- HuggingFace Inference API
- LangChain
- TinyLlama LLM
- dotenv


# Methds 
The system analyzes Reddit posts and identifies problems using two different approaches: a keyword-based method and an AI-based method. These approaches help detect problem statements and generate meaningful startup ideas automatically.

| Feature               | Keyword Method | AI Method     |
| --------------------- | -------------- | ------------- |
| Speed                 | Very fast      | Slower        |
| Accuracy              | Low            | High          |
| Context understanding | No             | Yes           |
| Idea quality          | Basic          | More creative |


# AI Method 
```
User
  │
  ▼
Python App (app.py)
  │
  ├── Reddit API (PRAW)
  │       │
  │       ▼
  │   Fetch startup problems/posts
  │
  ▼
Data Processing
(filter useful posts)
  │
  ▼
LLM (TinyLlama via HuggingFace)
  │
  ▼
Idea Generation / Classification
  │
  ▼
Output
(TXT file)
```

## Prompt Design
The application uses a carefully structured prompt to guide the Large Language Model (TinyLlama) in analyzing Reddit posts and generating startup ideas.

# Prompt Objectives
The model is instructed to:

- Determine whether the Reddit post describes a real, specific, and solvable problem
- Extract the core problem statement
- Suggest a concrete startup idea (not generic)
- Identify the target users
- Estimate market potential (Low / Medium / High)
- Categorize the solution (SaaS / Marketplace / Mobile App / AI Tool)
- Estimate initial investment required (Low / Medium / High)
- Evaluate customer retention potential (with reasoning)
- Define the revenue model (Subscription, Freemium, Ads, Commission, etc.)
- Determine whether the problem is temporary or recurring
- Identify existing solutions or competitors

The prompt provides the model with clear instructions to respond in a fixed format containing:
- Response: True / False
- Problem:
- Startup Idea:
- Target Users:
- Market Potential:
- Category:
- Initial Investment Required:
- Customer Retention Potential:
- Revenue Model:
- Problem Duration:
- Existing Solutions:

This structured prompting helps ensure that the AI generates consistent, organized, and actionable insights rather than unstructured responses.
Using this prompt structure improves the reliability of the system and makes it easier to process and store the generated results programmatically.


# Conclusion
This project demonstrates how real-world problems discussed on online platforms can be transformed into potential startup opportunities using data and artificial intelligence. By combining Reddit data extraction, keyword-based analysis, and AI-powered reasoning, the system can automatically detect problems and generate innovative startup ideas.

The project highlights the practical integration of APIs and large language models to build intelligent applications. With further improvements such as better ranking systems, databases, and a web interface, this system could evolve into a powerful tool for discovering new startup opportunities.
