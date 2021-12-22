from typing import List
from fastapi import APIRouter
from starlette.responses import Response
from config.db import userDC
from schemas.user import userEntity
from models.user import User
from models.chef import Chef
from models.category import Category
from models.vrecipe import VRecipe
from utils.categoriesStructure import categoriesInitial
from utils.vrStructure import vrInitial
from utils.algorithm import Analize

import json

user = APIRouter()

@user.get("/user/{uid}")
def createUserData(uid: int):
    if userDC.find_one({"uid": uid}):
        return f"El usuario con id {uid} ya fue creado!"
    new_user = {
        "uid": uid,
        "categories": categoriesInitial,
        "viewedRecipes": vrInitial,
        "RNVRecipes": {},
        "chefs": {},
    }
    res = userDC.insert_one(new_user)

    return str(res.inserted_id)

@user.post("/user/{uid}")
def getUserSortedData(uid: int, data: list):
    if userDC.find_one({"uid": uid}):
        analized = Analize(uid,data)
        print(f"Sorted data: \n {analized}")
        return Response(json.dumps({"recipes":analized}), 200,{"Content-Type":"application/json"})

    return f"El usuario no existe!!!"

@user.delete("/user/{uid}")
def deleteUserData(uid: int):
    res = userDC.delete_one({"uid": uid})
    return f"Usuario eliminado, UID del usuario: {uid} | Documentos eliminados: {res.deleted_count}"


# Routes for chef
@user.get("/user/{uid}/chefs")
def obtainAllChefs(uid: int):
    res = dict(userDC.find_one({"uid": uid}, {"_id":0,"chefs":1})).get("chefs")
    return res

@user.post("/user/{uid}/chefs")
def interactWithChef(uid: int, chef: Chef):
    chefToInsert = dict(chef)
    chefid = str(dict(chef).get('chefid'))
    uinfo = userDC.find_one({"uid":uid})
    if uinfo is not None:
        chefinfo = dict(dict(uinfo).get("chefs")).get(chefid)
        if chefinfo is None:
            chefToInsert["lastCountRate"] = 1
            chefToInsert["lastRateSum"] = chefToInsert["rate"]
            chefToInsert.pop("chefid")
            userDC.find_one_and_update({"uid":uid},{"$set":{f"chefs.{chefid}":chefToInsert}})
            return str(f"Chef con ID {str(dict(chef).get('chefid'))} creado con éxito")
        else:
            chefinfo["viewedTime"] = int(chefinfo["viewedTime"]) + int(chefToInsert["viewedTime"])
            chefinfo["lastCountRate"] = int(chefinfo["lastCountRate"]) + 1
            chefinfo["lastRateSum"] = float(chefinfo["lastRateSum"]) + float(chefToInsert["rate"])
            chefinfo["rate"] = chefinfo["lastRateSum"] / chefinfo["lastCountRate"]
            chefinfo["savedRecipes"] = int(chefinfo["savedRecipes"]) + int(chefToInsert["savedRecipes"])
            chefinfo["isReported"] = bool(chefinfo["isReported"])
            print(chefinfo)
            userDC.find_one_and_update({"uid": uid},{"$set": {f"chefs.{chefid}":chefinfo}})
            return str(f"Chef con ID {chefid} actualizado con éxito")
    
    return Response(json.dumps({"Status": "Bad request", "ERROR": "ERROR User Not Found"}),400,{"Content-Type":"application/json"})

# Routes for categories 

@user.post("/user/{uid}/cats")
def registerCategoryView(uid: int, cats: Category):
    cats = dict(cats)
    uinfo = userDC.find_one({"uid":uid})
    if uinfo is not None:
        catstats = dict(userDC.find_one({"uid":uid},{f"categories.{cats['region']}": 1, "_id":0})).get("categories").get(cats["region"])
        catstats["timesVisited"] += 1
        for tag in cats["tags"]:
            catstats[tag] += 1

        userDC.find_one_and_update({"uid":uid},{"$set": {f"categories.{cats['region']}": catstats}})
        return Response(json.dumps({"Status": "200 Ok", "MSG": "Categories Updated"}),200,{"Content-Type":"application/json"})

    return Response(json.dumps({"Status": "Bad request", "ERROR": "ERROR User Not Found"}),400,{"Content-Type":"application/json"})


# Routes for viewedVideos

@user.get("/user/{uid}/vr")
def getVieweds(uid: int):
    uinfo = userDC.find_one({"uid":uid})
    if uinfo is not None:
        ids = dict(userDC.find_one({"uid":uid}, {"viewedRecipes.video_ids":1,"_id":0})).get("viewedRecipes").get("video_ids")
        return Response(json.dumps({"ids":ids}),200)
        
    return Response(json.dumps({"Status": "Bad request", "ERROR": "ERROR User Not Found"}),400,{"Content-Type":"application/json"})


@user.post("/user/{uid}/vr")
def appendViewedRecipe(uid: int, recipe: VRecipe):
    uinfo = userDC.find_one({"uid":uid})
    recipe = dict(recipe)
    if uinfo is not None:
        rInfo = dict(userDC.find_one({"uid":uid}, {"viewedRecipes":1,"_id":0})).get("viewedRecipes")
        rInfo["num"] += 1
        rInfo["last_sum"] += recipe["viewedSeconds"]
        if rInfo["max"] < recipe["videoDuration"]:
            rInfo["max"] = recipe["videoDuration"]
        
        rInfo["avg_secs"] += rInfo["last_sum"] / rInfo["num"]
        rInfo["video_ids"].append(recipe["recipeid"])

        userDC.find_one_and_update({"uid": uid}, {"$set": {"viewedRecipes":rInfo}})

        print(rInfo)
        return Response(json.dumps({"Status": "200 Ok", "Msg": "Good Ending"}),200,{"Content-Type":"application/json"})

    return Response(json.dumps({"Status": "Bad request", "ERROR": "ERROR User Not Found"}),400,{"Content-Type":"application/json"})
    