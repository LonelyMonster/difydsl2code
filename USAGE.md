# DeepResearch Usage

## Setup
1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Set environment variables for API access:
   ```bash
   export OPENROUTER_API_KEY=your_openrouter_key
   export TAVILY_API_KEY=your_tavily_key
   ```

## Command Line
Run a research job:
```bash
python -m deepresearch.workflow "your question" --depth 3
```

## Streamlit App
Launch the web UI:
```bash
streamlit run app.py
```
Then open the displayed local URL in your browser to chat with the agent.
