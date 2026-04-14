
from fastapi import FastAPI, HTTPException,Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, field_validator, model_validator,Field,computed_field
from typing import List, Optional,Annotated, Literal,Optional
import json

from sqlalchemy import desc

app = FastAPI()
# getting full data inside the json file
def load_data():
    with open("App/patient.json", "r") as f:
        data=json.load(f)
    return data
def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f)


class patient(BaseModel):
    id:Annotated[...,str,Field(..., description="the id of patient", example=["P001"])]
    name:Annotated[...,str, Field(..., description="the name of patient", example=["john"])]
    age:Annotated[...,int, Field(..., gt=0, lt=100,description="the age of patient", example=[30])]
    height:Annotated[float, Field(..., description="the height of patient", example=["1.75m"])]
    weight:Annotated[float, Field(..., gt=0, description="the weight of patient", example=[70.5])]
    gender:Annotated[...,Literal["Male","Female","Other"],  Field(..., description="the gender of patient")]
    
    @computed_field
    @property
    def BMI(self) -> float:
        bmi=round(self.weight/(self.height**2),2)
        return(bmi)
    @computed_field
    @property
    def verdict(self) -> str:
        if self.BMI<18.5:
            return "underweight"
        elif self.BMI<25:
            return "normal weight"
        return "overweight"
    
# update patient
class update_Patient(BaseModel):
    name:Annotated[Optional,str, Field(..., description="the name of patient", example=["john"])]
    age:Annotated[Optional,int, Field(..., gt=0, lt=100,description="the age of patient", example=[30])]
    height:Annotated[Optional,float, Field(..., description="the height of patient", example=["1.75m"])]
    weight:Annotated[Optional,float, Field(..., gt=0, description="the weight of patient", example=[70.5])]
    gender:Annotated[Optional,Literal["Male","Female","Other"],  Field(..., description="the gender of patient")]



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

# @app.get("/sort")
# def sort_patients(sort_by:str=Query(..., description="the field to sort by, for example: name"),order:str=Query("asc",description="the order of sorting, either 'asc' for ascending or 'desc' for descending")):
#     valid_fields=["height","weight","age","BMI"]
#     if sort_by not in valid_fields:
#         raise HTTPException(status_code=400, detail="invalid sort field, {valid_fields}", )
#     if order not in ["asc","desc"]:
#         raise HTTPException (status_code=400,detail=f"Invalid sort field. Valid fields are: {valid_fields}")
#     data=load_data()
# sortdata=True if order=="desc" else False
# sorted_data=sorted(data.items(), key=lambda x:x[1][sort_by],reverse=sortdata)


# class patient(BaseModel):
#     name:str
#     age:int
#     weight:float
#     married:bool
#     allergies:List[str]

# def patient_record(patient:patient):
#     print(patient.name,patient.age)

# # dictionary

# patient_info={"name":"anurag", "age":20}
# patient1=patient(**patient_info)
# patient_record(patient1)

# class patient(BaseModel):
#     name:str
#     age:int
#     email:EmailStr
#     weight:float
#     married:bool
#     allergies: Annotated[Optional[List[str]], "list of allergies"] = None
# # field validator is used to validate the email field
#     @field_validator("email")
#     # class method is used to give reference to the class
#     @classmethod
#     def validate_email(cls, email):
#         valid_domains=["hdfc.com", "icici.com"]
#         domain_name=email.split("@")[-1]
#         if domain_name not in valid_domains:
#             raise ValueError("invalid email domain")
#         return email




# def patient_record(patient:patient):
#     print(patient.name,patient.age,patient.email,patient.weight,patient.married,patient.allergies)


# patient_info={"name":"anurag", "age":20, "email":"anurag@hdfc.com", "weight":70.5, "married":"false", "allergies":["pollen","dust"]}

# patien1=patient(**patient_info)

# patient_record(patien1)

# class student():
#     name:str
#     age:int
#     def __init__(self):
#        self.name="anurag"
#        self.age=20

# student1=student()
# print(student1.name, student1.age)

@app.post("/create")
# in the patient variable we passed data for validation as patient
def create_patient(patient:patient):
    #load all existing data
    data=load_data()

    # check if patient id already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='patient id already exists')
    
    # if  not exist then add new patient in to the database
    # but before adding it will convert it in to patient model in to dictionary
    data[patient.id]= patient.model_dump(exclude=[id])
    # now we have to save this in database for this will create a utility function to save data on top
    save_data(data)
    #now will send the response to client for that we use fastapi.response
    return JSONResponse(status_code=201, content="patient created successfully")
# for edit
@app.put('/edit/{patient_id}')
def update_patient(patient_id:str,patient_update:update_Patient ):
    # load full data
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="patient not found")
    # get existing patient id data
    existing_patient=data[patient_id]
    # convert existing patient object in to dictionary
    patient_update_dict=patient_update.model_dump(exclude_unset=True)
    for key, value in patient_update_dict.items():
        # changing key with new value
        existing_patient [key]=value
        existing_patient[key]=patient_id
        patient_pydantic_object= patient(**existing_patient)
        existing_patient= patient_pydantic_object.model_dump(exclude=id)
        # now we will merge all data into dictionary
        # existing_patient-->convert in to object, bmi+verdict--->pydanticobject--->dict
        data[patient_id]=existing_patient
        save_data(data)
        return JSONResponse(status_code=200,content={"messsage":"patient updated successfully"})









@app.delete('/delete/{patient_id}')
def del_patient(patient_id:str):
    data=load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, details="patient not found")
    del data[patient_id]
    save_data(data)
    return{"message":"{patient_id}deleted successfully"}






    
 

    




    
    
