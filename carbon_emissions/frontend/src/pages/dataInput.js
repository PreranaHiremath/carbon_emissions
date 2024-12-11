import React, {useState} from "react";
import axios from 'axios';

function CoalData() {
    

    const [formData, setData] = useState({
        name : '',
        location : '',
        mine_type : '',
        coal_production_tonnes : '',
        methane_emission_factor: '',
    });

    const handleChange = (e) => {
        setData ({
            ...formData,
            [e.target.name] : e.target.value,        
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {

            const ProcessedData = {
                ...formData,
                coal_production_tonnes: parseFloat(formData.coal_production_tonnes),
                methane_emission_factor: parseFloat(formData.methane_emission_factor)
            }

            const response = await axios.post(`http://localhost:8000/api/CoalMine/`, 
                ProcessedData,
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            );
            alert('Great! lets move on to the next phase');
            console.log(response.data);
        }catch (error) {
            alert('There was a problem in submitting data, please try again.');
            console.error(error.response ? error.response.data : error.message);
        }

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
          <h2>Enter Coal Mine Details</h2>
        </div>

        <div className="card-body p-4">
          <form onSubmit={handleSubmit}>
            <div className="form-floating mb-3">
              <input
                type="text"
                className="form-control"
                id="coalMineName"
                name="name"
                placeholder="Mine Name"
                value={formData.name}
                onChange={handleChange}
                required
              />
              <label htmlFor="coalMineName">Mine Name</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="text"
                className="form-control"
                id="location"
                name="location"
                placeholder="Location"
                value={formData.location}
                onChange={handleChange}
                required
              />
              <label htmlFor="location">Location</label>
            </div>

            <div className="form-floating mb-3">
              <select
                className="form-select"
                id="mine_type"
                name="mine_type"
                value={formData.mine_type}
                onChange={handleChange}
                required
              >
                <option value="">Select Mine Type</option>
                <option value="open_pit">Open Pit</option>
                <option value="underground">Underground</option>
              </select>
              <label htmlFor="mine_type">Mine Type</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="number"
                className="form-control"
                id="coalProductionTonnes"
                name="coal_production_tonnes"
                placeholder="Coal Production (Tonnes)"
                value={formData.coal_production_tonnes}
                onChange={handleChange}
                required
              />
              <label htmlFor="coalProductionTonnes">Coal Production (Tonnes)</label>
            </div>

            <div className="form-floating mb-3">
              <input
                type="number"
                className="form-control"
                id="methaneEmissionFactor"
                name="methane_emission_factor"
                placeholder="Methane Emission Factor"
                value={formData.methane_emission_factor}
                onChange={handleChange}
                required
              />
              <label htmlFor="methaneEmissionFactor">Methane Emission Factor</label>
            </div>

            <button type="submit" className="btn btn-success w-100 fw-bold">
              Submit
            </button>
          </form>
        </div>
      </div>
    </div>
    )


}

export default CoalData;