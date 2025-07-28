import React, { useState, useEffect } from "react";
import SideBarMap from "./components/SideBars/SideBarMap";
import Map from "./components/Map";
import DetailsSideBar from "./components/SideBars/DetailsSideBar";
import PropertiesSidebar from "./components/SideBars/PropertiesSideBar";
import TimeSeries from "./components/Map components/TimeSeries";
import { useTranslation } from 'react-i18next';

const MapTab = (props) => {
  const { t } = useTranslation();
  const [generalSettings, setGeneralSettings] = useState({
    baseMap: "Satellite",
    showLegend: true,
    showLabels: true,
  });
  const [drawArea, setDrawArea] = useState(false);
  const [projectedROI, setProjectedROI] = useState(null);
  const [pointCoordinates, setPointCoordinates] = useState(null);
  const [selectPoint, setSelectPoint] = useState(false);
  const [geoJson, setGeoJson] = useState(null);
  const [openSideBar, setOpenSideBar] = useState(null);
  const [dispalyTimeSeries, setDispalyTimeSeries] = useState(false);
  const [timeSeriesDates, setTimeSeriesDates] = useState([]);
  const [max, setMax] = useState(0);
  const [mapInstance, setMapInstance] = useState(null);
  const [checkRaster, setCheckRaster] = useState(false);
  const [loading, setLoading] = useState(false);
  const [indexOfRanger, setIndexOfRanger] = useState(0);
  const [rasters, setRasters] = useState([]);
  const [tmpFile, setTmpFile] = useState(null);
  const [dragedLay, setDragedLay] = useState(false);

  useEffect(() => {
    if (rasters?.length > 1) {
      const uniqueRasters = [];
      const seenIndices = new Set();

      for (let i = rasters.length - 1; i >= 0; i--) {
        const raster = rasters[i];
        if (!seenIndices.has(raster.index)) {
          uniqueRasters.push(raster);
          seenIndices.add(raster.index);
        } else {
          if (mapInstance) mapInstance.removeLayer(raster.layer);
        }
      }

      uniqueRasters.reverse();

      if (uniqueRasters.length !== rasters.length) {
        setRasters(uniqueRasters);
      }
    }
  }, [rasters, setRasters]);


  useEffect(() => {
    let tmp = null;
    props.layers.forEach((ele) => {
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
  }, [props.layers]);

  return (
    <div className="h-[87vh] flex">
      <div>
        <SideBarMap
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
          layers={props.layers}
          setLayers={props.setLayers}
          rasters={rasters}
          setRasters={setRasters}
          setTimeSeriesDates={setTimeSeriesDates}
          timeSeriesDates={timeSeriesDates}
          setMax={setMax}
          mapInstance={mapInstance}
          setMapInstance={setMapInstance}
          checkRaster={checkRaster}
          setCheckRaster={setCheckRaster}
          setLoading={setLoading}
          setTmpFile={setTmpFile}
          tmpFile={tmpFile}
          setDragedLay={setDragedLay}
          dragedLay={dragedLay}
          setIndexOfRanger={setIndexOfRanger}
        />
      </div>
      <div className="relative w-full z-0">
        <div className="relative z-10">
          <Map
            showLabels={generalSettings.showLabels}
            baseMap={generalSettings.baseMap}
            showLegend={generalSettings.showLegend}
            drawArea={drawArea}
            projectedROI={projectedROI}
            pointCoordinates={pointCoordinates}
            setPointCoordinates={setPointCoordinates}
            selectPoint={selectPoint}
            setGeoJson={setGeoJson}
            layers={props.layers}
            setLayers={props.setLayers}
            setDispalyTimeSeries={setDispalyTimeSeries}
            setTmpFile={setTmpFile}
            tmpFile={tmpFile}
            setDragedLay={setDragedLay}
            setLoading={setLoading}
            setProjectedROI={setProjectedROI}

          />
          {loading ? (
            <div role="status" className="absolute  top-1/2 left-1/2 z-[1000]">
              <svg
                aria-hidden="true"
                className="w-10 h-10 text-gray-200 animate-spin dark:text-gray-600 fill-blue-600"
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

        <div className="absolute flex justify-center bottom-0  w-full h-[10vh] z-20">
          {dispalyTimeSeries && (
            <TimeSeries
              timeSeriesDates={timeSeriesDates}
              indexOfRanger={indexOfRanger}
              setIndexOfRanger={setIndexOfRanger}
              max={max}
              layers={props.layers}
              setLayers={props.setLayers}
            />
          )}
        </div>
      </div>
      <DetailsSideBar
        type={"map"}
        isOpen={openSideBar?.sideBar === "details" && openSideBar?.open}
        setOpenSideBar={setOpenSideBar}
        checkRaster={checkRaster}
        setCheckRaster={setCheckRaster}
        index={openSideBar?.index}
        rasters={rasters}
        setRasters={setRasters}
        layers={props.layers}
        setLayers={props.setLayers}
        mapInstance={mapInstance}
      />
      <PropertiesSidebar
        isOpen={openSideBar?.sideBar === "properties" && openSideBar?.open}
        setOpenSideBar={setOpenSideBar}
        index={openSideBar?.index}
        ind={openSideBar?.ind}
        layers={props.layers}
        setLayers={props.setLayers}
        rasters={rasters}
      />
    </div>
  );
};

export default MapTab;
