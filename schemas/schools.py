def SchoolPadalarang(item)->dict:
    return {
        "id":str(item["_id"]),
        "school_name":item["school_name"],
        "basis_name":item["basis_name"],
        "male_ambalan_name":item["male_ambalan_name"],
        "female_ambalan_name": item.get("female_ambalan_name", "")
    }
def SchoolsPadalarang(entity)->list:
    return[SchoolPadalarang(item)for item in entity]