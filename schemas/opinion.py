def OpinionPramuka(item)->dict:
    return {
        "id":str(item["_id"]),
        "sender_name":item["sender_name"],
        "subject":item["subject"],
        "content":item["content"]
    }
    
def OpinionsPramuka(entity)->list:
    return [OpinionPramuka(item)for item in entity]