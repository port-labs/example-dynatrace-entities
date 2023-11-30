# Ingesting Dynatrace Entities


## Getting started

In this example you will create a`dynatrace_entity` blueprint that ingests monitored entities from your Dynatrace account. You will then add some python script to make API calls to Dynatrace REST API and fetch data for your account.

## Entity Blueprint
Create the dynatrace entity blueprint in Port using this schema:

```json 
{
  "identifier": "dynatrace_entity",
  "description": "Ingest Dynatrace entities into your software catalog",
  "title": "Dynatrace Entity",
  "icon": "Dynatrace",
  "schema": {
    "properties": {
      "type": {
        "title": "Type",
        "description": "Entity Type",
        "type": "string"
      },
      "tags": {
        "title": "Tags",
        "type": "array"
      },
      "last_seen": {
        "title": "Last Seen",
        "type": "string",
        "format": "date-time"
      },
      "first_seen": {
        "title": "First Seen",
        "type": "string",
        "format": "date-time"
      }
    },
    "required": []
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

## Running the python script

To ingest data from your Dynatrace account to Port, run the following commands: 

```bash
export PORT_CLIENT_ID=<ENTER CLIENT ID>
export PORT_CLIENT_SECRET=<ENTER CLIENT SECRET>
export DYNATRACE_API_KEY=<ENTER DYNATRACE API KEY>
export DYNATRACE_HOST_URL=<ENTER DYNATRACE API URL>
export DYNATRACE_ENTITY_SELECTORS=<ENTER DYNATRACE ENTITY SELECTORS>


git clone https://github.com/port-labs/example-dynatrace-entities.git

cd example-dynatrace-entities

pip install -r ./requirements.txt

python app.py
```

The list of variables required to run this script are:
- `PORT_CLIENT_ID` - Port client ID
- `PORT_CLIENT_SECRET` - Port client secret
- `DYNATRACE_API_KEY` - Dynatrace access token
- `DYNATRACE_HOST_URL` - Dynatrace host such as `https://my-environment-id.live.dynatrace.com`
- `DYNATRACE_ENTITY_SELECTORS` - An optional comma separated list of Dynatrace entity types such as `HOST,APPLICATION,DATASTORE`. If not specified, the default will be `KUBERNETES_SERVICE,DATASTORE,APPLICATION,HOST,SERVICE`. Check [here](./entity_types.json) for a complete list of valid entity types.


Follow the official documentation on how to [generate API key](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication#create-token)