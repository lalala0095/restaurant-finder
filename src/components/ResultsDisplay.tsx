import React from 'react';
import type { Restaurant } from '../types';

interface ResultsDisplayProps {
  results: Restaurant[];
  loading: boolean;
  error: string | null;
}

const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, loading, error }) => {
  if (loading) {
    return <p className="text-center text-gray-500 py-4">Loading results...</p>;
  }

  if (error) {
    return <p className="text-center text-red-500 bg-red-100 border border-red-400 p-3 rounded-md">Error: {error}</p>;
  }

  if (results.length === 0) {
    return <p className="text-center text-gray-500 py-4">No restaurants found. Try widening the location of the search!</p>;
  }

  return (
    <div className="space-y-4"> {/* Adds space between child elements (the cards) */}
      <h2 className="text-2xl font-semibold text-gray-700 mb-4">Search Results:</h2>
      {results.map((restaurant) => (
        <div key={restaurant.id || restaurant.name} className="bg-white p-5 border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <h3 className="text-xl font-bold text-blue-600 mb-2">{restaurant.name}</h3>
          {restaurant.address && <p className="text-sm text-gray-600 mb-1"><strong>Address:</strong> {restaurant.address}</p>}
          {restaurant.cuisine && restaurant.cuisine.length > 0 && (
            <p className="text-sm text-gray-600 mb-1"><strong>Cuisine:</strong> {restaurant.cuisine.join(', ')}</p>
          )}
          {restaurant.rating !== undefined && <p className="text-sm text-gray-600 mb-1"><strong>Rating:</strong> {restaurant.rating}</p>}
          {restaurant.price_level !== undefined && (
            <p className="text-sm text-gray-600 mb-1">
              <strong>Price Level:</strong> {restaurant.price_level}
            </p>
          )}
          {restaurant.operating_hours && <p className="text-sm text-gray-600"><strong>Hours:</strong> {restaurant.operating_hours}</p>}
        </div>
      ))}
    </div>
  );
};

export default ResultsDisplay;