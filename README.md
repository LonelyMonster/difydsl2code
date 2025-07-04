# difydsl2code
# 这段README是提供给LLM编程的需求，以及LLM随时回来查看的草稿纸和‘记忆中心’
# 我的全局要求
## 任务：
- 我会给你个来自dify workflow导出的DSL，他是一个deepresearch的任务
- 我需要你将这个dsl直接转换成python代码，可以使用langraph或者其他你觉得有必要的库，请你认真解读这个yml，反复检查，最后给我生成**整个工程**
## Workflow的各节点作用：
Simply input what you want to search for, and it will repeatedly execute searches to create a report.  
User Input Reception: The user inputs an initial question (sys.query) and the depth of research (depth).  
Search Initialization: Using GPT-4o, the initial question is analyzed to extract the search theme and determine whether further searches are necessary.  
Iterative Search: Based on the specified depth, multiple rounds of iterative searches are conducted.  
In each iteration, the Tavily search engine is used to conduct searches based on the previously extracted search themes and to collect search results.  
It assesses whether further searches are needed through the LLM and controls the iterative process.  
Analysis and Summary: When the iterative search concludes (or when it is determined that further searches are unnecessary), the deepseek-reasoner model is used to comprehensively analyze and summarize all collected search results.  
Report Generation: The analysis results are generated and output as a final report in Markdown format.
## 环境依赖：
- **如果你需要LLM调用，env环境请配置：**
  <env>
  base_url="https://openrouter.ai/api/v1",
  api_key=""
  </env>
- 你还会用上Tavily Search的调用,env环境请配置
  <env>
  base_url="https://api.tavily.com/search",
  api_key=""
  </env>
- 其他需要配置的内容，请你websearch做进一步规划处理，你可以在dify社区和相关讨论里找到他们的一些资源，以及dsl的定义
## 项目要求：
- 确保真实地调用LLM去解析用户的query，做好上下文的意图的处理，不用指定model，我的openrouter会自己处理
- 确保项目本身足够完备而非一个玩具，是一个完整的工程
- 给这个demo配上一个前端的chat交互
- **在你开始开发前，输出一个完整的计划，让我review**
- **在我确认计划后，将这个计划更新到当前md内，追加，但不要覆盖**
- **你可以在执行的过程中随时查看这个md**
- 在工程输出完成后，自己检查工程能否跑通，确保没有bug再交付给我，并且告诉我一些建议的提问内容
- 在工程输出完成后，新建文件，或者更新下方的内容，生成一个readme，告诉其他看到这个项目的人类如何配置
- 输出代码时不要带上 ''' triple-quoted string '''去注释掉部分代码，这样我的工程很难跑通，查起来很累

# 下面是你的规划，你可以反复读写此处，但请不要覆盖我的全局要求
## 计划 Plan
1. 解析 `DeepResearch.yml` 中描述的迭代搜索流程，提炼主要步骤：解析用户问题->生成搜索主题->调用 Tavily 搜索->判断是否继续->累计搜索结果->最终汇总。
2. 使用 `openai` SDK 配合 `OPENROUTER_API_KEY` 与 `TAVILY_API_KEY` 在 `deepresearch` 包中实现该流程，提供 `DeepResearch.run(query, depth)` 接口。
3. 创建命令行脚本与 `streamlit` 前端，允许用户在终端或网页中输入问题和深度并获得 Markdown 报告。
4. 编写 `requirements.txt` 和 README 中的配置说明，包含环境变量与运行方式。
5. 自检代码可运行后提交 PR。
