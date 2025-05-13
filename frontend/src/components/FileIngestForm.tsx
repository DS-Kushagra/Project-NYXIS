import React, { useState } from "react";

export function FileIngestForm() {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<
    "idle" | "loading" | "success" | "error"
  >("idle");
  const [chunks, setChunks] = useState<number | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setStatus("loading");

    const form = new FormData();
    form.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/api/ingest-file", {
        method: "POST",
        body: form,
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Upload failed");
      setChunks(data.chunks);
      setStatus("success");
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow mb-6">
      <h2 className="text-xl font-semibold mb-2">Ingest File (PDF / TXT)</h2>
      <form onSubmit={handleSubmit} className="space-y-3">
        <input
          type="file"
          accept=".pdf,text/plain,.md"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          className="block"
          required
        />
        <button
          type="submit"
          className="px-4 py-2 bg-indigo-600 text-white rounded disabled:opacity-50"
          disabled={status === "loading"}
        >
          {status === "loading" ? "Uploading…" : "Upload & Ingest"}
        </button>
        {status === "success" && (
          <p className="text-green-600">Ingested {chunks} chunks!</p>
        )}
        {status === "error" && (
          <p className="text-red-600">Error ingesting file.</p>
        )}
      </form>
    </div>
  );
}
