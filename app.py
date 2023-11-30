## Import the needed libraries
import requests
from decouple import config
from loguru import logger
from typing import Any
from datetime import datetime


# Get environment variables using the config object or os.environ["KEY"]
# These are the credentials passed by the variables of your pipeline to your tasks and in to your env

PORT_CLIENT_ID = config("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = config("PORT_CLIENT_SECRET")
DYNATRACE_API_KEY = config("DYNATRACE_API_KEY")
DYNATRACE_HOST_URL = config("DYNATRACE_HOST_URL")
DYNATRACE_ENTITY_SELECTORS = config("DYNATRACE_ENTITY_SELECTOR", default=None)
PORT_API_URL = "https://api.getport.io/v1"
DEFAULT_ENTITY_TYPES = {"KUBERNETES_SERVICE", "DATASTORE", "APPLICATION", "HOST", "SERVICE"}

## Get Port Access Token
credentials = {'clientId': PORT_CLIENT_ID, 'clientSecret': PORT_CLIENT_SECRET}
token_response = requests.post(f'{PORT_API_URL}/auth/access_token', json=credentials)
access_token = token_response.json()['accessToken']

# You can now use the value in access_token when making further requests
headers = {
	'Authorization': f'Bearer {access_token}'
}
dynatrace_headers = {'Authorization': f'Api-Token {DYNATRACE_API_KEY}', 'Accept': 'application/json'}


def add_entity_to_port(blueprint_id, entity_object):
    """A function to create the passed entity in Port

    Params
    --------------
    entity_object: dict
        The entity to add in your Port catalog
    
    Returns
    --------------
    response: dict
        The response object after calling the webhook
    """
    response = requests.post(f'{PORT_API_URL}/blueprints/{blueprint_id}/entities?upsert=true&merge=true', json=entity_object, headers=headers)
    logger.info(response.json())

def get_paginated_resource(params: dict[str, Any] = None, page_size: int = 5):

    url = f"{DYNATRACE_HOST_URL}/api/v2/entities"
    next_page_key = None

    while True:
        try:
            if next_page_key:
                params["nextPageKey"] = next_page_key

            response = requests.get(url=url, headers=dynatrace_headers, params=params)
            response.raise_for_status()
            page_json = response.json()
            batch_data = page_json["entities"]
            yield batch_data
            
            next_page_key = page_json.get("nextPageKey")

            if not next_page_key:
                break
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error with code {e.response.status_code}, content: {e.response.text}")
            raise
    logger.info(f"Successfully fetched paginated data for {params.get('entitySelector')}")

def convert_to_datetime(timestamp: int):
    converted_datetime = datetime.utcfromtimestamp(timestamp / 1000.0)
    return converted_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

def process_dynatrace_entities(entities_data: list[dict[str, Any]]):
    blueprint_id = 'dynatrace_entity'

    for entity in entities_data:
        entity = {
            "identifier": str(entity["entityId"]),
            "title": entity["displayName"],
            "properties": {
                "type": entity["type"],
                "tags": entity["tags"],
                "last_seen": convert_to_datetime(entity["lastSeenTms"]),
                "first_seen": convert_to_datetime(entity["firstSeenTms"])
            },
            "relations": {}
        }
        add_entity_to_port(blueprint_id=blueprint_id, entity_object=entity)



if __name__ == "__main__":
    # Check if DYNATRACE_ENTITY_SELECTOR is not None before splitting
    if DYNATRACE_ENTITY_SELECTORS is not None:
        user_entity_types = set(DYNATRACE_ENTITY_SELECTORS.split(","))
    else:
        user_entity_types = set()

    entity_types = DEFAULT_ENTITY_TYPES.union(user_entity_types)

    for entity_type in entity_types:
        logger.info(f"Paginating request to {entity_type}")
        params: dict[str, Any] = {
            "entitySelector": f"type({entity_type})",
            "fields": "firstSeenTms,lastSeenTms,tags"
        }

        for entities_batch in get_paginated_resource(params=params):
            logger.info(f"Received batch with size {len(entities_batch)} {entity_type} ")
            process_dynatrace_entities(entities_data=entities_batch)
