import React, { useState } from "react";

export function IngestForm() {
  const [text, setText] = useState("");
  const [meta, setMeta] = useState<string>("{}");
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");
    let metadata;
    try {
      metadata = JSON.parse(meta);
    } catch {
      setStatus("error");
      return;
    }
    try {
      const res = await fetch("http://localhost:8000/api/ingest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text, metadata }),
      });
      if (!res.ok) throw new Error();
      setStatus("success");
      setText("");
      setMeta("{}");
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow mb-6">
      <h2 className="text-xl font-semibold mb-2">Ingest Text</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <textarea
          className="w-full border rounded p-2"
          rows={4}
          placeholder="Enter text to ingest"
          value={text}
          onChange={(e) => setText(e.target.value)}
          required
        />
        <input
          className="w-full border rounded p-2"
          type="text"
          placeholder='Metadata JSON (e.g. {"source":"note"})'
          value={meta}
          onChange={(e) => setMeta(e.target.value)}
        />
        <button
          type="submit"
          className="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50"
          disabled={status === "loading"}
        >
          {status === "loading" ? "Ingesting…" : "Ingest"}
        </button>
        {status === "success" && (
          <p className="text-green-600">Ingested successfully!</p>
        )}
        {status === "error" && (
          <p className="text-red-600">Error. Check input or server.</p>
        )}
      </form>
    </div>
  );
}
