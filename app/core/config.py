

import os

# NOTE FOR STUDENTS:
# During the guest lecture, this demo used the lecturer's Azure OpenAI credentials.
# If you are running this project yourself, you will need to configure your own
# language model access. Possible options include:
#
# - Azure OpenAI (similar setup using your own Azure account)
# - OpenAI API
# - A local LLM using tools such as Ollama
# - A hosted model via Hugging Face Inference API
#
# Update the configuration and story_service.py accordingly depending on the
# model provider you choose.


LLM_API_KEY = os.environ.get("LLM_API_KEY")
LLM_API_ENDPOINT = os.environ.get("LLM_API_ENDPOINT")
LLM_MODEL = os.environ.get("LLM_MODEL")

DEFAULT_RADIUS_METERS = 1000
LANGUAGE = "en"