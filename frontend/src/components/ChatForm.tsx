import { useState, useRef } from "react";

interface Message {
  sender: "user" | "bot";
  text: string;
}

export function ChatForm() {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  const sendMessage = async () => {
    if (!message.trim()) return;
    const userMsg = { sender: "user" as const, text: message };
    setChat((c) => [...c, userMsg]);
    setMessage("");
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, k: 4 }),
      });
      const data = await res.json();
      setChat((c) => [...c, { sender: "bot", text: data.reply }]);
    } catch {
      setChat((c) => [
        ...c,
        { sender: "bot", text: "Error generating response." },
      ]);
    } finally {
      setLoading(false);
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-2">Chat with NYXIS</h2>
      <div className="h-64 overflow-y-auto mb-3 space-y-2 p-2 border rounded">
        {chat.map((m, i) => (
          <div
            key={i}
            className={`flex ${
              m.sender === "bot" ? "justify-start" : "justify-end"
            }`}
          >
            <span
              className={`px-3 py-1 rounded-lg ${
                m.sender === "bot" ? "bg-gray-200" : "bg-blue-500 text-white"
              }`}
            >
              {m.text}
            </span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <div className="flex space-x-2">
        <input
          className="flex-1 border rounded p-2"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Type your question..."
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && sendMessage()}
        />
        <button
          className="px-4 py-2 bg-purple-600 text-white rounded disabled:opacity-50"
          onClick={sendMessage}
          disabled={loading}
        >
          {loading ? "…" : "Send"}
        </button>
      </div>
    </div>
  );
}
