import { motion } from 'framer-motion'
import { Brain, Upload, Stethoscope, MessageCircle, Users, Activity, Shield, Zap, TrendingUp } from 'lucide-react'
import { Link } from 'react-router-dom'

const Home = () => {
  const features = [
    {
      icon: Upload,
      title: 'Multi-Format Upload',
      description: 'Support for CSV, PDF, Image, and EDF files',
      color: 'from-blue-500 to-cyan-500',
      link: '/upload'
    },
    {
      icon: Stethoscope,
      title: 'Symptom Analysis',
      description: 'AI-powered symptom checker with risk assessment',
      color: 'from-purple-500 to-pink-500',
      link: '/symptoms'
    },
    {
      icon: MessageCircle,
      title: 'AI Chatbot',
      description: 'Get instant answers about seizures and epilepsy',
      color: 'from-green-500 to-emerald-500',
      link: '/chat'
    },
    {
      icon: Users,
      title: 'Find Neurologists',
      description: 'Connect with qualified specialists near you',
      color: 'from-orange-500 to-red-500',
      link: '/doctors'
    },
  ]
  
  const stats = [
    { icon: Activity, label: 'Detection Accuracy', value: '95%', color: 'text-blue-600' },
    { icon: Shield, label: 'Risk Levels', value: '4', color: 'text-purple-600' },
    { icon: Zap, label: 'Response Time', value: '<2s', color: 'text-green-600' },
    { icon: TrendingUp, label: 'File Formats', value: '5+', color: 'text-orange-600' },
  ]
  
  return (
    <div className="space-y-20">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center space-y-8 py-20"
      >
        <motion.div
          animate={{ 
            scale: [1, 1.05, 1],
            rotate: [0, 5, -5, 0]
          }}
          transition={{ duration: 5, repeat: Infinity }}
          className="inline-block"
        >
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-full blur-3xl opacity-30 animate-pulse"></div>
            <Brain className="relative w-32 h-32 mx-auto text-blue-600" />
          </div>
        </motion.div>
        
        <div className="space-y-4">
          <h1 className="text-6xl md:text-7xl font-bold">
            <span className="gradient-text">SeizureGuard AI</span>
          </h1>
          <p className="text-2xl text-gray-600 max-w-3xl mx-auto">
            Intelligent Seizure Detection and Neurologist Recommendation System
          </p>
          <p className="text-lg text-gray-500 max-w-2xl mx-auto">
            Powered by advanced machine learning to detect seizures, analyze symptoms, 
            and connect you with healthcare professionals
          </p>
        </div>
        
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/upload">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary text-lg"
            >
              Get Started
            </motion.button>
          </Link>
          <Link to="/chat">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-secondary text-lg"
            >
              Talk to AI
            </motion.button>
          </Link>
        </div>
      </motion.section>
      
      {/* Stats Section */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon
          return (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.05 }}
              className="glass-card p-6 rounded-2xl text-center card-hover"
            >
              <Icon className={`w-12 h-12 mx-auto mb-4 ${stat.color}`} />
              <div className="text-3xl font-bold text-gray-800">{stat.value}</div>
              <div className="text-sm text-gray-600 mt-2">{stat.label}</div>
            </motion.div>
          )
        })}
      </section>
      
      {/* Features Section */}
      <section className="space-y-12">
        <div className="text-center space-y-4">
          <h2 className="text-4xl font-bold text-gray-800">Powerful Features</h2>
          <p className="text-xl text-gray-600">Everything you need for seizure detection and management</p>
        </div>
        
        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon
            return (
              <Link key={index} to={feature.link}>
                <motion.div
                  initial={{ opacity: 0, x: index % 2 === 0 ? -20 : 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ scale: 1.02 }}
                  className="glass-card p-8 rounded-2xl card-hover group cursor-pointer"
                >
                  <div className="flex items-start space-x-4">
                    <div className={`p-4 rounded-xl bg-gradient-to-br ${feature.color} group-hover:scale-110 transition-transform duration-300`}>
                      <Icon className="w-8 h-8 text-white" />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-800 mb-2">{feature.title}</h3>
                      <p className="text-gray-600">{feature.description}</p>
                    </div>
                  </div>
                </motion.div>
              </Link>
            )
          })}
        </div>
      </section>
      
      {/* How It Works */}
      <section className="glass-card p-12 rounded-3xl">
        <div className="text-center space-y-4 mb-12">
          <h2 className="text-4xl font-bold text-gray-800">How It Works</h2>
          <p className="text-xl text-gray-600">Simple, fast, and accurate</p>
        </div>
        
        <div className="grid md:grid-cols-4 gap-8">
          {[
            { step: '1', title: 'Upload Data', desc: 'Upload EEG files or describe symptoms' },
            { step: '2', title: 'AI Analysis', desc: 'Advanced ML processes your data' },
            { step: '3', title: 'Get Results', desc: 'Receive detailed predictions' },
            { step: '4', title: 'Find Help', desc: 'Connect with neurologists' },
          ].map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              className="text-center space-y-4"
            >
              <div className="relative mx-auto w-20 h-20">
                <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full blur-xl opacity-50"></div>
                <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 rounded-full w-20 h-20 flex items-center justify-center">
                  <span className="text-3xl font-bold text-white">{item.step}</span>
                </div>
              </div>
              <h3 className="text-xl font-bold text-gray-800">{item.title}</h3>
              <p className="text-gray-600">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>
      
      {/* CTA Section */}
      <section className="text-center space-y-8 py-20">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card p-12 rounded-3xl bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10"
        >
          <h2 className="text-4xl font-bold text-gray-800 mb-4">Ready to Get Started?</h2>
          <p className="text-xl text-gray-600 mb-8">
            Join thousands using AI-powered seizure detection
          </p>
          <Link to="/upload">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary text-lg"
            >
              Start Analysis Now
            </motion.button>
          </Link>
        </motion.div>
      </section>
      
      {/* Disclaimer */}
      <section className="text-center text-sm text-gray-500 pb-8">
        <p className="max-w-3xl mx-auto">
          ⚠️ This is an AI assistant tool for educational purposes. 
          Always consult healthcare professionals for medical advice. 
          In case of emergency, call 911 immediately.
        </p>
      </section>
    </div>
  )
}

export default Home
