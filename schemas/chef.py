def userEntity(item) -> dict:
    return {
        "chefid": item["chefid"],
        "viewedTime": item["viewedTime"],
        "rate": item["rate"],
        "savedRecipes": item["savedRecipes"],
        "isReported": item["isReported"],
        "lastCountRate": item["lastCountRate"],
        "lastRateSum": item["lastRateSum"],
    }