import React, {useState} from "react";
import { performGapAnalysis } from "../components/API";

const GapAnalysis = () => {
    const [gapResult, setGapResult] = useState(null);

    const handlePerformAnalysis = async () => {
        const result = await performGapAnalysis();
        setGapResult(result);
    };

    return (
        <div>
            <h1>Gap Analysis</h1>
            <button onClick={handlePerformAnalysis}>Perform Gap Analysis</button>

            {gapResult && (
                <div>
                    <h2>Gap Analysis Result</h2>
                    <p><strong>Gap:</strong> {gapResult.gap_value} kg CO2e</p>
                    <p><strong>Recommendations:</strong> {gapResult.recommendations}</p>

                    <h2>Shortfall Areas</h2>
                    {gapResult.shortfall_areas.length > 0 ? (
                        <ul>
                            {gapResult.shortfall_areas.map((area, index) => (
                                <li key={index}>
                                    <p><strong>Area:</strong> {area.area}</p>
                                    <p><strong>Issue:</strong> {area.issue}</p>
                                    <p><strong>Suggestion:</strong> {area.suggestion}</p>
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p>No shortfalls detected.</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default GapAnalysis;