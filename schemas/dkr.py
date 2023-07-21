def DewanKerja(item)->dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "school_name":item["school_name"],
        "level":item["level"],
        "position":item["position"],
        "period":item["period"],
    }
    
def DewansKerja(entity)->list:
    return [DewanKerja(item)for item in entity]