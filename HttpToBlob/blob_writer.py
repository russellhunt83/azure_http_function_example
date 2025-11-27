import json
import uuid
from datetime import datetime
from typing import Any
from azure.storage.blob import BlobServiceClient

def generate_blob_name(prefix: str = "payload") -> str:
    """Generate a unique blob name using timestamp and uuid."""
    now = datetime.now().strftime("%Y%m%dT%H%M%S%fZ")
    return f"{prefix}_{now}_{uuid.uuid4().hex}.json"


def serialize_payload(payload: Any) -> bytes:
    """Serialize a JSON-serializable payload to normalized bytes."""
    return json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def upload_blob(connection_string: str, container: str, payload: Any, blob_name: str = None) -> str:
    """Upload the payload to blob storage and return the blob name.

    This function performs the network call. For unit tests, test `generate_blob_name` and `serialize_payload` instead.
    """
    if blob_name is None:
        blob_name = generate_blob_name()

    data = serialize_payload(payload)
    # Import Azure SDK only when performing network/upload operations so module import
    # is lightweight and unit-tests that import this module don't require the package.
  
    client = BlobServiceClient.from_connection_string(connection_string)
    container_client = client.get_container_client(container)
    # Create container if doesn't exist (idempotent)
    try:
        container_client.create_container()
    except Exception:
        # ignore; container may already exist or insufficient permissions
        pass

    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(data, overwrite=True)
    return blob_name
