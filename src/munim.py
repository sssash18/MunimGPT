import os
from dotenv import load_dotenv
load_dotenv()
from promptflow.core import Prompty, AzureOpenAIModelConfiguration
from promptflow.tracing import start_trace
start_trace()

model_config = AzureOpenAIModelConfiguration(
    azure_deployment=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
def analyze(image_data):
  prompty = Prompty.load("artifacts/prompt.prompty", model={'configuration': model_config})
  result = prompty(
      chat_input="Do other Azure AI services support this too?",
      image_data=image_data)
  return result

