# Restaurant Finder Coding Challenge

## This frontend is made for a FastAPI server of a Restaurant Finder Coding Challenge.

## **Task Overview**

Build an **LLM-Driven Restaurant Finder App** that allows users to enter a free‑form message describing what they want to do. The system should then:

1. Convert the natural language message into a structured JSON command using an LLM (your choice—OpenAI is an option).
2. Use the JSON command to call the [Foursquare Places API](https://docs.foursquare.com/developer/reference/place-search) for restaurant data.
3. Display the search results with multiple fields (e.g., name, address, rating, price level, operating hours).

## Deployment setup
This is setup to be deployed to Vercel. Follow the following steps to deploy:

1. This clones the Github repository.
```bash
git clone -b frontend https://github.com/lalala0095/restaurant-finder
```

2. Go to the created directory.
```bash
cd restaurant-finder
```

3. Install dependencies.
```bash
npm install
```

4. Setup the project in Vercel if running for the first time. Follow the instructions after.
```bash
vercel
```

5. If redeploying after some updates, run the following for production re-deployment.
```bash
vercel --prod
```
