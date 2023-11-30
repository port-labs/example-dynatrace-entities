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

git clone https://github.com/port-labs/datadog-service-catalog.git

cd datadog-service-catalog

pip install -r ./requirements.txt

python app.py
```

The list of variables required to run this script are:
- `PORT_CLIENT_ID`
- `PORT_CLIENT_SECRET`
- `DYNATRACE_API_KEY`
- `DYNATRACE_HOST_URL`

Please note that by deafult, all Datadog API clients are configured to consume Datadog US site APIs (https://api.datadoghq.com). If you are on the Datadog EU site, set the environment variable `DATADOG_API_URL` to `https://api.datadoghq.eu`. Some Datadog clients may require you to add your account region to the API. In this case, you may change the DATADOG_API_URL to `https://api.<region>.datadoghq.com` or `https://api.<region>.datadoghq.eu`

Follow the official documentation on how to [generate API key](https://docs.dynatrace.com/docs/dynatrace-api/basics/dynatrace-api-authentication#create-token)