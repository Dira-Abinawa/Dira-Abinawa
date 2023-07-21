def DataPotensi(item:dict)-> dict:
    return {
        "id": str(item["_id"]),
        "school_name": str(item["school_name"]),
        "male_builder": item.get("male_builder", None),
        "female_builder": item.get("female_builder", None),
        "male_member": item.get("male_member", None),
        "female_member": item.get("female_member", None),
        "bantara_member": item.get("bantara_member", None),
        "laksana_member": item.get("laksana_member", None),
        "garuda_member": item.get("garuda_member", None),
    }
    
def DatasPotensi(entity)->list:
    return [DataPotensi(item)for item in entity]