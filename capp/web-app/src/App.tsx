import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Upload, FileUp, BarChart3, History, RefreshCcw, Camera } from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

const API_URL = 'http://127.0.0.1:8000';

interface Prediction {
  id: string;
  filename: string;
  object_count: number;
  details: Record<string, number>;
  created_at?: string;
  timestamp?: string;
}

function App() {
  const [history, setHistory] = useState<Prediction[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [lastResult, setLastResult] = useState<Prediction | null>(null);

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/history`);
      setHistory(res.data);
    } catch (err) {
      console.error("Failed to fetch history", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedFile) return;

    setUploading(true);
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const res = await axios.post(`${API_URL}/predict`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setLastResult(res.data);
      fetchHistory(); // Refresh history
      setSelectedFile(null); // Clear selection
    } catch (err) {
      console.error("Upload failed", err);
      alert("Upload failed! See console for details.");
    } finally {
      setUploading(false);
    }
  };

  // Prepare chart data
  const chartData = history.slice(0, 10).map(item => ({
    name: item.filename.substring(0, 10) + '...',
    count: item.object_count,
  })).reverse();

  return (
    <div className="min-h-screen bg-gray-100 p-8 font-sans text-gray-900">
      <div className="max-w-7xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex justify-between items-center bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="bg-blue-600 p-2 rounded-lg">
              <Camera className="w-8 h-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold">AI Object Counter</h1>
              <p className="text-gray-500 text-sm">Dashboard & Analysis</p>
            </div>
          </div>
          <button
            onClick={fetchHistory}
            className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <RefreshCcw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Data
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">

          {/* Upload Section */}
          <div className="lg:col-span-1 space-y-8">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Upload className="w-5 h-5 text-blue-600" />
                New Analysis
              </h2>

              <form onSubmit={handleUpload} className="space-y-4">
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:bg-gray-50 transition-colors cursor-pointer relative">
                  <input
                    type="file"
                    onChange={handleFileChange}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    accept="image/*"
                  />
                  <div className="flex flex-col items-center gap-2">
                    <FileUp className="w-10 h-10 text-gray-400" />
                    <span className="text-sm text-gray-500 font-medium">
                      {selectedFile ? selectedFile.name : "Click or Drag image here"}
                    </span>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={!selectedFile || uploading}
                  className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-semibold rounded-lg shadow-md transition-all flex justify-center items-center gap-2"
                >
                  {uploading ? 'Analyzing...' : 'Analyze Image'}
                </button>
              </form>

              {lastResult && (
                <div className="mt-6 p-4 bg-green-50 border border-green-100 rounded-lg animate-in fade-in slide-in-from-top-4">
                  <h3 className="text-green-800 font-semibold mb-2">Analysis Complete!</h3>
                  <div className="text-4xl font-extrabold text-green-700 mb-2">{lastResult.object_count} <span className="text-lg font-medium text-green-600">Total Objects</span></div>

                  <div className="mt-4">
                    <p className="text-sm font-semibold text-green-800 mb-2 uppercase tracking-wide">Breakdown</p>
                    <div className="flex flex-wrap gap-2">
                      {Object.entries(lastResult.details).map(([key, value]) => (
                        <span key={key} className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-white border border-green-200 shadow-sm">
                          <span className="font-medium text-gray-700 capitalize">{key}</span>
                          <span className="bg-green-100 text-green-800 text-xs font-bold px-2 py-0.5 rounded-full">{value}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Stats Card */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-purple-600" />
                Quick Stats
              </h2>
              <div className="grid grid-cols-2 gap-4">
                <div className="p-4 bg-purple-50 rounded-lg">
                  <div className="text-purple-500 text-sm font-medium">Total Scans</div>
                  <div className="text-2xl font-bold text-purple-700">{history.length}</div>
                </div>
                <div className="p-4 bg-indigo-50 rounded-lg">
                  <div className="text-indigo-500 text-sm font-medium">Avg Objects</div>
                  <div className="text-2xl font-bold text-indigo-700">
                    {history.length > 0
                      ? (history.reduce((acc, curr) => acc + curr.object_count, 0) / history.length).toFixed(1)
                      : 0}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Setup Chart and History */}
          <div className="lg:col-span-2 space-y-8">

            {/* Chart */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-80">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-gray-600" />
                Recent Detection Trends
              </h2>
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
                  <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#4F46E5" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* History Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
              <div className="p-6 border-b border-gray-100">
                <h2 className="text-lg font-semibold flex items-center gap-2">
                  <History className="w-5 h-5 text-gray-600" />
                  Recent History
                </h2>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm">
                  <thead className="bg-gray-50 text-gray-500 uppercase">
                    <tr>
                      <th className="px-6 py-3 font-medium">Filename</th>
                      <th className="px-6 py-3 font-medium">Count</th>
                      <th className="px-6 py-3 font-medium">Details</th>
                      <th className="px-6 py-3 font-medium">ID</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-100">
                    {history.map((item) => (
                      <tr key={item.id} className="hover:bg-gray-50 transition-colors">
                        <td className="px-6 py-4 font-medium text-gray-900">{item.filename}</td>
                        <td className="px-6 py-4">
                          <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                            {item.object_count}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-gray-500">
                          <div className="flex flex-wrap gap-1">
                            {Object.entries(item.details).map(([k, v]) => (
                              <span key={k} className="inline-flex items-center text-xs bg-gray-100 px-2 py-0.5 rounded border border-gray-200">
                                {k}: <span className="font-semibold ml-1">{v}</span>
                              </span>
                            ))}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-gray-400 font-mono text-xs">
                          {item.id}
                        </td>
                      </tr>
                    ))}
                    {history.length === 0 && (
                      <tr>
                        <td colSpan={4} className="px-6 py-8 text-center text-gray-400">
                          No history available. Upload an image to start!
                        </td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
