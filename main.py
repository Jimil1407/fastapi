import json
from fastapi import FastAPI 
from fastapi.params import Query

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/sort_patients")
def sort_patients(sort_by: str = Query(..., description="The field to sort by"), order: str = Query(..., description="The order to sort by")):
    with open("patients.json", "r") as f:
        patients = json.load(f)
    if sort_by in ["name", "height", "weight", "bmi"]:
        sorted_patients = sorted(patients, key=lambda x: x[sort_by], reverse=order == "desc")
    else:
        return {"error": "Invalid sort_by parameter"}
    
    if order not in ["asc", "desc"]:
        return {"error": "Invalid order parameter"}
    
    if order == "desc":
        sorted_patients.reverse()
    
    return sorted_patients

@app.post("/add_patient")
def add_patient(patient: dict):
    with open("patients.json", "r") as f:
        patients = json.load(f)
    patients.append(patient)
    with open("patients.json", "w") as f:
        json.dump(patients, f)
    return {"message": "Patient added successfully"}

@app.get("/get_patient")
def get_patient(name: str):
    with open("patients.json", "r") as f:
        patients = json.load(f)
    for patient in patients:
        if patient["name"] == name:
            return patient
    return {"error": "Patient not found"}

@app.delete("/delete_patient")      
def delete_patient(name: str):
    with open("patients.json", "r") as f:
        patients = json.load(f)
    for patient in patients:
        if patient["name"] == name:
            patients.remove(patient)
            with open("patients.json", "w") as f:
                json.dump(patients, f)
            return {"message": "Patient deleted successfully"}
    return {"error": "Patient not found"}