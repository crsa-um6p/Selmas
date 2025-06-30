import React from "react";

const DashboardStates = (props) => {

  const samples = props.aggregated_data;

  console.log("aggregated_data",samples);

  return (
    <>
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-6 w-full">
    

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Classification
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {Object.entries(samples.classification_percentages).map(([key, value], index) => (
          <div key={index}>
            {key} : {value.percentage}%
            <br />
          </div>
        ))
        }
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Ex-change Sodium Potential
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
      <div>Surface : {samples.sar_stats_surface.mean_sar.toFixed(4)}</div>
        <div>Profondeur : {samples.sar_stats_profondeur.mean_sar.toFixed(4)}</div>
        
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Sodium absorption ratio
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
      <div>Surface : {samples.esp_stats_surface.mean_esp.toFixed(4)}</div>
        <div>Profondeur : {samples.esp_stats_profondeur.mean_esp.toFixed(4)}</div>
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Date of edition
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
      <div>From : {samples.min_date.min_date}</div>
        <div>To : {samples.max_date.max_date}</div>
      </h4>
    </div>

  </div>
</>


  );
};

export default DashboardStates;
