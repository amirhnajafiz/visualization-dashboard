import { useEffect, useState } from 'react';
import BarChart from '../components/BarChart.jsx';
import "./Home.css";

function Home() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('/api/data?page=1&columns=genre')
      .then(res => res.json())
      .then(json => {
        setData(json["records"]);
      });
  }, []);

  return (
    <div className="grid-container">
      <div className="section section-1">
        <BarChart data={data} />
      </div>
      <div className="section section-2">Section 2</div>
      <div className="section section-3">Section 3</div>
      <div className="section section-4">Section 4</div>
      <div className="section section-5">Section 5</div>
      <div className="section section-6">Section 6</div>
    </div>
  );
}

export default Home;
