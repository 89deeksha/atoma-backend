
from fastapi import FastAPI, HTTPException,Path, Query
from pydantic import BaseModel
import json

from sqlalchemy import desc

app = FastAPI()

def load_data():
    with open("App/patient.json", "r") as f:
        data=json.load(f)
    return data


@ app.get("/")
# read_root is the name of the function that will be called when the root endpoint is accessed
def read_root(): 
    return{"message":"hello world"}

@app.get("/about") 
def about():
    return{"message":"this is the about page"}

@app.get("/view")
def view():
    data=load_data()
    return data

# to get specific patient data

@app.get("/patient/{patient_id}")
def get_patient(patient_id:str=Path(...,description="the id of patient,for example:POO1")):
    # getting all data
    data=load_data() 
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(..., description="the field to sort by, for example: name"),order:str=Query("asc",description="the order of sorting, either 'asc' for ascending or 'desc' for descending")):
    valid_fields=["height","weight","age","BMI"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail="invalid sort field, {valid_fields}", )
    if order not in ["asc","desc"]:
        raise HTTPException (status_code=400, detail="invalid sort order)")
    data=load_data()
sortdata=True if oder=="desc" else False
sorted_data=sorted(data.items(), key=lambda x:x[1][sort_by],reverse=sortdata)
    
    