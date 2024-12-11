import React, {useState, useEffect} from "react";
import { DashboardData } from "../components/API";
import Chart from "chart.js/auto";
import {Line, Bar, Pie} from 'react-chartjs-2';

const Dashboard = () => {
    const [dashboardData, setDashboardData] = useState(null);

    useEffect(() => {
        DashboardData().then((data) => setDashboardData(data));
    }, []);

    if (!dashboardData) return <p>Loading...</p>;

    const emissionData = dashboardData.emissions_breakdown || {};

    const emissionsBreakdownData = {
        labels: ['Excavation', 'Transportation', 'Fuel Usage', 'Electricity'],
        datasets: [
            {
                label: 'emissions (kg CO2e)',
                data: [
                    emissionData.excavation_tonnes || 0,
                    emissionData.transportation_cost || 0,
                    emissionData.fuel_usage_liters || 0,
                    emissionData.electricity_usage_kwh || 0,
                ],
                backgroundColor: ["#4e73df", "#1cc88a", "#36b9cc", "#f6c23e"],
            },
        ],
    };

    const carbonSinkVersusEmissionData = {
        labels: ["Carbon Sink", "Emissions Gap"],
        datasets: [
            {
                label: "Comparison (kg CO2e)",
                data: [
                    dashboardData.carbon_sink_capacity || 0,
                    dashboardData.gap_value || 0,
                ],
                backgroundColor: ["#2ecc71", "#e74c3c"],
            },
        ],
    };

    const printReport = () => {
        window.print();
    };

    return (
        <div>
            <h1>Live Dashboard</h1>

            <div>
                <h2>Emission Breakdown</h2>
                <Bar data={emissionsBreakdownData} />
            </div>

            <div>
                <h2>Effectiveness of Strategies</h2>
                <p>Coming soon...</p>
            </div>

            <div>
                <h2>Carbon Sinks vs Emissions Gap</h2>
                <Pie data={carbonSinkVersusEmissionData} />
            </div>

            <button onClick={printReport}>Print Summary Report</button>
        </div>
    );
};

export default Dashboard;
