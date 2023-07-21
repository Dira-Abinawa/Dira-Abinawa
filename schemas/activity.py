def ActivityPramuka(item)->dict:
    return {
        "id":str(item["_id"]),
        "activity_name":item["activity_name"],
        "circular_letter":item["circular_letter"],
        "participant_requirements":item["participant_requirements"],
        "schedule_of_activities":item["schedule_of_activities"]
    }
    
def ActivitiesPramuka(entity)->list:
    return [ActivityPramuka(item)for item in entity]