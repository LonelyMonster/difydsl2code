import os
import json
import requests
from typing import List
import openai

class DeepResearch:
    def __init__(self, openrouter_api_key: str, tavily_api_key: str, base_url: str = "https://openrouter.ai/api/v1"):
        self.openrouter_api_key = openrouter_api_key
        self.tavily_api_key = tavily_api_key
        openai.api_key = openrouter_api_key
        openai.api_base = base_url

    def _llm(self, messages: List[dict], model: str = "gpt-4o") -> str:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content

    def _search(self, query: str) -> str:
        url = "https://api.tavily.com/search"
        headers = {"Authorization": f"Bearer {self.tavily_api_key}"}
        payload = {"query": query, "search_depth": "advanced"}
        res = requests.post(url, json=payload, headers=headers, timeout=30)
        res.raise_for_status()
        data = res.json()
        # Tavily may return `answer` field containing a textual summary
        return data.get("answer", str(data))

    def run(self, query: str, depth: int = 3) -> str:
        topics: List[str] = []
        findings: List[str] = []
        next_topic = query
        for _ in range(depth):
            messages = [
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": f"Analyze the question and suggest next search topic and whether to continue. Question: {next_topic}. Respond with JSON having keys nextSearchTopic and shouldContinue."}
            ]
            reply = self._llm(messages)
            try:
                data = json.loads(reply)
            except json.JSONDecodeError:
                data = {"nextSearchTopic": next_topic, "shouldContinue": "false"}
            next_topic = data.get("nextSearchTopic", next_topic)
            topics.append(next_topic)
            search_result = self._search(next_topic)
            findings.append(search_result)
            if str(data.get("shouldContinue", "false")).lower() != "true":
                break
        summary_prompt = [
            {"role": "system", "content": "You summarize research findings into a markdown report."},
            {"role": "user", "content": f"Topics: {topics}\nFindings: {findings}\nProvide a concise markdown report."}
        ]
        report = self._llm(summary_prompt, model="deepseek-chat")
        return report

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run DeepResearch workflow")
    parser.add_argument("query", help="initial question")
    parser.add_argument("--depth", type=int, default=3, help="search depth")
    args = parser.parse_args()
    openrouter_api_key = os.environ.get("OPENROUTER_API_KEY")
    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    if not openrouter_api_key or not tavily_api_key:
        raise RuntimeError("OPENROUTER_API_KEY and TAVILY_API_KEY must be set")
    dr = DeepResearch(openrouter_api_key, tavily_api_key)
    report = dr.run(args.query, depth=args.depth)
    print(report)

if __name__ == "__main__":
    main()
