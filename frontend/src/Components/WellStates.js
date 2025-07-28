import React from "react";

const WellStates = (props) => {

  const samples = Array.isArray(props.selectedSample) ? props.selectedSample : [props.selectedSample];

  return (
    <>
  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 gap-6 w-full">
    

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Date
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Date
            ):(
              sample.Date
            )}
          </div>
        ))
        }
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Depth
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " m"
            ):(
              sample.Depth + " m"
            )
            

            }
            
          </div>
        ))}
      </h4>
    </div>

    <div className="max-w-full px-6 py-3 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100">
      <h6 className="text-md font-nunito text-blue-600 font-bold">
         Electrical Conductivity
      </h6>
      <h4 className="font-bold tracking-tight text-gray-900">
        {samples.map((sample, index) => (
          <div key={index}>
            {samples.length > 1 ? (
                sample.Depth + " m : " + parseFloat(sample.ec).toFixed(2) +" ms/cm"
            ):(
              parseFloat(sample.ec).toFixed(2) +" ms/cm"
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

export default WellStates;
