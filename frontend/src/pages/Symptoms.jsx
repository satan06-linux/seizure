import { useState } from 'react'
import { motion } from 'framer-motion'
import { Stethoscope, Send, AlertTriangle, CheckCircle2, Loader } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

const Symptoms = () => {
  const [symptoms, setSymptoms] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  
  const handleAnalyze = async () => {
    if (!symptoms.trim()) {
      toast.error('Please describe your symptoms')
      return
    }
    
    setLoading(true)
    try {
      const response = await axios.post('/api/symptoms/analyze', { symptoms })
      if (response.data.success) {
        setResult(response.data.result)
        toast.success('Analysis complete!')
      }
    } catch (error) {
      toast.error('Analysis failed')
    } finally {
      setLoading(false)
    }
  }
  
  const getRiskColor = (level) => {
    const colors = {
      'HIGH': 'bg-red-100 text-red-800 border-red-300',
      'MEDIUM': 'bg-orange-100 text-orange-800 border-orange-300',
      'LOW': 'bg-green-100 text-green-800 border-green-300',
      'MINIMAL': 'bg-blue-100 text-blue-800 border-blue-300'
    }
    return colors[level] || 'bg-gray-100 text-gray-800 border-gray-300'
  }
  
  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <Stethoscope className="w-20 h-20 mx-auto text-purple-600" />
        <h1 className="text-5xl font-bold gradient-text">Symptom Checker</h1>
        <p className="text-xl text-gray-600">
          Describe your symptoms for AI-powered risk assessment
        </p>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-8 rounded-2xl space-y-6"
      >
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Describe Your Symptoms
          </label>
          <textarea
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            placeholder="Example: I feel dizzy, confused, and seeing strange lights..."
            className="input-field min-h-[150px] resize-none"
          />
        </div>
        
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          {loading ? (
            <>
              <Loader className="w-5 h-5 animate-spin" />
              <span>Analyzing...</span>
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              <span>Analyze Symptoms</span>
            </>
          )}
        </button>
      </motion.div>
      
      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <div className="glass-card p-8 rounded-2xl">
            <h2 className="text-3xl font-bold text-gray-800 mb-6">Analysis Results</h2>
            
            <div className="grid md:grid-cols-3 gap-4 mb-6">
              <div className={`p-4 rounded-xl border-2 ${getRiskColor(result.risk_level)}`}>
                <p className="text-sm font-medium mb-1">Risk Level</p>
                <p className="text-2xl font-bold">{result.risk_level}</p>
              </div>
              
              <div className="p-4 rounded-xl bg-purple-50 border-2 border-purple-200">
                <p className="text-sm font-medium text-purple-700 mb-1">Risk Score</p>
                <p className="text-2xl font-bold text-purple-800">{result.risk_score}/100</p>
              </div>
              
              <div className="p-4 rounded-xl bg-blue-50 border-2 border-blue-200">
                <p className="text-sm font-medium text-blue-700 mb-1">Condition</p>
                <p className="text-2xl font-bold text-blue-800">{result.possible_condition}</p>
              </div>
            </div>
            
            {result.detected_symptoms.length > 0 && (
              <div className="mb-6">
                <h3 className="font-semibold text-gray-800 mb-3">Detected Symptoms</h3>
                <div className="flex flex-wrap gap-2">
                  {result.detected_symptoms.map((s, i) => (
                    <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">
                      {s.symptom}
                    </span>
                  ))}
                </div>
              </div>
            )}
            
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg mb-6">
              <p className="text-gray-700">{result.explanation}</p>
            </div>
            
            <div>
              <h3 className="font-semibold text-gray-800 mb-3">Recommendations</h3>
              <ul className="space-y-2">
                {result.recommendations.map((rec, i) => (
                  <li key={i} className="flex items-start space-x-2">
                    <CheckCircle2 className="w-5 h-5 text-green-500 flex-shrink-0 mt-0.5" />
                    <span className="text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default Symptoms
