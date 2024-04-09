import base64
import os
import glob

import uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from assets import functions as fct

#TODO: could move it to docker/minikube app arguments done with argument_parser
#TODO: enable PC debugging (paths below)
#TODO: check why we are getting different results minikube vs PC

label_to_class, model = fct.initialize_model(
    path = '/app/models/f1-racecar-image-classifier.h5',
    input_path = '/app/input/formula-one-cars-images/train'
)

app = FastAPI()
app.mount(
    "/static", 
    StaticFiles(directory="static"), 
    name="static"
)

templates = Jinja2Templates(directory="templates")

files = {
    item: os.path.join('static', item)
    for item in os.listdir('static')
}

target_chart_html_file = ""

@app.get("/healthcheck")
async def root():
    return {"message": "Hello World"}

@app.get("/")
def dynamic_file(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#TODO: could create endpoint with API response only

@app.post("/predict")
def dynamic(request: Request, file: UploadFile = File()):

    is_image = 0

    base64_extensions = {
        '.jpg': "/9j/",
        '.png': "iVBO",
        '.gif': "R0lG",
        '.tif': "SUkq"
    }
    base64_extensions_bytes_flattened = [x for xs in list(base64_extensions.items()) for x in xs] 

    # cleanup stuff at the beginning of each processing
    files = glob.glob('./static/temp_file*')
    for f in files:
        os.remove(f)

    data = file.file.read()
    file.file.close()

    # encoding the content
    encoded_entry_content = base64.b64encode(data).decode("utf-8")

    start_bytes_source_file = encoded_entry_content[0:4]

    # TODO: I think it could be improved, to get filenames more easily
    if start_bytes_source_file in base64_extensions_bytes_flattened: #.jpg, .png, .gif, .tif, .tif
        is_image = 1
        source_file_extension = [k for k,v in base64_extensions.items() if v == start_bytes_source_file][0]
        
    source_content_filepath = "./static/temp_file{}".format(source_file_extension)

    with open(source_content_filepath, "wb") as binary_file:
        binary_file.write(data)
    binary_file.close()

    if is_image == 1:
        response = fct.predict_image(
            source_content_filepath, 
            model,
            label_to_class
        )
        target_chart_html_file = fct.make_chart(response)
    
    result_content_filepath = source_content_filepath.replace('./static/', '')
    chart_html_file = target_chart_html_file.replace('./static/', '')

    return templates.TemplateResponse(
        "predict.html", {
            "request": request, 
            "output": response, 
            "is_image": is_image,
            "content_filepath": result_content_filepath,
            "chart_filepath": chart_html_file
            }
        )     

uvicorn.run(app, host = "0.0.0.0")