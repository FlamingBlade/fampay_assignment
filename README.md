
# Backend Assignment | FamPay


A brief description of what this project does and who it's for


## Project Description

API to fetch latest videos sorted in reverse chronological order of their publishing date-time from YouTube for a given tag/search query in a paginated response.


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`


## Deployment

Clone the project

```bash
  git clone https://github.com/FlamingBlade/fampay_assignment.git
```
Navigate to fampay_assignment/fampay_assignment/settings.py
You will need Youtube API keys to run this, you can get them 
 [here](https://developers.google.com/youtube/v3/getting-started)

Once you have it add it to 

`YOUTUBE_API_KEYS`
in fampay_assignment/fampay_assignment/settings.py

Multiple keys are supported, so you can add a list here.

Build the docker image 
```bash
  docker build -t fampay .
```
Run it
```bash
  docker run -p 8080:8080 fampay
```
Navigate to `http://localhost:8080` to access the apis



## API Reference

#### Start fetching youtube videos based on search parameter

```http
  GET /video/start
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. Your search parameter |

#### Stop fetching youtube videos based on search parameter

```http
  GET /video/stop
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. Your search parameter |

#### Get fetched videos based on search parameter

```http
  GET /video/fetch
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `q`      | `string` | **Required**.Your search parameter |
| `page`      | `string` |  page number |

#### Search videos based on title or description

```http
  GET /video/search
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `q` | `string` | **Required**. Your keyword parameters |

Fuzzy search occurs based on the input here against title and description
Accuracy can be tweaked with by changing `FUZZY_SEARCH_FACTOR` in settings



## A few examples for the API's

```javascript
curl --location 'http://127.0.0.1:8080/video/start?q=cars+benz'
curl --location 'http://127.0.0.1:8080/video/stop?q=cars+benz'
curl --location 'http://127.0.0.1:8080/video/fetch?page=1&q=car+benz'
curl --location 'http://localhost:8080/video/search?q=cars+benz'


```

