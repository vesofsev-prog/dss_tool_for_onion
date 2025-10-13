import React, { useMemo, useState } from "react";

const defaultForm = {
  planting_date: "",
  soil_type: "loam",
  irrigation_mm: 350,
  fertilizer_plan: {
    nitrogen: 1,
    phosphorus: 0.5,
    potassium: 0.5
  }
};

const soilOptions = [
  { label: "Loam", value: "loam" },
  { label: "Sandy", value: "sandy" },
  { label: "Clay", value: "clay" }
];

function SimulationForm({ presets, onSubmit, loading }) {
  const [formState, setFormState] = useState(defaultForm);
  const presetOptions = useMemo(() => presets || [], [presets]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormState((prev) => ({
      ...prev,
      [name]: name === "irrigation_mm" ? Number(value) : value
    }));
  };

  const handleFertilizerChange = (event) => {
    const { name, value } = event.target;
    setFormState((prev) => ({
      ...prev,
      fertilizer_plan: {
        ...prev.fertilizer_plan,
        [name]: Number(value)
      }
    }));
  };

  const handlePreset = (event) => {
    const presetName = event.target.value;
    const selected = presetOptions.find((preset) => preset.name === presetName);
    if (selected) {
      setFormState({
        planting_date: selected.planting_date,
        soil_type: selected.soil_type,
        irrigation_mm: selected.irrigation_mm,
        fertilizer_plan: selected.fertilizer_plan
      });
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formState);
  };

  return (
    <section className="form-section">
      <h2>Simulation Inputs</h2>
      <form onSubmit={handleSubmit} className="form-grid">
        <label>
          Planting date
          <input
            type="date"
            name="planting_date"
            value={formState.planting_date}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Soil type
          <select name="soil_type" value={formState.soil_type} onChange={handleChange}>
            {soilOptions.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        </label>

        <label>
          Irrigation (mm)
          <input
            type="number"
            name="irrigation_mm"
            value={formState.irrigation_mm}
            onChange={handleChange}
            min="0"
          />
        </label>

        <fieldset className="fertilizer">
          <legend>Fertilizer plan (kg/ha)</legend>
          {Object.entries(formState.fertilizer_plan).map(([nutrient, amount]) => (
            <label key={nutrient}>
              {nutrient}
              <input
                type="number"
                name={nutrient}
                value={amount}
                onChange={handleFertilizerChange}
                min="0"
                step="0.1"
              />
            </label>
          ))}
        </fieldset>

        <label>
          Preset scenarios
          <select onChange={handlePreset} defaultValue="">
            <option value="" disabled>
              Choose a preset
            </option>
            {presetOptions.map((preset) => (
              <option key={preset.name} value={preset.name}>
                {preset.name}
              </option>
            ))}
          </select>
        </label>

        <button type="submit" disabled={loading}>
          {loading ? "Running..." : "Run simulation"}
        </button>
      </form>
    </section>
  );
}

export default SimulationForm;
