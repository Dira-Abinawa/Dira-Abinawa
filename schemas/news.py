def NewPramuka(item)->dict:
    return {
        "id":str(item["_id"]),
        "title":item["title"],
        "description":item["description"],
        "content":item["content"],
        "thumbnail": item.get("thumbnail")
    }
    
def NewsPramuka(entity)->list:
    return [NewPramuka(item)for item in entity]