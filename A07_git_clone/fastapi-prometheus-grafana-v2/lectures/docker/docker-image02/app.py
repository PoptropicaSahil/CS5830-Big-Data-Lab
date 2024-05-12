#!/usr/bin/python

#!pip install spacy fastapi
#!pip install python-multipart

from fastapi import FastAPI, Body, UploadFile, File
from pydantic import BaseModel
import spacy
import uvicorn

nlp_en = spacy.load("en_core_web_sm")
app = FastAPI(title="First AI application with File upload option")

class Data(BaseModel):
    text:str

@app.post("/np")
def extract_np(data:Data, lang:str):
    """This code defines a FastAPI endpoint at "/np" that takes a Data object and a language string as input. It processes the text from the Data object using a spaCy model loaded as nlp_en to extract noun phrases. Finally, it returns a dictionary containing the input text, the extracted noun phrases, and the language provided."""
    doc_en = nlp_en(data.text)
    nps = [ch for ch in map(lambda x: x.text, doc_en.noun_chunks)]
    return {"input":data.text, "NP":nps, "lang":lang}

@app.post('/ne')
def extract_ne(data:Data):
    """The selected code defines a FastAPI endpoint at "/ne" that takes a Data object as input. It processes the text from the Data object using a spaCy model loaded as nlp_en to extract named entities. Finally, it returns a dictionary containing the input text, the extracted named entities, and the language "en".

The code uses the spaCy function doc.ents to extract named entities from the input text. The function map() is used to iterate over the entities and create a tuple of (entity text, entity label) for each entity. The function dict() is used to convert the list of tuples into a dictionary, where the key is the entity text and the value is the entity label.

The function returns a dictionary containing the input text, the extracted named entities, and the language "en"."""
    doc_en = nlp_en(data.text)
    ne = dict(map(lambda x: (x.text,x.label_), doc_en.ents))
    return {"input":data.text, "NE":ne}

def process_text(text:str):
    """The selected code defines a function named process_text that takes a string text as input. The function first splits the input text into lines using the split("\n") method. It then iterates over each line in the list of lines. If a line is empty, it skips processing that line.

For each non-empty line, it uses the spaCy model nlp_en to process the line and extract noun phrases. The nlp_en.noun_chunks attribute returns a list of noun chunks (noun phrases) in the input text. The map() function is used to iterate over the noun chunks and extract the text of each chunk. The list of noun phrases is then stored in the nps variable.

A dictionary record is created with the input line and the list of noun phrases. This dictionary is then added to the records list.

Finally, the function returns a dictionary containing the records list, which is a list of dictionaries, each containing an input line and the corresponding list of noun phrases extracted from that line.

This function is used in the /nptext endpoint to process text input and return the extracted noun phrases. It is also used in the /upload endpoint to process the text content of an uploaded file and return the extracted noun phrases.
"""
    lines = text.split("\n")
    records = []
    for line in lines:
        if line == "":
            continue
        doc_en = nlp_en(line)
        nps = [ch for ch in map(lambda x: x.text, doc_en.noun_chunks)]
        record = {"input":line, "NP":nps}
        records.append(record)
    return {"results": records}

@app.post("/nptext")
async def extract_body(text:str=Body(...)):
    """The selected code defines a FastAPI endpoint at "/nptext" that takes a string text as input through the Body parameter. The Body parameter is annotated with  which means it's a required parameter and it's type is inferred from the value it receives.
The function extract_body processes the input text using the process_text function (defined in lines 32-46). The process_text function splits the input text into lines, processes each line using the spaCy model nlp_en to extract noun phrases, and stores the results in a dictionary record. The dictionary record is then added to a list of records.
Finally, the extract_body function returns the list of records containing the input lines and the corresponding lists of noun phrases extracted from those lines.
This endpoint is used to process text input and return the extracted noun phrases. It is also used in the /upload endpoint to process the text content of an uploaded file and return the extracted noun phrases."""
    return process_text(text)

@app.post("/upload")
async def extract_ne_from_upload(file: UploadFile = File(...)):
    """
    This function is a FastAPI endpoint that handles the upload of a file. It takes a file as input through the `file` parameter. The `file` parameter is annotated with `UploadFile` and `File(...)` which means it's a required parameter and it's type is inferred from the value it receives.

    The function reads the content of the uploaded file and decodes it into a string. The decoded string is then passed to the `process_text` function to extract named entities.

    The function returns the result of the `process_text` function, which is a dictionary containing the input text and the extracted named entities.

    Parameters:
    - file (UploadFile): The uploaded file.

    Returns:
    - dict: A dictionary containing the input text and the extracted named entities.
    """
    content_bytes = file.file.read()
    content_text = content_bytes.decode()
    return process_text(content_text)

# Run from command line: uvicorn ai_app:app --port 7000 --host 0.0.0.0
# or invoke the code below.
uvicorn.run(app, host='0.0.0.0', port=7000)