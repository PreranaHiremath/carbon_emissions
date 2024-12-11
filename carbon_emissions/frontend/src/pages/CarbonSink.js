import React, {useState, useEffect} from "react";
import { getCarbonSink, createCarbonSinkRecord } from "../components/API";

const CarbonSink = () => {
    const [sinks, setSinks] = useState([]);
    const [newSink, setNewSink] = useState({
        mine_location: '',
        forest_area_hectares: ''
    });

    useEffect(()=>{
        getCarbonSink().then(data => createCarbonSinkRecord(data));
    }, []);

    const handleChange = (e) => {
        setNewSink({
            ...newSink,
            [e.traget.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault()
        await createCarbonSinkRecord(newSink);
        getCarbonSink().then(data => setNewSink(data));
    };

    return (
    <div
      className="d-flex flex-column justify-content-center align-items-center vh-100"
      style={{
        background: "linear-gradient(135deg, #f0fdf4, #d9f7be)"
      }}
    >
      {/* Project Name */}
      <h1 className="text-success text-center display-3 mb-4">
        QuantC
      </h1>

      {/* Responsive Card Container */}
      <div className="card shadow w-50">
        <div className="card-header bg-white text-success text-center" style={{ borderRadius: "15px 15px 0 0"}}>
          <h2>Carbon Sink Estimation</h2>
        </div>

        <div className="card-body p-4">
          <form onSubmit={handleSubmit}>
            <div className="form-floating mb-3">
              <input
                type="number"
                className="form-control"
                id="areaHectares"
                name="forest_area_hectares"
                placeholder="forest area in hectares"
                onChange={handleChange}
                required
              />
              <label htmlFor="areaHectares">Forest area</label>
            </div>

            <div className="form-floating mb-3">
              <select
                className="form-select"
                id="mine_location"
                name="mine_location"
                onChange={handleChange}
                required
              >
                <option value="">Select Mine Type</option>
                <option value="jharkhand">Jharkhand</option>
                <option value="rajasthan">Rajasthan</option>
                <option value="assam">Assam</option>
                <option value="other">Other</option>
              </select>
              <label htmlFor="mine_type">Mine Location</label>
            </div>

            <button type="submit" className="btn btn-success w-100 fw-bold">
              Calculate Carbon Sink
            </button>
          </form>
        </div>
        <div className="card-body p-4">
            <ul className="list-group">
                {sinks.map((sink) => (
                    <li className="list-group-item" key={sink.id}>
                        <strong>Area:</strong>{sink.forest_area_hectares} ha | <strong>Offset:</strong> {sink.afforestation_offset} kg CO2e
                    </li>
                ))}
            </ul>
        </div>
        </div>
    </div>
    );
};

export default CarbonSink;