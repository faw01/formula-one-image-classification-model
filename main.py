import base64
import os
import glob
import time
import argparse
from minio import Minio
from minio.error import InvalidResponseError
import urllib3

import uvicorn
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from assets import functions as fct

#TODO: check why we are getting different results minikube vs PC

base_path = '/app/'

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--minio-url')
parser.add_argument('-a', '--access-key')
parser.add_argument('-s', '--secret-key')
parser.add_argument('-d', '--debugging-local')
args = parser.parse_args()

if args.debugging_local == "True":
    base_path = ''

httpClient = urllib3.PoolManager(cert_reqs="CERT_NONE")

minio_client = Minio(args.minio_url,
               access_key=args.access_key,
               secret_key=args.secret_key,
               http_client=httpClient
              )

bucket_name = "classify"

label_to_class, model = fct.initialize_model(
    path = '{}models/f1-racecar-image-classifier.h5'.format(base_path),
    input_path = '{}input/formula-one-cars-images/train'.format(base_path)
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
def dynamic_file(request: Request, local_debugging = args.debugging_local):
    return templates.TemplateResponse(
        "index.html", 
        {
            "request": request,
            "debugging_local": local_debugging
        }
    )

#TODO: could create endpoint with API response only

@app.post("/predict")
def dynamic(request: Request, file: UploadFile = File(), local_debugging = args.debugging_local):

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

    original_filename = file.filename
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

    current_timestamp = int(str(time.time()).replace('.', ''))

    minio_client.fput_object(
        bucket_name, '{}_{}'.format(current_timestamp, original_filename), source_content_filepath
    )

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
            "chart_filepath": chart_html_file,
            "debugging_local": local_debugging
            }
        )     

uvicorn.run(app, host = "0.0.0.0")