## Data to be stored
```
{
    employeeId: string,
    name: string,
    city: string
}
```
---
## API
***

>##### GET /greeting
###### Response
* Code: 200  
* Content: `Hello world!` 
---

>##### POST /employee
###### Request & Response headers
Content-Type: application/json
###### Body
```
{
    "name": "Big(O)",
    "city": "Mumbai"
}
```
###### Success Response
* Status code: 201
* Content: 
```
{
  "employeeId": 1,
  "name": "Big(O)",
  "city": "Mumbai"
}
```
---

>##### GET /employee/1
###### URL Params
###### Success Response
* Status code: 200
* Content: 
```
{
  "employeeId": 1,
  "name": "Big(O)",
  "city": "Mumbai"
}
```
>##### GET /employee/3
###### Error Response
* Status code: 404
* Content: 
```
{ message : "Employee with 3 was not found" }
```
---

>##### GET /employees/all
###### Success Response
* Status code: 200
* Content: 
```
[
  {
    "employeeId": 1,
    "name": "Big(O)",
    "city": "Mumbai"
  }
]
```
---

>##### PUT /employee/1
###### Headers
Content-Type: application/json
###### Body
```
{
    "name": NaN(O),
    "city": "Pune"
}
```

###### Success Response
* Code: 201
* Content: 
```
{
  "employeeId": 1,
  "name": "NaN(O),
  "city": "Pune"
}
```
>##### PUT /employee/2
###### Body
```
{
    "name": NaN(O),
    "city": "Pune"
}
```
###### Error Response
* Code: 404
* Content: `{ message : "Employee with 2 was not found" }`
---

>##### DELETE /employee/1
###### Success Response
* Status code: 200
* Content:
```
{
  "employeeId": 1,
  "name": "NaN(O),
  "city": "Pune"
}
```
>##### DELETE /employee/2
###### Error Response
* Status code: 404
* Content: `{ message : "Employee with 2 was not found" }`

----


