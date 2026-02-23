"""
Module 6: Doctor Recommender
Recommends neurologists based on location and specialization
"""
import pandas as pd
import os
from typing import List, Dict


class DoctorRecommender:
    def __init__(self, data_source='local'):
        """
        Initialize doctor recommender
        data_source: 'local' for CSV file, 'web' for web scraping (future)
        """
        self.data_source = data_source
        self.doctors_df = None
        self.load_doctors()
    
    def load_doctors(self):
        """Load doctor database"""
        if self.data_source == 'local':
            self.load_local_database()
        else:
            # Future: implement web scraping
            self.load_local_database()
    
    def load_local_database(self):
        """Load doctors from local CSV or create sample data"""
        csv_path = 'datasets/neurologists.csv'
        
        if os.path.exists(csv_path):
            self.doctors_df = pd.read_csv(csv_path)
            print(f"Loaded {len(self.doctors_df)} doctors from database")
        else:
            # Create sample database
            self.doctors_df = self.create_sample_database()
            print("Using sample doctor database")
    
    def create_sample_database(self) -> pd.DataFrame:
        """Create sample neurologist database"""
        doctors = [
            {
                'name': 'Dr. Sarah Johnson',
                'specialization': 'Epilepsy & Seizure Disorders',
                'hospital': 'City Medical Center',
                'location': 'New York, NY',
                'phone': '(555) 123-4567',
                'experience_years': 15,
                'rating': 4.8,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. Michael Chen',
                'specialization': 'Pediatric Neurology',
                'hospital': 'Children\'s Hospital',
                'location': 'Los Angeles, CA',
                'phone': '(555) 234-5678',
                'experience_years': 12,
                'rating': 4.9,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. Emily Rodriguez',
                'specialization': 'Epilepsy Surgery',
                'hospital': 'University Medical Center',
                'location': 'Chicago, IL',
                'phone': '(555) 345-6789',
                'experience_years': 18,
                'rating': 4.7,
                'accepts_emergency': False
            },
            {
                'name': 'Dr. James Wilson',
                'specialization': 'General Neurology',
                'hospital': 'Metro Health Hospital',
                'location': 'Houston, TX',
                'phone': '(555) 456-7890',
                'experience_years': 10,
                'rating': 4.6,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. Lisa Anderson',
                'specialization': 'Epilepsy & EEG',
                'hospital': 'Regional Medical Center',
                'location': 'Phoenix, AZ',
                'phone': '(555) 567-8901',
                'experience_years': 14,
                'rating': 4.8,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. Robert Taylor',
                'specialization': 'Neurophysiology',
                'hospital': 'St. Mary\'s Hospital',
                'location': 'Philadelphia, PA',
                'phone': '(555) 678-9012',
                'experience_years': 20,
                'rating': 4.9,
                'accepts_emergency': False
            },
            {
                'name': 'Dr. Maria Garcia',
                'specialization': 'Pediatric Epilepsy',
                'hospital': 'Children\'s Specialty Center',
                'location': 'San Antonio, TX',
                'phone': '(555) 789-0123',
                'experience_years': 11,
                'rating': 4.7,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. David Kim',
                'specialization': 'Epilepsy & Sleep Disorders',
                'hospital': 'Advanced Neurology Clinic',
                'location': 'San Diego, CA',
                'phone': '(555) 890-1234',
                'experience_years': 13,
                'rating': 4.8,
                'accepts_emergency': False
            },
            {
                'name': 'Dr. Jennifer Brown',
                'specialization': 'General Neurology',
                'hospital': 'Community Hospital',
                'location': 'Dallas, TX',
                'phone': '(555) 901-2345',
                'experience_years': 9,
                'rating': 4.5,
                'accepts_emergency': True
            },
            {
                'name': 'Dr. Christopher Lee',
                'specialization': 'Epilepsy & Neurostimulation',
                'hospital': 'Brain & Spine Institute',
                'location': 'San Jose, CA',
                'phone': '(555) 012-3456',
                'experience_years': 16,
                'rating': 4.9,
                'accepts_emergency': False
            }
        ]
        
        return pd.DataFrame(doctors)
    
    def recommend_doctors(self, 
                         risk_level: str = None,
                         location: str = None,
                         specialization: str = None,
                         emergency: bool = False,
                         top_n: int = 5) -> List[Dict]:
        """
        Recommend neurologists based on criteria
        
        Args:
            risk_level: Patient's risk level (HIGH, MEDIUM, LOW)
            location: Preferred location
            specialization: Required specialization
            emergency: Whether emergency care is needed
            top_n: Number of recommendations to return
        """
        df = self.doctors_df.copy()
        
        # Filter by emergency availability
        if emergency or risk_level == 'HIGH':
            df = df[df['accepts_emergency'] == True]
        
        # Filter by location if specified
        if location:
            df = df[df['location'].str.contains(location, case=False, na=False)]
        
        # Filter by specialization if specified
        if specialization:
            df = df[df['specialization'].str.contains(specialization, case=False, na=False)]
        
        # Sort by rating and experience
        df = df.sort_values(['rating', 'experience_years'], ascending=[False, False])
        
        # Get top N
        top_doctors = df.head(top_n)
        
        # Convert to list of dictionaries
        recommendations = []
        for _, doctor in top_doctors.iterrows():
            recommendations.append({
                'name': doctor['name'],
                'specialization': doctor['specialization'],
                'hospital': doctor['hospital'],
                'location': doctor['location'],
                'phone': doctor['phone'],
                'experience_years': int(doctor['experience_years']),
                'rating': float(doctor['rating']),
                'accepts_emergency': bool(doctor['accepts_emergency'])
            })
        
        return recommendations
    
    def get_emergency_contacts(self) -> List[Dict]:
        """Get emergency neurologist contacts"""
        return self.recommend_doctors(emergency=True, top_n=3)
    
    def search_by_name(self, name: str) -> List[Dict]:
        """Search doctors by name"""
        df = self.doctors_df[
            self.doctors_df['name'].str.contains(name, case=False, na=False)
        ]
        
        results = []
        for _, doctor in df.iterrows():
            results.append({
                'name': doctor['name'],
                'specialization': doctor['specialization'],
                'hospital': doctor['hospital'],
                'location': doctor['location'],
                'phone': doctor['phone'],
                'experience_years': int(doctor['experience_years']),
                'rating': float(doctor['rating'])
            })
        
        return results
    
    def get_all_locations(self) -> List[str]:
        """Get all available locations"""
        return sorted(self.doctors_df['location'].unique().tolist())
    
    def get_all_specializations(self) -> List[str]:
        """Get all specializations"""
        return sorted(self.doctors_df['specialization'].unique().tolist())
    
    def format_recommendation(self, doctor: Dict) -> str:
        """Format doctor recommendation as readable text"""
        text = f"""
**{doctor['name']}**
Specialization: {doctor['specialization']}
Hospital: {doctor['hospital']}
Location: {doctor['location']}
Phone: {doctor['phone']}
Experience: {doctor['experience_years']} years
Rating: {doctor['rating']}/5.0
Emergency Care: {'✓ Available' if doctor['accepts_emergency'] else '✗ Not Available'}
"""
        return text.strip()
    
    def get_recommendations_text(self, recommendations: List[Dict]) -> str:
        """Format multiple recommendations as text"""
        if not recommendations:
            return "No doctors found matching your criteria."
        
        text = f"**Found {len(recommendations)} Recommended Neurologist(s):**\n\n"
        
        for i, doctor in enumerate(recommendations, 1):
            text += f"{i}. {self.format_recommendation(doctor)}\n\n"
        
        return text


if __name__ == "__main__":
    # Test doctor recommender
    recommender = DoctorRecommender()
    
    print("Testing Doctor Recommender\n")
    
    # Test 1: General recommendations
    print("1. General Recommendations:")
    doctors = recommender.recommend_doctors(top_n=3)
    print(recommender.get_recommendations_text(doctors))
    
    # Test 2: Emergency recommendations
    print("\n2. Emergency Recommendations:")
    emergency_doctors = recommender.get_emergency_contacts()
    print(recommender.get_recommendations_text(emergency_doctors))
    
    # Test 3: Location-based
    print("\n3. Location-based (California):")
    ca_doctors = recommender.recommend_doctors(location='CA', top_n=2)
    print(recommender.get_recommendations_text(ca_doctors))
