from prompts.repository import PromptRepository
from service import BaseService

class PromptService(BaseService):
    repository = PromptRepository
