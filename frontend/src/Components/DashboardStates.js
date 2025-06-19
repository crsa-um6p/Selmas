import React from "react";

const DashboardStates = (props) => {

  const samples = Array.isArray(props.selectedSample) ? props.selectedSample : [props.selectedSample];

  return (
    <>
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 lg:grid-cols-4 gap-6 w-full">
    

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Classification
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " : " + sample.salinity.classification
            ):(
              sample.salinity.classification
            )}
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
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " : " + sample.salinity.esp
            ):(
              sample.salinity.esp
            )
            

            }
            
          </div>
        ))}
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Sodium absorption ratio
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " : " + sample.salinity.sar
            ):(
              sample.salinity.sar
            )
            }
          </div>
        ))}
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Date of edition
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " : " + sample.Date_edition
            ):(
              sample.Date_edition
            )
            }
          </div>
        ))}
      </h4>
    </div>

  </div>
</>


  );
};

export default DashboardStates;
