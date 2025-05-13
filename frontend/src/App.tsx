import { useHealth } from "./useHealth";
import { IngestForm } from "./components/IngestForm";
import { QueryForm } from "./components/QueryForm";
import { ChatForm } from "./components/ChatForm";
import { FileIngestForm } from "./components/FileIngestForm";
import { AgentForm } from "./components/AgentForm";

export default function App() {
  const health = useHealth();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="p-6 bg-white rounded-2xl shadow-lg">
        <h1 className="text-2xl font-bold mb-4">Project-NYXIS</h1>
        <p>
          Backend Health:{" "}
          <span
            className={
              health === "ok"
                ? "text-green-600"
                : health === "loading"
                ? "text-gray-500"
                : "text-red-600"
            }
          >
            {health}
          </span>
        </p>
      </div>
      <IngestForm />
      <QueryForm />
      <FileIngestForm />
      <QueryForm />
      <FileIngestForm />
      {/* <QueryForm /> */}
      <ChatForm />
      <AgentForm />
    </div>
  );
}
