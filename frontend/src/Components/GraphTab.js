import React, { useEffect, useState } from "react";
import SideBarGraph from "./components/SideBars/SideBarGraph";
import Graph from "./components/Graph";
import MapModal from "./components/Map components/MapModal";
import DetailsSideBar from "./components/SideBars/DetailsSideBar";
import PropertiesSidebar from "./components/SideBars/PropertiesSideBar";
import { useTranslation } from 'react-i18next';

const GraphTab = (props) => {
  const [drawArea, setDrawArea] = useState(false);
  const [projectedROI, setProjectedROI] = useState(null);
  const [pointCoordinates, setPointCoordinates] = useState(null);
  const [selectPoint, setSelectPoint] = useState(false);
  const [geoJson, setGeoJson] = useState(null);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [openSideBar, setOpenSideBar] = useState(null);
  const { t } = useTranslation();

  const [generalSettings, setGeneralSettings] = useState({
    baseMap: "Satellite",
    graphTitle: "",
    graphType: "",
    showLabels: true,
  });

  
  useEffect(() => {
    let tmp = null;
    props.variables.forEach((ele) => {
      if (ele.displaySideBar !== null) {
        tmp = {
          sideBar: ele.displaySideBar.sideBar,
          index: ele.displaySideBar.index,
          ind: ele.index,
          open: true,
        };
      }
      setOpenSideBar(tmp);
    });
  }, [props.variables]);

  return (
    <>
      <div className="relative ">
        <MapModal
          open={open}
          setOpen={setOpen}
          generalSettings={generalSettings}
          drawArea={drawArea}
          projectedROI={projectedROI}
          pointCoordinates={pointCoordinates}
          setPointCoordinates={setPointCoordinates}
          selectPoint={selectPoint}
          setGeoJson={setGeoJson}
        />
        {loading ? (
          <div role="status" className="absolute left-1/2  top-[30vh] z-20">
            <svg
              aria-hidden="true"
              className="w-10 h-10 text-gray-200 animate-spin  fill-blue-600"
              viewBox="0 0 100 101"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                fill="white"
              />
              <path
                d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                fill="grey"
              />
            </svg>
            <span className="sr-only">{t("loading")}...</span>
          </div>
        ) : (
          ""
        )}
      </div>
      <div className="h-[87vh] flex">
        <div>
          <SideBarGraph
            setOpen={setOpen}
            setDrawArea={setDrawArea}
            generalSettings={generalSettings}
            setGeneralSettings={setGeneralSettings}
            setProjectedROI={setProjectedROI}
            pointCoordinates={pointCoordinates}
            setPointCoordinates={setPointCoordinates}
            setSelectPoint={setSelectPoint}
            selectPoint={selectPoint}
            setGeoJson={setGeoJson}
            geoJson={geoJson}
            projectedROI={projectedROI}
            setTab={props.setTab}
            setLoading={setLoading}
            variables={props.variables}
            setVariables={props.setVariables}
            layers={props.layers}
          />
        </div>
        <div className="relative w-full z-10">
          <Graph
            setOpen={setOpen}
            setDrawArea={setDrawArea}
            generalSettings={generalSettings}
            variables={props.variables}
            setVariables={props.setVariables}
            loading={loading}
          />
          
        </div>
        <DetailsSideBar
          type={"graph"}
          isOpen={openSideBar?.sideBar === "details" && openSideBar?.open}
          setOpenSideBar={setOpenSideBar}
          index={openSideBar?.index}
          layers={props.variables}
          setLayers={props.setVariables}
        />
        {/* <PropertiesSidebar
          isOpen={openSideBar?.sideBar === "properties" && openSideBar?.open}
          setOpenSideBar={setOpenSideBar}
          index={openSideBar?.index}
          layers={props.variables}
          setLayers={props.setVariables}
        /> */}
      </div>
    </>
  );
};

export default GraphTab;
