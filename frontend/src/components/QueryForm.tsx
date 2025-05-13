import React, { useState } from "react";

interface Result {
  text: string;
  metadata: Record<string, any>;
}

export function QueryForm() {
  const [q, setQ] = useState("");
  const [k, setK] = useState(4);
  const [results, setResults] = useState<Result[] | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(
        `http://localhost:8000/api/query?q=${encodeURIComponent(q)}&k=${k}`
      );
      
      const data: Result[] = await res.json();
      setResults(data);
    } catch {
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-2">Semantic Search</h2>
      <form onSubmit={handleSearch} className="flex flex-col space-y-3 mb-4">
        <input
          className="border rounded p-2"
          type="text"
          placeholder="Enter your query"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          required
        />
        <div className="flex items-center space-x-2">
          <label>k:</label>
          <input
            className="border rounded p-1 w-16"
            type="number"
            min={1}
            max={20}
            value={k}
            onChange={(e) => setK(Number(e.target.value))}
          />
        </div>
        <button
          type="submit"
          className="px-4 py-2 bg-green-600 text-white rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Searching…" : "Search"}
        </button>
      </form>

      {results && (
        <div>
          {results.length === 0 && (
            <p className="text-gray-600">No results found.</p>
          )}
          {results.map((r, i) => (
            <div key={i} className="mb-3 p-3 border rounded">
              <p className="italic mb-1">{JSON.stringify(r.metadata)}</p>
              <p>{r.text}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
