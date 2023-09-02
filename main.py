from fastapi import FastAPI, Path, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name:str
    price:float
    brand:Optional[str] = None

class UpdateItem(BaseModel):
    name:Optional[str] = None
    price:Optional[float] = None
    brand:Optional[str] = None

@app.get("/")
def home():
    return {"Data": "Test"}

@app.get("/about")
def about():
    return {"Data": "about"}

inventory = {
}

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(..., description="The ID of the item youd like to view", gt=0)):
    return inventory[item_id]

@app.get("/get-by-name/{name}")
def get_item(name: Optional[str] = None):
    "list comprehension"
    items = [item_data for item_id, item_data in inventory.items() if item_data["name"] == name]
    if items:
        return items
    else:
        raise HTTPException(status_code=404)

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item:Item):
    inventory[item_id] = item
    return {"message": "item created successfully",
            "id": item_id }

@app.put("/update-item/{item_id}")
def update_item(item_id:int, item:UpdateItem):
    if item_id not in inventory:
        return {"Error": "item id does not exist."}
    
    if item.name != None:
        inventory[item_id].name = item.name
    
    if item.price != None:
        inventory[item_id].price = item.price
    
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]

@app.delete("/delete-item/{item_id}")
def delete_item_by_id(item_id:int):
    if item_id in inventory:
        del inventory[item_id]
        return {"message": "item successfully deleted."}
    else:
        return {"message": "item did not successfully delete."}