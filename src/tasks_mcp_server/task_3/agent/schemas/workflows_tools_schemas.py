from pydantic import BaseModel, Field

# ----------------------wf1 input schema ------------------------------- 
class LinkJobAndCallInput(BaseModel):
    transcript: str = Field(
        ...,
        description=(
            "The call transcript containing information used to "
            "identify and link the relevant job and call."
        ),
    )