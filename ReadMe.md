# FastAPI Server for Restaurant Finder
## Overview
This is a simple FastAPI server that provides an endpoint to let the user find relevant Restaurants based on their user query.

## Setup to run the server
This is setup to run in an AWS EC2 virtual machine. The server can be cloned from a Github repository. Execute the following steps in an EC2 instance:

1. This clones the Github repository.
```bash
git clone -b backend https://github.com/lalala0095/restaurant-finder
```

2. Go to the created directory.
```bash
cd restaurant-finder
```

3. Create and activate a Python virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate
```

4. Install the dependencies
```bash
pip install -r requirements.txt
```

5. You need to create an `.env` file for the environment variables.
```bash
sudo nano .env
```

Write the following to the `.env` file:
```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
FOURSQUARE_API_KEY="YOUR_FOURSQUARE_API_KEY"
```

Make sure to replace the placeholder values with your actual configuration.

6. Run the uvicorn server.
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

7. To keep the server running, you can use `nohup` to run the server in the background and log the output to a file. Additionally, you can save the process ID (PID) to a file for easier management.

```bash
nohup uvicorn main:app --host 0.0.0.0 --port 8000 > fastapi.log 2>&1 & echo $! > fastapi.pid
```

- `fastapi.log` will contain the server's output logs.
- `fastapi.pid` will store the PID of the running process, which can be used to stop the server later.

8. In order for this backend server to communicate with the frontend, you need to setup cloudflared tunnel. This will auto-generate an https URL for the FastAPI server.
Follow this documentations for setting up cloudflared tunnels:
`https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/`

9. Run cloudflared tunnel with nohup.
```bash
nohup cloudflared tunnel --url http://localhost:8002 > cloudflared.log 2>&1 & echo $! > cloudflared.pid
```

10. This will generate a log named `cloudflared.log`. View the log and get the auto-generated URL.:
```bash
cat cloudflared.log
```
This URL will be the main API base URL for the frontend.


## Notes on how to deploy to production.
In main.py file, you can add the frontend's URL so that the FastAPI server will accept the requests coming from the frontend.
Add it in this part:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*']
)
```