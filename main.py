from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from config import gemini_client, foursquare_api_key
import json
import re
import requests
from models import MessageRequest

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'https://restaurant-finder-sage.vercel.app'],
    allow_methods=['*'],
    allow_headers=['*']
)

chat_router = APIRouter(tags=["Chat"])

@chat_router.post("/api/execute")
async def execute(request: MessageRequest):
    """
    This endpoint executes the query of the user, sends the appropriate prompt to Gemini API ->
    Returns the JSON response of the structured input ->
    Sends request to Foursquare Places API to return the restaurants data ->
    Displays the search results with multiple fields (e.g., name, address, rating, price level, operating hours).
    """
    message = request.message
    print(message)
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"""
        The following is a user query for a restaurant finder:
        {message}
        *Your Task:*
        Return me a JSON object that I can reuse for a Restaurant finder API with the following sample format.
        Just return the following schema, no other comments or extra texts.
        If a field is not included in the user's query, do not include it in the JSON response.
        I included some comments in the sample JSON, do not include them in the response.
        Make the values URL-like strings, for ex. replace commas with %2C and spaces with %20.
        The tricky parameter here is the "near" field. A string naming a locality in the world (e.g., "Chicago, IL"). If the value is not geocodable, it will return an error in the Restaurant finder API, take note of this. Determine the exact locality of the user query, try using the City, Province/State convention.
        ```json
        {{
        "action": "restaurant_search",
        "parameters": {{
            "query": "sushi", # A string to be matched against all content for this place, including but not limited to venue name, category, telephone number, taste, and tips.
            "ll": "41.8781,-87.6298", # this is optional, this is the longitude/latitude of the location of the user if given
            "radius": 22000, # this is in meters, on how wide the search will be, and is optional
            "min_price": 1, # 1 (most affordable) to 4 (most expensive) - do not misinterpret this to the currency, estimate how cheap the user is finding for a product
            "max_price": 4, # 1 (most affordable) to 4 (most expensive) - do not misinterpret this to the currency, estimate how cheap the user is finding for a product
            "open_at": "1T2130", # To be specified as DOWTHHMM (e.g., 1T2130), where DOW is the day number 1-7 (Monday = 1, Sunday = 7) and time is in 24 hour format.
            "open_now": "false", # do not return this if there is an open_at in the user query. Set this to default as 'false'
            "near": "downtown Los Angeles",
            "sort": "RELEVANCE" # RATING, RELEVANCE, DISTANCE and POPULARITY are the only options here
            }}
        }}
        ```
        """
    )

    gemini_response = response.text
    print(gemini_response)
    gemini_response = gemini_response.replace(r"```json", "").replace(r"```", "")
    print("now converting the response to json")

    fsq_json_input = json.loads(gemini_response)
    query = fsq_json_input['parameters'].get('query', None)
    ll = fsq_json_input['parameters'].get('ll', None)
    radius = fsq_json_input['parameters'].get('radius', None)
    min_price = fsq_json_input['parameters'].get('min_price', None)
    max_price = fsq_json_input['parameters'].get('max_price', None)
    open_at = fsq_json_input['parameters'].get('open_at', None)
    open_now = fsq_json_input['parameters'].get('open_now', 'false')
    near = fsq_json_input['parameters'].get('near', None)
    sort = fsq_json_input['parameters'].get('sort', None)

    url1 = "https://api.foursquare.com/v3/places/search?query="
    url2 = "&ll="
    url3 = "&radius="
    url4 = "&min_price="
    url5 = "&max_price="
    url6 = "&open_at="
    url7 = "&open_now="
    url8 = "&near="
    url9 = "&sort="
    url10 = "&fields=name%2Clocation%2Ccategories%2Cprice%2Chours%2Crating%2Cfeatures"
    url11 = "&categories=4bf58dd8d48988d120951735,56aa371be4b08b9a8d57350b,4bf58dd8d48988d1cb941735,4d4b7105d754a06374d81259,4bf58dd8d48988d16e941735,5665c7b9498e7d8a4f2c0f06,63be6904847c3692a84b9bb6,4bf58dd8d48988d1e0931735,52e81612bcbc57f1066b7a00,4bf58dd8d48988d16e941735,4bf58dd8d48988d1ce941735,4bf58dd8d48988d14f941735,53e0feef498e5aac066fd8a9,4bf58dd8d48988d1ef931735".replace(",", "%2C")

    params_list = [
        (query, url1),
        (ll, url2), 
        (radius, url3), 
        (min_price, url4), 
        (max_price, url5),
        (open_at, url6), 
        (open_now, url7), 
        (near, url8), 
        (sort, url9)
    ]
    params_new_list = []
    params_counter = 0
    for p, url in params_list:
        params_counter += 1
        if p:
            if params_counter == 2:
                params_new_list.append(url2)
            params_new_list.append(url)
            params_new_list.append(str(p))
    params_new_list.append(url10)
    params_new_list.append(url11)
    final_url = "".join(params_new_list)
    print(final_url)
    print("now requesting the fsq_json_input to Four Square restaurant API.")
    headers = {
        "accept": "application/json",
        "Authorization": foursquare_api_key
    }

    response = requests.get(final_url, headers=headers)
    results = json.loads(response.text).get('results', {})
    if results:
        new_restaurants = []
        for r in results:
            categories = r.get('categories', [])
            features = r.get('features', {})

            new_cuisines = set()
            for c in categories:
                category_short_name = c.get('short_name', None) 
                if category_short_name:
                    new_cuisines.add(category_short_name)
            meals = features.get('food_and_drink', {}).get("meals", {})
            for meal_name, meal_data in meals.items():
                print(meal_name, meal_data)
                try:
                    for value in meal_data:
                        if value:
                            new_cuisines.add(value)
                except TypeError:
                    if meal_data == True:
                        new_cuisines.add(f"{meal_name}: Yes")
            new_cuisines = list(new_cuisines)
            rating = r.get('rating', "Not found.")
            
            returned_price = r.get('price', 0)
            if returned_price == 0:
                price_level = "Not found."
                print(r)
            elif returned_price == 1:
                price_level = "Very Affordable."
            elif returned_price == 2:
                price_level = "Affordable."
            elif returned_price == 3:
                price_level = "Expensive."
            elif returned_price == 4:
                price_level = "Very Expensive."

            operating_hours = r.get('hours', {}).get('display', 'No display hours found.')

            new_restaurants.append({
                "name": r.get('name', 'No name found.'),
                "address": r.get('location', {}).get('formatted_address', 'No address found.'),
                "cuisine": new_cuisines,
                "rating": rating,
                "price_level": price_level,
                "operating_hours": operating_hours
            })
        return {"message": "success", "restaurants": new_restaurants}
        
    else:
        print("no result in the initial request, setting the least parameters now")
        params_list = [(query, url1), (near, url8)]
        params_new_list = []
        for p, url in params_list:
            if p:
                params_new_list.append(url)
                params_new_list.append(str(p))
        params_new_list.append(url10)
        params_new_list.append(url11)
        final_url = "".join(params_new_list)
        print(final_url)
        print("now requesting the fsq_json_input to Four Square restaurant API.")
        headers = {
            "accept": "application/json",
            "Authorization": foursquare_api_key
        }

        response = requests.get(final_url, headers=headers)
        results = json.loads(response.text).get('results', {})
        if results:
            new_restaurants = []
            for r in results:
                categories = r.get('categories', [])
                features = r.get('features', {})

                new_cuisines = set()
                for c in categories:
                    category_short_name = c.get('short_name', None) 
                    if category_short_name:
                        new_cuisines.add(category_short_name)
                meals = features.get('food_and_drink', {}).get("meals", {})
                for meal_name, meal_data in meals.items():
                    print(meal_name, meal_data)
                    try:
                        for value in meal_data:
                            if value:
                                new_cuisines.add(value)
                    except TypeError:
                        if meal_data == True:
                            new_cuisines.add(f"{meal_name}: Yes")
                new_cuisines = list(new_cuisines)
                rating = r.get('rating', "Not found.")

                returned_price = r.get('price', 0)
                if returned_price == 0:
                    price_level = "Not found."
                elif returned_price == 1:
                    price_level = "Very Affordable."
                elif returned_price == 2:
                    price_level = "Affordable."
                elif returned_price == 3:
                    price_level = "Expensive."
                elif returned_price == 4:
                    price_level = "Very Expensive."

                operating_hours = r.get('hours', {}).get('display', 'No display hours found.')

                new_restaurants.append({
                    "name": r.get('name', 'No name found.'),
                    "address": r.get('location', {}).get('formatted_address', 'No address found.'),
                    "cuisine": new_cuisines,
                    "rating": rating,
                    "price_level": price_level,
                    "operating_hours": operating_hours
                })
            return {"message": "success", "restaurants": new_restaurants}
        else:
            return {"message": "No results found", "restaurants": {}}

app.include_router(chat_router)

@app.get("/")
async def root():
    return {"message": "This FastAPI server is for backend of a Restaurant Finder App."}

