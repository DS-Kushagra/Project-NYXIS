import { useEffect, useState } from "react";

export function useHealth() {
  const [status, setStatus] = useState<string>("loading");

  useEffect(() => {
    fetch("/api/health")
      .then((res) => res.json())
      .then(({ status }) => setStatus(status))
      .catch(() => setStatus("error"));
  }, []);

  return status;
}
