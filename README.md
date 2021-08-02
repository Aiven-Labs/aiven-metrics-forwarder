# Aiven Metrics Forwarder 
## README

### Purpose

This is a small utility script to grab metrics from an Aiven service and forward to a Dynatrace environment (or any API that accepts Metrics in Influx Line Protocol format). 

This is NOT intended for Production use and comes with no guarantees of functionality. No error handling has been used

### Config

Using the `config.py.sample` file, you can fill out the required fields, most important is the Aiven API Token and the Prometheus config. A help article is available [here](https://help.aiven.io/en/articles/2473061-using-aiven-with-prometheus) for this.

For Dynatrace, the Custom Metrics API is documented [here](https://www.dynatrace.com/support/help/dynatrace-api/environment-api/metric-v2/post-ingest-metrics/).

Metrics can also be grabbed directly from the Aiven API (see `get_avn_metrics`), this will require some transformation from JSON to the Influx Line Protocol and this has not been implemented for this example.

Configuring this to run at intervals could be done in a number of ways, for example:
1. Setting up a cron job
2. Using a `TimerThread` 

### Usage

You can run this using `pipenv`.
1. `pipenv install`
2. `pipenv run python3 main.py`




