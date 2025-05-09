import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ResultsDisplay from './components/ResultsDisplay';
import type { Restaurant, ApiRequest, ApiResponse } from './types';

const App: React.FC = () => {
  const [results, setResults] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (message: string) => {
    setLoading(true);
    setError(null);
    setResults([]);

    const requestBody: ApiRequest = { message };

    try {
      const response = await fetch('https://belly-compare-committed-pressed.trycloudflare.com/api/execute', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        let errorMessage = `HTTP error! status: ${response.status}`;
        try {
            const errorData = await response.json();
            errorMessage = errorData.error || errorData.message || errorMessage;
        } catch (e) {
            // Could not parse JSON error, stick with status
        }
        throw new Error(errorMessage);
      }

      const data: ApiResponse = await response.json();
      setResults(data.restaurants || []);

    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred.');
      }
      console.error('Search failed:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4 md:p-6 max-w-2xl">
      <header className="text-center my-6 md:my-8">
        <h1 className="text-3xl md:text-4xl font-bold text-blue-700">
          Restaurant Finder
        </h1>
      </header>
      <main>
        <SearchBar onSearch={handleSearch} loading={loading} />
        <ResultsDisplay results={results} loading={loading} error={error} />
      </main>
    </div>
  );
};

export default App;