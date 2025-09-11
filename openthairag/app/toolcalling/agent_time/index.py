import os
from crewai import LLM, Task, Agent, Crew
from crewai.tools import BaseTool
from datetime import datetime
import pytz
from db import Connection
from dotenv import load_dotenv
load_dotenv()

mongo=Connection('otg_db')


def get_model_env():
    """
    Fetch 'server' and 'local' configs from the settings collection.
    Returns the enabled config's apikey, domainname, and modelname.
    """
    setting = mongo.setting.find_one({}, {"_id": 0, "server": 1, "local": 1})
    if setting:
        if setting.get("server", {}).get("enabled", False):
            config = setting["server"]
        elif setting.get("local", {}).get("enabled", False):
            config = setting["local"]
        else:
            config = {}
        return {
            "isServer": config.get("enabled", False),
            "isLocal": not config.get("enabled", False),
            "apikey": config.get("apikey", ""),
            "domainname": config.get("domainname", ""),
            "modelname": config.get("modelname", "")
        }
    return {"apikey": "", "domainname": "", "modelname": ""}

api_key = get_model_env().get("apikey", "")

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
          api_key=api_key,
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