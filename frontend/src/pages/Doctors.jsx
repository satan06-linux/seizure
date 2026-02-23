import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Users, MapPin, Award, Phone, Star, Search } from 'lucide-react'
import axios from 'axios'
import toast from 'react-hot-toast'

const Doctors = () => {
  const [doctors, setDoctors] = useState([])
  const [locations, setLocations] = useState([])
  const [specializations, setSpecializations] = useState([])
  const [filters, setFilters] = useState({
    location: '',
    specialization: '',
    emergency: false
  })
  const [loading, setLoading] = useState(false)
  
  useEffect(() => {
    fetchLocations()
    fetchSpecializations()
    fetchDoctors()
  }, [])
  
  const fetchLocations = async () => {
    try {
      const response = await axios.get('/api/doctors/locations')
      if (response.data.success) {
        setLocations(response.data.locations)
      }
    } catch (error) {
      console.error('Failed to fetch locations')
    }
  }
  
  const fetchSpecializations = async () => {
    try {
      const response = await axios.get('/api/doctors/specializations')
      if (response.data.success) {
        setSpecializations(response.data.specializations)
      }
    } catch (error) {
      console.error('Failed to fetch specializations')
    }
  }
  
  const fetchDoctors = async () => {
    setLoading(true)
    try {
      const params = new URLSearchParams()
      if (filters.location) params.append('location', filters.location)
      if (filters.specialization) params.append('specialization', filters.specialization)
      if (filters.emergency) params.append('emergency', 'true')
      
      const response = await axios.get(`/api/doctors?${params}`)
      if (response.data.success) {
        setDoctors(response.data.doctors)
      }
    } catch (error) {
      toast.error('Failed to fetch doctors')
    } finally {
      setLoading(false)
    }
  }
  
  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-4"
      >
        <Users className="w-20 h-20 mx-auto text-orange-600" />
        <h1 className="text-5xl font-bold gradient-text">Find a Neurologist</h1>
        <p className="text-xl text-gray-600">
          Connect with qualified specialists near you
        </p>
      </motion.div>
      
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="glass-card p-6 rounded-2xl"
      >
        <div className="grid md:grid-cols-3 gap-4 mb-4">
          <select
            value={filters.location}
            onChange={(e) => setFilters({ ...filters, location: e.target.value })}
            className="input-field"
          >
            <option value="">All Locations</option>
            {locations.map((loc, i) => (
              <option key={i} value={loc}>{loc}</option>
            ))}
          </select>
          
          <select
            value={filters.specialization}
            onChange={(e) => setFilters({ ...filters, specialization: e.target.value })}
            className="input-field"
          >
            <option value="">All Specializations</option>
            {specializations.map((spec, i) => (
              <option key={i} value={spec}>{spec}</option>
            ))}
          </select>
          
          <label className="flex items-center space-x-2 px-4 py-3 bg-white rounded-xl border-2 border-gray-200 cursor-pointer">
            <input
              type="checkbox"
              checked={filters.emergency}
              onChange={(e) => setFilters({ ...filters, emergency: e.target.checked })}
              className="w-5 h-5"
            />
            <span className="font-medium text-gray-700">Emergency Care</span>
          </label>
        </div>
        
        <button
          onClick={fetchDoctors}
          className="btn-primary w-full flex items-center justify-center space-x-2"
        >
          <Search className="w-5 h-5" />
          <span>Search Doctors</span>
        </button>
      </motion.div>
      
      <div className="grid md:grid-cols-2 gap-6">
        {doctors.map((doctor, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className="glass-card p-6 rounded-2xl card-hover"
          >
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="text-xl font-bold text-gray-800">{doctor.name}</h3>
                <p className="text-blue-600 font-medium">{doctor.specialization}</p>
              </div>
              <div className="flex items-center space-x-1 bg-yellow-100 px-3 py-1 rounded-full">
                <Star className="w-4 h-4 text-yellow-600 fill-current" />
                <span className="font-semibold text-yellow-800">{doctor.rating}</span>
              </div>
            </div>
            
            <div className="space-y-2 text-gray-600">
              <div className="flex items-center space-x-2">
                <MapPin className="w-4 h-4" />
                <span>{doctor.hospital}, {doctor.location}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Phone className="w-4 h-4" />
                <span>{doctor.phone}</span>
              </div>
              <div className="flex items-center space-x-2">
                <Award className="w-4 h-4" />
                <span>{doctor.experience_years} years experience</span>
              </div>
            </div>
            
            {doctor.accepts_emergency && (
              <div className="mt-4 inline-block px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium">
                Emergency Care Available
              </div>
            )}
          </motion.div>
        ))}
      </div>
      
      {doctors.length === 0 && !loading && (
        <div className="text-center py-12 text-gray-500">
          No doctors found. Try adjusting your filters.
        </div>
      )}
    </div>
  )
}

export default Doctors
