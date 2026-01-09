import React from 'react';

export default function CameraList({ cameras }) {
  return (
    <div className="bg-white p-4 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Cameras</h2>
      <ul>
        {cameras.map((cam) => (
          <li key={cam.id} className="border-b py-2 flex justify-between items-center">
            <div>
              <p className="font-semibold">{cam.name}</p>
              <p className="text-sm text-gray-500">{cam.rtsp_url}</p>
              <p className="text-xs text-gray-400">{cam.location}</p>
            </div>
            <span className={`px-2 py-1 rounded text-xs ${cam.status === 'online' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
              {cam.status}
            </span>
          </li>
        ))}
        {cameras.length === 0 && <p className="text-gray-500">No cameras configured.</p>}
      </ul>
    </div>
  );
}
