import logo from './logo.svg';
import './App.css';
import { useState } from 'react';

function App() {
  const [data, setData] = useState('');
  const [variable, setVariable] = useState('');
  const [filter, setFilter] = useState('');
  const [min_value, setMin_value] = useState('');
  const [max_value, setMax_value] = useState('');
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(variable, filter, min_value, max_value);
    fetch('http://localhost:8000/visualisation/get_data/', {
      method: 'POST',
      body: JSON.stringify({ variable, filter, min_value, max_value }),
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then((response) => response.json())
      .then((data) => setData(data));
  };

  const handleVariableChange = (e) => {
    setVariable(e.target.value);
  };

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
  };

  const handleMinValueChange = (e) => {
    setMin_value(e.target.value);
  };

  const handleMaxValueChange = (e) => {
    setMax_value(e.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Visualisation des données</h1>
        <form>
          <label>Variable</label>
          <select onChange={handleVariableChange}>
            <option value="soiltexture">Texture du sol</option>
            <option value="soilquality">Qualité du sol</option>
            <option value="soilsample">Échantillon de sol</option>
          </select>
          <label>Filtre</label>
          <select onChange={handleFilterChange}>
            <option value="Argile">Argile</option>
            <option value="Lemon">Lemon</option>
            <option value="Sable">Sable</option>
          </select>
          <label>Valeur minimale</label>
          <input type="number" onChange={handleMinValueChange} />
          <label>Valeur maximale</label>
          <input type="number" onChange={handleMaxValueChange} />
          <button type="submit" onClick={handleSubmit}>Afficher</button>
        </form>
        <div id="data-container">
          <textarea id="data-display">{JSON.stringify(data)}</textarea>
        </div>
      </header>
    </div>
  );
}

export default App;
