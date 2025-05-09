export interface Restaurant {
    id: string;
    name: string;
    address?: string;
    cuisine?: string[];
    rating?: string;
    price_level?: string;
    operating_hours?: string;
  }
  
  export interface ApiRequest {
    message: string;
  }
  
  export interface ApiResponse {
    restaurants: Restaurant[];
  }