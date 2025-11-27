import os
import logging

import azure.functions as func
# Custom module to handle blob writing
from . import blob_writer

def main(req):
    logging.info("HttpToBlob function processed a request.")

    try:
        # Handles Sensor Data decoding
        payload = req.get_json()
    except Exception:
        if func:
            return func.HttpResponse("Invalid JSON payload", status_code=400)
        return ("Invalid JSON payload", 400)

    conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not conn:
        if func:
            return func.HttpResponse("Storage connection string not configured", status_code=500)
        return ("Storage connection string not configured", 500)

    container = os.getenv("BLOB_CONTAINER_NAME", "incoming")

    try:
        blob_name = blob_writer.generate_blob_name()
        uploaded = blob_writer.upload_blob(conn, container, payload, blob_name)
        if func:
            return func.HttpResponse(f"Uploaded as {uploaded}", status_code=200)
        return (f"Uploaded as {uploaded}", 200)
    except Exception as e:
        logging.exception("Failed to upload blob")
        if func:
            return func.HttpResponse(f"Error uploading payload: {e}", status_code=500)
        return (f"Error uploading payload: {e}", 500)
