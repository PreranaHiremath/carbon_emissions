
import './App.css';
import CoalData from './pages/dataInput';
import Emissions from './pages/Emissions';
import CarbonSink from './pages/CarbonSink';
import GapAnalysis from './pages/GapAnalysis';
import Dashboard from './pages/Dashboard';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
        {/* Default route (Home page) */}
        <Route path="/" element={<CoalData />} />

        <Route path = "/Emissions" element={<Emissions />}/>

        <Route path = "/CarbonSink" element={<CarbonSink />} />

        <Route path = "/GapAnalysis" element={<GapAnalysis />} />

        <Route path = "/Dashboard" element={<Dashboard />} />

      </Routes>
    </Router>
  );
}

export default App;
