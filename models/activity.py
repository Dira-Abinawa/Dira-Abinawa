from pydantic import BaseModel

class Activity(BaseModel):
    activity_name : str
    circular_letter : str
    participant_requirements : str
    schedule_of_activities : str