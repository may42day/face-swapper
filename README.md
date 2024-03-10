# Face changer

This is an initial version for test task. Future iterations are expected to implement Celery and Docker integration, utility function segmentation, code coverage with tests and detailed code commenting.

---
## Instalation

1. Download `inswapper_128.onnx` to `~/.insightface/models/`
```
mkdir -p ~/.insightface/models/ ; wget -P ~/.insightface/models/ -O ~/.insightface/models/inswapper_128.onnx https://huggingface.co/Devia/G/resolve/main/inswapper_128.onnx?download=true
```
2. Clone the repository
```
$ git clone <link>
$ cd <link>
```
3. Create virtual environment and install the dependencies. **Python3.11 required**
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Fill in .env file or use .env_example:
```
$ mv .env_example .env
```
5. Run the application  
**The initial run initiates the download of buffalo_l to .insightface\models**
```
uvicorn src.main:app --reload
```

## Endpoints
`POST` /api/v1/swapper/in-swapping : Perform face swapping using the provided images or URLs.  
Supports a combination of different types  
  
Data required:  
`face_image`: The image or URL with face  
`source_image`: The image or URL for replacing faces
```
curl --location 'http://127.0.0.1:8000/api/v1/swapper/in-swapping' \
--form 'face_image="<LINK WITH IMAGE>"' \
--form 'source_image="<LINK WITH IMAGE>"'
```
or
```
curl --location 'http://127.0.0.1:8000/api/v1/swapper/in-swapping' \
--form 'face_image=@"<PATH TO FILE>"' \
--form 'source_image=@"<PATH TO FILE>"'
```
