import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CameraList from './CameraList';
import EventFeed from './EventFeed';

const API_URL = 'http://localhost:8000';

export default function Dashboard() {
  const [cameras, setCameras] = useState([]);
  const [events, setEvents] = useState([]);
  const [newCamUrl, setNewCamUrl] = useState('');
  const [newCamName, setNewCamName] = useState('');

  const fetchData = async () => {
    try {
      const cams = await axios.get(`${API_URL}/cameras`);
      setCameras(cams.data);
      const evts = await axios.get(`${API_URL}/events`);
      setEvents(evts.data);
    } catch (error) {
      console.error("Error fetching data", error);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const [selectedCameraId, setSelectedCameraId] = useState(null);

  const addCamera = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_URL}/cameras`, {
        name: newCamName,
        rtsp_url: newCamUrl,
        status: 'offline',
        // Default zone: entire frame (roughly) - in real app, UI editor needed
        zone_config: JSON.stringify([{name: "Zone 1", points: [[0,0], [640,0], [640,480], [0,480]]}])
      });
      setNewCamName('');
      setNewCamUrl('');
      fetchData();
    } catch (error) {
      console.error("Error adding camera", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-8">
      <header className="mb-8 flex justify-between items-center">
         <h1 className="text-3xl font-bold text-blue-900">SentinelSight</h1>
         <div className="text-sm text-gray-600">MVP Build</div>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1">
          <div className="mb-4">
              <h3 className="font-bold mb-2">Select Camera</h3>
               <select className="w-full border p-2 rounded" onChange={(e) => setSelectedCameraId(e.target.value)}>
                   <option value="">Select a camera...</option>
                   {cameras.map(c => <option key={c.id} value={c.id}>{c.name}</option>)}
               </select>
          </div>
          <CameraList cameras={cameras} />

          <div className="bg-white p-4 rounded shadow mt-4">
            <h3 className="font-bold mb-2">Add Camera</h3>
            <form onSubmit={addCamera} className="space-y-2">
              <input
                type="text"
                placeholder="Camera Name"
                className="w-full border p-2 rounded"
                value={newCamName}
                onChange={(e) => setNewCamName(e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="RTSP URL"
                className="w-full border p-2 rounded"
                value={newCamUrl}
                onChange={(e) => setNewCamUrl(e.target.value)}
                required
              />
              <button type="submit" className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">
                Add Stream
              </button>
            </form>
          </div>
        </div>

        <div className="md:col-span-2">
           <div className="bg-black h-96 rounded flex items-center justify-center text-white mb-4 overflow-hidden relative">
              {selectedCameraId ? (
                   <img
                      src={`${API_URL}/cameras/${selectedCameraId}/stream?t=${Date.now()}`}
                      className="w-full h-full object-contain"
                      alt="Live Stream"
                      onError={(e) => {e.target.style.display='none';}}
                   />
              ) : (
                  <span>Select a camera to view live stream</span>
              )}
              {selectedCameraId && <div className="absolute bottom-2 right-2 text-xs bg-black/50 p-1 rounded">Refreshes on event/poll</div>}
           </div>

           <EventFeed events={events} />
        </div>
      </div>
    </div>
  );
}
