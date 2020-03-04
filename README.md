# General

REST API based on python Flask web framework. 
App calculating average of data points.
Calculating takes place in parallel service.

# Current main functionalities

- GET `/health`

Respond 200 status code whether app is running

- POST `/api/add_customers`

Request body should look like:

```
[
    {"name":"example1", "t":13515551,"v":1.1},
    {"name":"example1", "t":13515552,"v":2.4},
    {"name":"example1", "t":13515553,"v":3.5},
    {"name":"example2", "t":13515554,"v":1.5},
    {"name":"example2", "t":13515555,"v":2.5},
]
```

Respond 201 Accepted response whether request body is valid,
and save data to database.

- GET `/api/get_average/<customer_name>/<from_range>/<to_range>`

Sending data of request to calculating service.
Average of data points in range time (eg. `from=13515551&to=13515553` means
all data including `13515551` and `13515553` epoch).
Respond with new object `id` called `request`, which included status, and
response value.
Value of average for single customer is calculating in separated service. When
it is done then service set `request` object status to `Done` and set
appropriate values in this object.

- GET `/api/request/<requestID>`

`In progress` response:

```
{
    ObjectId: "123456789",
    status: "In progress",
    value: {
        "s": 0.0,
        "a": 0.0
    }
}
```

`Done` response:
```
{
    ObjectId: "123456789",
    status: "Done",
    value: {
        "s": 7,
        "a": 2.33
    }
}
```




# TODO

- Connect to Mongo database in docker-compose running.
- Create short bash script to build, setup and run app.
- After sending /health GET request, app should check
if there is connection with database, and send appropriate response.