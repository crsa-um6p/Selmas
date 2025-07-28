/* eslint-disable react-hooks/exhaustive-deps */
import React, { useState, useEffect, useRef } from "react";
import MapTab from "./MapTab";
import GraphTab from "./GraphTab";






// import Map from "./Map"


const Visualization = () => {


  const [tab, setTab] = useState("map");

  const [layers, setLayers] = useState([])
  const [variables, setVariables] = useState([])


  return (
    <div className="">
      
      {tab === 'map' ? 
        <MapTab 
          setTab={setTab}
          layers={layers}
          setLayers={setLayers}
        />
      :
        <GraphTab
          setTab={setTab}
          variables={variables}
          setVariables={setVariables}
          layers={layers}
        />
      }
      
    </div>
  );
};

export default Visualization;
