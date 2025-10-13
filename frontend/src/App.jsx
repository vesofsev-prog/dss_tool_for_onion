import React, { useEffect, useState } from "react";
import SimulationForm from "./components/SimulationForm.jsx";
import { fetchPresets, runSimulation } from "./services/api.js";

const initialResult = {
  expected_yield_t_ha: null,
  maturity_date: null,
  notes_summary: "Submit a scenario to view results.",
  notes: []
};

function App() {
  const [presets, setPresets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(initialResult);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchPresets()
      .then((data) => setPresets(data.presets || []))
      .catch(() => setPresets([]));
  }, []);

  const handleSubmit = async (payload) => {
    setLoading(true);
    setError(null);
    try {
      const response = await runSimulation(payload);
      setResult(response);
    } catch (err) {
      setError(err.message || "Unable to run simulation");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <header>
        <h1>Onion Decision Support System</h1>
        <p>Prototype interface for exploring planting scenarios.</p>
      </header>
      <main>
        <SimulationForm presets={presets} onSubmit={handleSubmit} loading={loading} />
        <section className="results">
          <h2>Simulation Result</h2>
          {error && <p className="error">{error}</p>}
          {result.expected_yield_t_ha ? (
            <ul>
              <li>
                <strong>Expected yield:</strong> {result.expected_yield_t_ha} t/ha
              </li>
              <li>
                <strong>Maturity date:</strong> {result.maturity_date}
              </li>
              <li>
                <strong>Notes:</strong>
                <pre>{result.notes_summary}</pre>
              </li>
            </ul>
          ) : (
            <p>{result.notes_summary}</p>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
