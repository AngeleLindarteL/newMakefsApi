def userEntity(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "uid": item["uid"],
        "categories": item["categories"],
        "chefs": item["chefs"],
        "rnv": item["rnv"],
        "vw": item["vw"],
    }


def usersEntity(entities) -> list:
    return [userEntity(entity) for entity in entities]
