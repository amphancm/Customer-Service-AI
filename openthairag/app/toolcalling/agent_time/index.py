import os
from crewai import LLM, Task, Agent, Crew
from crewai.tools import BaseTool
from datetime import datetime
import pytz
from dotenv import load_dotenv
load_dotenv()

class TimeTool(BaseTool):
  name: str = "time_tool"
  description: str = "Useful for getting current date and time information in Thailand timezone. Input should be a natural language query about time or date."

  def _run(self, *args, **kwargs):
    query = kwargs.get("query")
    thailand_tz = pytz.timezone('Asia/Bangkok')
    current_time = datetime.now(thailand_tz).strftime("%Y-%m-%d %H:%M:%S")
    return f"Current time in Thailand: {current_time}"

# Qwen/Qwen3-235B-A22B-Thinking-2507 - นานมาก 0.20
# Qwen/Qwen2.5-72B-Instruct-Turbo - เร็ว

llm = LLM(model="together_ai/Qwen/Qwen2.5-72B-Instruct-Turbo",
          api_key="tgp_v1_X6sy0ZuipjZK1zAmpXpIM6XwPlE7pks6xiZBftKPu9Y",
          base_url="https://api.together.xyz/v1"
        )

time_agent = Agent(
    llm = llm,
    role="Thai Research Analyst",
    goal="Find and summarize information about specific topics",
    backstory="You are an experienced researcher with attention to detail",
    verbose=True,
    tools=[TimeTool()]
)

task = Task(
    description="วันนี้วันที่เท่าไหร่ และตอนนี้เวลาประมาณที่ไทยประมาณกี่โมง",
    expected_output="Answer the general answers in Thai language.",
    agent=time_agent
)


crew = Crew(
    agents=[time_agent],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
time_context = task.output

def get_time_context():
    return time_context