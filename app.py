import praw
from prawcore.exceptions import RequestException, ResponseException, Forbidden, NotFound
from access import client_id, client_secret, user_agent
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# LLM Setup
try:
    llm = HuggingFaceEndpoint(
        repo_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        task="text-generation",
        max_new_tokens=300,
        temperature=0.7
    )

    model = ChatHuggingFace(llm=llm)

except Exception as e:
    print("Error initializing LLM:", e)
    exit()


# Reddit API Setup
try:
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

except Exception as e:
    print("Error initializing Reddit API:", e)
    exit()


subreddits = [
    "Entrepreneur",
    "startups",
    "SaaS",
    "smallbusiness",
    "SideProject"
]

problem_keywords = [
    "hate",
    "problem",
    "annoying",
    "wish",
    "struggle",
    "difficult",
    "frustrating",
    "issue"
]

seen_posts = set()

output_file = "startup_ideas.txt"


# Problem Detection
def detect_problem(text):
    try:
        text = text.lower()
        return any(word in text for word in problem_keywords)
    except Exception:
        return False


# Idea Generator
def generate_startup_idea(text):
    try:
        return f"Startup Idea: Build a product that solves -> {text}"
    except Exception as e:
        return f"Idea generation error: {e}"


# LLM Analysis
def analyze_post(text):

    prompt = f"""
A user posted this on Reddit:
Give a precise analysis of the problem mentioned in the post and suggest a startup idea that could solve it. 
Focus on the core issue and how a new product or service could address it.

"{text}"

Your task Identify:
If the post describes a clear problem that can be solved with a startup idea. reply only True/False. If True, also provide:
1. The problem mentioned
2. A startup idea to solve it
3. Target users
4. Market potential (Low / Medium / High)
5. Category (SaaS / Marketplace / Mobile App / AI Tool)
6. Initial Investment Required (Low / Medium / High)
7. Customer Retention Potential
8. Revenue Model (Subscription, One-time, Freemium, Commission, ads etc)
9. Problem Duration (is the problem likely to persist(recurring) or is it a temporary issue?)
10. Existing solutions

Format response as:

Response: True/False
Problem:
Startup Idea:
Target Users:
Market Potential:
Category:
Initial Investment Required:
Customer Retention Potential:
Revenue Model:
Problem Duration
Existing Solutions:

IMPORTANT:
- Do NOT add any extra explanation
- Do NOT change format
- Be concise and specific
"""

    try:
        response = model.invoke(prompt)
        output = response.content.strip()

        for line in output.split("\n"):
            if line.lower().startswith("response"):
                value = line.split(":")[1].strip().lower()

                if value == "true":
                    return True, output
                if value == "false":
                    return False, output

        return False, output

    except Exception as e:
        return False, f"LLM Error: {str(e)}"


# Main Execution
def main():

    with open(output_file, "a", encoding="utf-8") as file:

        for sub_name in subreddits:

            header = f"\n==============================\nScanning subreddit: {sub_name}\n==============================\n"
            file.write(header)

            try:
                subreddit = reddit.subreddit(sub_name)

                for post in subreddit.hot(limit=10):

                    try:

                        if post.id in seen_posts:
                            continue
                        seen_posts.add(post.id)

                        if post.score < 20 and post.num_comments < 5:
                            continue

                        title = post.title.strip()

                        idea_score = post.score * 0.7 + post.num_comments * 0.3

                        is_problem, analysis = analyze_post(title)

                        if not is_problem:
                            continue

                        file.write("\n--------------------------------\n")
                        file.write(f"Reddit Post: {title}\n")
                        file.write(f"Upvotes: {post.score}\n")
                        file.write(f"Comments: {post.num_comments}\n")
                        file.write(f"Idea Score: {round(idea_score,2)}\n\n")

                        file.write("AI Generated Insight:\n")
                        file.write(analysis + "\n")

                        if detect_problem(title):
                            idea = generate_startup_idea(title)

                            file.write("\nKeyword Based Idea:\n")
                            file.write(idea + "\n")
                        else:
                            file.write("\nNo clear problem detected using keywords.\n")

                    except Exception as post_error:
                        file.write(f"\nError processing post: {post_error}\n")
                        continue

            except Forbidden:
                file.write(f"\nAccess forbidden to subreddit: {sub_name}\n")

            except NotFound:
                file.write(f"\nSubreddit not found: {sub_name}\n")

            except RequestException:
                file.write("\nNetwork error while accessing Reddit\n")

            except ResponseException:
                file.write("\nInvalid response from Reddit API\n")

            except Exception as e:
                file.write(f"\nUnexpected error while scanning subreddit: {e}\n")


if __name__ == "__main__":
    main()