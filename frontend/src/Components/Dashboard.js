import React, { useEffect, useState } from 'react'
import TextureChart from './charts/TextureChart'
import QualityChart from './charts/QualityChart'
import DashboardMap from './DashboardMap'
import DashboardStates from './DashboardStates'
import DashboardAggregated from './DashboardAggregated'
import MicroElementsChart from './charts/MicroElementsChart'
import SoilMinerral from './charts/SoilMinerals'

import WellMineral from './charts/WellMineral'
import WellComposition from './charts/WellComposition'
import WellStates from './WellStates'
// import axiosInstance from '../utils/axiosConfig'

const Dashboard = () => {

  const [GeoData, setGeoData] = useState(null)
  const [selectedSample, setSelectedSample] = useState(null)

  useEffect(()=>{

    const fetchData = async ()  =>  {
      try{
        const response = await fetch('http://localhost:8000/visualisation/dashboard_data/')
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log("data",data);
        setGeoData(data);
      } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
      }
    }
    
    fetchData()
  }, [])

  useEffect(()=>{
    console.log("selectedSample",selectedSample);
  },[selectedSample])

  




  return (
    
    <div className='bg-gray-200 w-full p-4 h-100 z-0 '>
        <div className=" h-100 ">
          {GeoData ? 
          <>
            <div className="state_cards flex space-x-4 w-full">
              {selectedSample == null ?
               <DashboardAggregated aggregated_data={GeoData.soil_data.aggregated_data}/>
               
                : 
                selectedSample && selectedSample[0].type == "SoilSample" ?
                <DashboardStates selectedSample={selectedSample} GeoData={GeoData}/>
                :
                <WellStates selectedSample={selectedSample} />
              }
              
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full pt-4">


              <div className="space-y-3">

                { selectedSample == null  ?
                  <TextureChart selectedSample={GeoData.soil_data.aggregated_data.properties} />
                : 
                selectedSample && selectedSample[0].type == "SoilSample" ?
                  <TextureChart selectedSample={selectedSample} />
                :
                <WellMineral selectedSample={selectedSample} />
                }

                {selectedSample == null ?
                <MicroElementsChart selectedSample={GeoData.soil_data.aggregated_data.properties} />
                :
                selectedSample && selectedSample[0].type == "SoilSample" ?
                <MicroElementsChart selectedSample={selectedSample} />
                :
                <></>
                }

              </div>


              <div className="space-y-3">

              {selectedSample == null ?
                <QualityChart selectedSample={GeoData.soil_data.aggregated_data.properties} />
                :
                selectedSample && selectedSample[0].type == "SoilSample" ?
                <QualityChart selectedSample={selectedSample} />
                :
                <WellComposition selectedSample={selectedSample} />
                }
                <SoilMinerral selectedSample={GeoData.aggregated_data.properties} />

              </div>

              <div className="space-y-3">
                <DashboardMap
                  GeoData={GeoData}
                  setSelectedSample={setSelectedSample}
                  selectedSample={selectedSample}
                />
              </div>
              
            </div>

          </>
        :
        <div className="h-[80vh] rounded-xl flex items-center justify-center bg-white">
          <div className="h-100 ">
              <h3 className='text-center'>Loading...</h3>
              <div className="relative">
                  <div className="h-24 w-24 rounded-full border-t-8 border-b-8 border-gray-200"></div>
                  <div className="absolute top-0 left-0 h-24 w-24 rounded-full border-t-8 border-b-8 border-blue-500 animate-spin">
                  </div>
              </div>
          </div>
        </div>
        }
          
        </div>
    </div>
  )
}

export default Dashboard