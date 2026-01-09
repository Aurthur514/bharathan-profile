import React from 'react';

export default function EventFeed({ events }) {
  return (
    <div className="bg-white p-4 rounded shadow mt-4">
      <h2 className="text-xl font-bold mb-4">Event Feed</h2>
      <div className="space-y-4">
        {events.map((evt) => (
          <div key={evt.id} className="flex border rounded p-3">
            <div className="w-24 h-24 bg-gray-200 flex-shrink-0 mr-4">
               {evt.snapshot_path ? (
                   <div className="w-full h-full bg-cover bg-center" style={{ backgroundImage: `url(http://localhost:8000/${evt.snapshot_path})` }}></div>
               ) : (
                   <div className="flex items-center justify-center h-full text-xs text-gray-500">No Image</div>
               )}
            </div>
            <div>
              <p className="font-bold text-red-600">{evt.rule_name}</p>
              <p className="text-sm">Camera: {evt.camera_id}</p>
              <p className="text-sm">Object: {evt.object_type} ({Math.round(evt.confidence * 100)}%)</p>
              <p className="text-xs text-gray-500">{new Date(evt.timestamp).toLocaleString()}</p>
            </div>
          </div>
        ))}
        {events.length === 0 && <p className="text-gray-500">No events yet.</p>}
      </div>
    </div>
  );
}
