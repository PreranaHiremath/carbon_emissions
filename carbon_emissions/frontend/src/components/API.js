import axios from 'axios';


//getting emissions and creating emission record
export const getEmissions = async () => {
    const response = await axios.get("http://localhost:8000/api/emissions/");
    return response.data;
};

export const CreateEmissionRecord = async (EmissionsData) => {
    const response = await axios.post("http://localhost:8000/api/emissions/", EmissionsData);
    return response.data;
};

// getting carbonSink and creating CarbonSink record
export const getCarbonSink = async () => {
    const response = await axios.get("http://localhost:8000/api/carbonSink/");
    return response.data;
};

export const createCarbonSinkRecord = async (sinkData) => {
    const response = await axios.post("http://localhost:8000/api/carbonSink/", sinkData);
    return response.data;
};

//Perform gap analysis.
export const performGapAnalysis = async () => {
    const response = await axios.post("http://localhost:8000/api/gapAnalysis/")
    return response.data;
};

//Dahsboard API
export const DashboardData = async () => {
    const response = await axios.get("http://localhost:8000/api/dashboard/")
    return response.data;
}