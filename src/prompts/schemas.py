from schemas import BaseCreate, BaseUpdate

class PromptCreate(BaseCreate):
    text: str
    parent_id: str | None = None

class UnapprovedPrompt(PromptCreate):
    id: str
    creator_id: int
    # is_locked: bool
    
class PromptUpdate(BaseUpdate):
    text: str | None = None
    parent_id: str | None = None