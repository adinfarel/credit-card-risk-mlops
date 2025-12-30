from fastapi import FastAPI, Request, Form # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
import uvicorn # type: ignore
from src.pipeline.predict_pipeline import PredictPipeline, CustomData
from prometheus_fastapi_instrumentator import Instrumentator # type: ignore

app = FastAPI(title="CreditRisk AI")

Instrumentator().instrument(app).expose(app)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/predict", response_class=HTMLResponse)
async def get_predict(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def post_predict(
    request: Request,
    person_age: int = Form(...),
    person_income: float = Form(...),
    person_home_ownership: str = Form(...),
    person_emp_length: float = Form(...),
    loan_intent: str = Form(...),
    loan_grade: str = Form(...),
    loan_amnt: float = Form(...),
    loan_int_rate: float = Form(...),
    cb_person_default_on_file: str = Form(...),
    loan_percent_income: float = Form(...),
    cb_person_cred_hist_length: float = Form(...)
):
    try:
        input_data = CustomData(
            person_age=person_age,
            person_income=person_income,
            person_home_ownership=person_home_ownership,
            person_emp_length=person_emp_length,
            loan_intent=loan_intent,
            loan_grade=loan_grade,
            loan_amnt=loan_amnt,
            loan_int_rate=loan_int_rate,
            cb_person_default_on_file=cb_person_default_on_file,
            loan_percent_income=loan_percent_income,
            cb_person_cred_hist_length=cb_person_cred_hist_length
        )
        
        input_df = input_data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict(input_df)

        input_dict = {
            "person_age": person_age,
            "person_income": person_income,
            "person_home_ownership": person_home_ownership,
            "person_emp_length": person_emp_length,
            "loan_intent": loan_intent,
            "loan_amnt": loan_amnt,
            "loan_int_rate": loan_int_rate,
            "loan_percent_income": loan_percent_income,
            "cb_person_default_on_file": cb_person_default_on_file,
            "cb_person_cred_hist_length": cb_person_cred_hist_length
        }
            
        if prediction[0] == 1:
            return templates.TemplateResponse("result_failed.html", {"request": request, "data": input_dict})
        else:
            return templates.TemplateResponse("result_success.html", {'request': request, "data":input_dict})
    
    except Exception as e:
        return templates.TemplateResponse("home.html", {
            "request": request, 
            "error": str(e)
        })

@app.get('/about', response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {'request': request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)