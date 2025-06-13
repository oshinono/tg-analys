from schemas import BaseCreate, BaseUpdate

class PromptCreate(BaseCreate):
    text: str
    parent_guid: str | None = None

class UnapprovedPrompt(PromptCreate):
    guid: str
    creator_id: int
    # is_locked: bool
    
class PromptUpdate(BaseUpdate):
    text: str | None = None
    parent_guid: str | None = None