import React, { useState } from "react";

interface AgentResponse {
  final_output: string;
  steps: { tool: string; input: any; output: any }[];
}

export function AgentForm() {
  const [goal, setGoal] = useState("");
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRun = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    try {
      const res = await fetch("http://localhost:8000/api/agent", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goal }),
      });
      const data: AgentResponse = await res.json();
      setResponse(data);
    } catch {
      setResponse({ final_output: "Error running agent.", steps: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow mb-6">
      <h2 className="text-xl font-semibold mb-2">Agent Playground</h2>
      <form onSubmit={handleRun} className="flex space-x-2 mb-4">
        <input
          className="flex-1 border rounded p-2"
          placeholder="Describe your goal..."
          value={goal}
          onChange={(e) => setGoal(e.target.value)}
          required
        />
        <button
          type="submit"
          className="px-4 py-2 bg-teal-600 text-white rounded disabled:opacity-50"
          disabled={loading}
        >
          {loading ? "Running…" : "Run Agent"}
        </button>
      </form>
      {response && (
        <div>
          <h3 className="font-semibold">Output:</h3>
          <p className="mb-2">{response.final_output}</p>
          {/* In future we’ll render steps here */}
        </div>
      )}
    </div>
  );
}
