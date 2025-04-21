# Setup

Install the requirements
```
pip install -r requirements.txt
```


Start the server
```
prefect server start
```

Create a work pool
```
prefect work-pool create test-pool --type process
```

Create the deployment
```
prefect deploy --prefect-file prefect.yaml
```

Start the worker
```
prefect worker start --pool test-pool
```

On [localhost:4200/deployments](http://127.0.0.1:4200/deployments), trigger the deployment test_flow with a quick run.



