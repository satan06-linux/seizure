import { useState } from 'react'
import { motion } from 'framer-motion'
import { Upload as UploadIcon, FileText, Image, File, CheckCircle, AlertCircle, Loader } from 'lucide-react'
import { useDropzone } from 'react-dropzone'
import axios from 'axios'
import toast from 'react-hot-toast'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

const Upload = () => {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'text/csv': ['.csv'],
      'application/pdf': ['.pdf'],
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/octet-stream': ['.edf']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setFile(acceptedFiles[0])
        setResult(null)
      }
    }
  })
  
  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first')
      return
    }
    
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    
    try {
      const response = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      if (response.data.success) {
        setResult(response.data.result)
        toast.success('File processed successfully!')
      } else {
        toast.error(response.data.error || 'Processing failed')
      }
    } catch (error) {
      toast.error(error.response?.data?.error || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }
  
  const getFileIcon = (filename) => {
    const ext = filename?.split('.').pop().toLowerCase()
    if (ext === 'csv') return <FileText className="w-12 h-12 text-green-500" />
    if (ext === 'pdf') return <FileText className="w-12 h-12 text-red-500" />
    if (['png', 'jpg', 'jpeg'].includes(ext)) return <Image className="w-12 h-12 text-blue-500" />
    return <File className="w-12 h-12 text-gray-500" />
  }
  
  const getRiskColor = (level) => {
    const colors = {
      'HIGH': 'from-red-500 to-red-600',
      'MEDIUM': 'from-orange-500 to-orange-600',
      'LOW': 'from-green-500 to-green-600',
      'MINIMAL': 'from-blue-500 to-blue-600'
    }
    return colors[level] || 'from-gray-500 to-gray-600'
  }
  
  const chartData = result?.prediction?.probabilities ? 
    Object.entries(result.prediction.probabilities).map(([name, value]) => ({
      name,
      value: parseFloat(value.toFixed(2))
    })) : []
  
  const COLORS = ['#10b981', '#f59e0b', '#ef4444']
  
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <h1 className="text-5xl font-bold gradient-text">Upload EEG File</h1>
        <p className="text-xl text-gray-600">
          Upload your EEG data for AI-powered seizure detection
        </p>
      </motion.div>
      
      {/* Upload Area */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-8 rounded-2xl"
      >
        <div
          {...getRootProps()}
          className={`border-4 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-300 ${
            isDragActive
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <UploadIcon className="w-20 h-20 mx-auto mb-4 text-gray-400" />
          
          {file ? (
            <div className="space-y-4">
              <div className="flex items-center justify-center space-x-4">
                {getFileIcon(file.name)}
                <div className="text-left">
                  <p className="font-semibold text-gray-800">{file.name}</p>
                  <p className="text-sm text-gray-500">
                    {(file.size / 1024).toFixed(2)} KB
                  </p>
                </div>
              </div>
              <CheckCircle className="w-8 h-8 mx-auto text-green-500" />
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-xl font-semibold text-gray-700">
                {isDragActive ? 'Drop file here' : 'Drag & drop file here'}
              </p>
              <p className="text-gray-500">or click to browse</p>
              <p className="text-sm text-gray-400">
                Supported: CSV, PDF, PNG, JPG, EDF
              </p>
            </div>
          )}
        </div>
        
        {file && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="mt-6 flex justify-center space-x-4"
          >
            <button
              onClick={handleUpload}
              disabled={loading}
              className="btn-primary flex items-center space-x-2"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 animate-spin" />
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <UploadIcon className="w-5 h-5" />
                  <span>Analyze File</span>
                </>
              )}
            </button>
            
            <button
              onClick={() => {
                setFile(null)
                setResult(null)
              }}
              className="btn-secondary"
            >
              Clear
            </button>
          </motion.div>
        )}
      </motion.div>
      
      {/* Results */}
      {result?.prediction && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          {/* Prediction Card */}
          <div className="glass-card p-8 rounded-2xl">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Analysis Results</h2>
            
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="text-center p-6 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl">
                <p className="text-sm text-gray-600 mb-2">Prediction</p>
                <p className="text-3xl font-bold text-blue-600">
                  {result.prediction.prediction}
                </p>
              </div>
              
              <div className="text-center p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl">
                <p className="text-sm text-gray-600 mb-2">Confidence</p>
                <p className="text-3xl font-bold text-purple-600">
                  {result.prediction.confidence.toFixed(1)}%
                </p>
              </div>
              
              <div className="text-center p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl">
                <p className="text-sm text-gray-600 mb-2">Risk Level</p>
                <div className={`inline-block px-4 py-2 rounded-lg bg-gradient-to-r ${getRiskColor(result.prediction.risk_level)} text-white font-bold`}>
                  {result.prediction.risk_level}
                </div>
              </div>
            </div>
            
            {/* Explanation */}
            <div className="bg-blue-50 border-l-4 border-blue-500 p-6 rounded-lg">
              <div className="flex items-start space-x-3">
                <AlertCircle className="w-6 h-6 text-blue-500 flex-shrink-0 mt-1" />
                <div>
                  <h3 className="font-semibold text-gray-800 mb-2">Explanation</h3>
                  <p className="text-gray-700">{result.prediction.explanation}</p>
                </div>
              </div>
            </div>
          </div>
          
          {/* Probability Chart */}
          <div className="glass-card p-8 rounded-2xl">
            <h3 className="text-2xl font-bold text-gray-800 mb-6">Probability Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default Upload
