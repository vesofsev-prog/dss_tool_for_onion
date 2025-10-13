const headers = {
  "Content-Type": "application/json"
};

export async function fetchPresets() {
  const response = await fetch("/api/simulations/presets");
  if (!response.ok) {
    throw new Error("Unable to fetch presets");
  }
  return response.json();
}

export async function runSimulation(payload) {
  const response = await fetch("/api/simulations/run", {
    method: "POST",
    headers,
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Simulation failed");
  }

  return response.json();
}
