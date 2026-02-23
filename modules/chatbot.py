"""
Module 5: Chatbot
Intelligent chatbot for seizure-related queries and support
"""
import re
from datetime import datetime
from typing import Dict, List


class SeizureChatbot:
    def __init__(self):
        self.conversation_history = []
        
        # Define response patterns
        self.patterns = {
            # Greetings
            r'\b(hi|hello|hey|greetings)\b': self.respond_greeting,
            
            # Seizure information
            r'\b(what is|what are|tell me about|explain)\s+(seizure|epilepsy)\b': self.respond_seizure_info,
            
            # Symptoms
            r'\b(symptom|sign|warning)\b': self.respond_symptoms,
            
            # Emergency
            r'\b(emergency|urgent|help|911)\b': self.respond_emergency,
            
            # Treatment
            r'\b(treatment|medication|medicine|cure)\b': self.respond_treatment,
            
            # Prevention
            r'\b(prevent|avoid|trigger)\b': self.respond_prevention,
            
            # First aid
            r'\b(first aid|what to do|how to help)\b': self.respond_first_aid,
            
            # Types
            r'\b(type|kind|category)\b.*\b(seizure)\b': self.respond_types,
            
            # Diagnosis
            r'\b(diagnos|test|eeg)\b': self.respond_diagnosis,
            
            # Living with epilepsy
            r'\b(living|lifestyle|daily life)\b': self.respond_lifestyle,
            
            # Safety
            r'\b(safety|safe|precaution)\b': self.respond_safety,
        }
        
        # Knowledge base
        self.knowledge = {
            'seizure_types': [
                'Generalized Tonic-Clonic (Grand Mal)',
                'Absence (Petit Mal)',
                'Focal (Partial) Seizures',
                'Myoclonic Seizures',
                'Atonic Seizures'
            ],
            'common_triggers': [
                'Lack of sleep',
                'Stress',
                'Alcohol consumption',
                'Flashing lights',
                'Missed medications',
                'Illness or fever',
                'Hormonal changes'
            ],
            'warning_signs': [
                'Aura (unusual sensations)',
                'Strange smells or tastes',
                'Visual disturbances',
                'Déjà vu feelings',
                'Sudden anxiety or fear',
                'Confusion or disorientation'
            ]
        }
    
    def chat(self, user_message: str) -> Dict:
        """Main chat method"""
        # Store message in history
        self.conversation_history.append({
            'role': 'user',
            'message': user_message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process message
        response = self.process_message(user_message)
        
        # Store response in history
        self.conversation_history.append({
            'role': 'assistant',
            'message': response['message'],
            'timestamp': datetime.now().isoformat()
        })
        
        return response
    
    def process_message(self, message: str) -> Dict:
        """Process user message and generate response"""
        message_lower = message.lower().strip()
        
        # Check patterns
        for pattern, handler in self.patterns.items():
            if re.search(pattern, message_lower):
                response_text = handler()
                return {
                    'message': response_text,
                    'intent': handler.__name__,
                    'confidence': 0.85
                }
        
        # Default response
        return {
            'message': self.respond_default(),
            'intent': 'unknown',
            'confidence': 0.5
        }
    
    # Response handlers
    def respond_greeting(self) -> str:
        return """Hello! I'm SeizureGuard AI Assistant. I'm here to help you with information about seizures and epilepsy.

I can help you with:
• Understanding seizures and epilepsy
• Recognizing symptoms and warning signs
• Emergency procedures and first aid
• Treatment options and lifestyle tips
• Safety precautions

How can I assist you today?"""
    
    def respond_seizure_info(self) -> str:
        return """**What is a Seizure?**

A seizure is a sudden, uncontrolled electrical disturbance in the brain. It can cause changes in behavior, movements, feelings, and levels of consciousness.

**What is Epilepsy?**
Epilepsy is a neurological disorder characterized by recurrent, unprovoked seizures. It affects people of all ages.

**Key Facts:**
• Seizures result from excessive electrical discharges in brain cells
• Not all seizures are epilepsy - single seizures can occur due to various causes
• Epilepsy is usually diagnosed after 2+ unprovoked seizures
• Many people with epilepsy can control seizures with medication

Would you like to know more about specific types of seizures or symptoms?"""
    
    def respond_symptoms(self) -> str:
        warning_signs = '\n'.join([f"• {sign}" for sign in self.knowledge['warning_signs']])
        
        return f"""**Seizure Warning Signs & Symptoms:**

**Pre-Seizure (Aura):**
{warning_signs}

**During Seizure:**
• Loss of consciousness
• Muscle stiffness or jerking
• Confusion or blank staring
• Uncontrollable movements
• Loss of bladder control

**After Seizure:**
• Confusion or disorientation
• Fatigue or sleepiness
• Headache
• Memory loss of the event

⚠️ If you're experiencing these symptoms, please consult a neurologist immediately."""
    
    def respond_emergency(self) -> str:
        return """🚨 **EMERGENCY SEIZURE RESPONSE:**

**Call 911 if:**
• Seizure lasts more than 5 minutes
• Person doesn't regain consciousness
• Second seizure follows immediately
• Person is injured, pregnant, or has diabetes
• Seizure occurs in water

**Immediate Actions:**
1. Stay calm and time the seizure
2. Protect from injury - clear the area
3. Turn person on their side (recovery position)
4. Cushion the head
5. Loosen tight clothing around neck

**DO NOT:**
❌ Restrain the person
❌ Put anything in their mouth
❌ Give food or water until fully alert

Stay with the person until they're fully conscious and oriented."""
    
    def respond_treatment(self) -> str:
        return """**Seizure Treatment Options:**

**Medications (Anti-Epileptic Drugs):**
• First-line treatment for most people
• 70% of people achieve seizure control with medication
• Common medications: Levetiracetam, Valproate, Carbamazepine

**Other Treatments:**
• Ketogenic Diet (high-fat, low-carb)
• Vagus Nerve Stimulation (VNS)
• Responsive Neurostimulation (RNS)
• Surgery (for drug-resistant epilepsy)

**Important:**
• Never stop medication without consulting your doctor
• Take medications as prescribed
• Regular follow-ups with neurologist are essential
• Report side effects immediately

💊 Treatment is individualized - what works varies by person."""
    
    def respond_prevention(self) -> str:
        triggers = '\n'.join([f"• {trigger}" for trigger in self.knowledge['common_triggers']])
        
        return f"""**Seizure Prevention & Trigger Management:**

**Common Triggers to Avoid:**
{triggers}

**Prevention Strategies:**
✓ Maintain regular sleep schedule (7-9 hours)
✓ Take medications consistently
✓ Manage stress through relaxation techniques
✓ Avoid alcohol and recreational drugs
✓ Stay hydrated and eat regularly
✓ Keep a seizure diary to identify personal triggers
✓ Wear medical alert identification

**Lifestyle Tips:**
• Exercise regularly (with precautions)
• Limit caffeine intake
• Use protective gear when needed
• Inform family, friends, and coworkers about your condition"""
    
    def respond_first_aid(self) -> str:
        return """**Seizure First Aid Guide:**

**During a Tonic-Clonic Seizure:**
1. ⏱️ Note the time - track duration
2. 🛡️ Protect from injury - move dangerous objects away
3. 🔄 Turn on side - helps breathing and prevents choking
4. 🛏️ Cushion head - use something soft
5. 👔 Loosen tight clothing - especially around neck
6. ⏳ Stay with them - until fully conscious

**During an Absence Seizure:**
• Guide away from danger
• Speak calmly and reassuringly
• Stay with them until awareness returns

**After the Seizure:**
• Check for injuries
• Allow them to rest
• Provide reassurance
• Don't offer food/drink until fully alert
• Stay until they're oriented

**When to Call 911:**
• Seizure > 5 minutes
• Multiple seizures without recovery
• First-time seizure
• Difficulty breathing
• Injury occurred
• Pregnant or has other medical conditions"""
    
    def respond_types(self) -> str:
        types = '\n'.join([f"• {t}" for t in self.knowledge['seizure_types']])
        
        return f"""**Types of Seizures:**

**Main Categories:**

**1. Generalized Seizures** (affect both sides of brain)
{types}

**2. Focal Seizures** (start in one area)
• Focal Aware (conscious)
• Focal Impaired Awareness (altered consciousness)

**Most Common Types:**

**Tonic-Clonic (Grand Mal):**
• Loss of consciousness
• Muscle stiffening and jerking
• Most recognizable type

**Absence (Petit Mal):**
• Brief loss of awareness
• Blank staring
• Common in children

Each type requires different management approaches. Consult a neurologist for proper diagnosis."""
    
    def respond_diagnosis(self) -> str:
        return """**Seizure Diagnosis & Testing:**

**Diagnostic Tests:**

**1. EEG (Electroencephalogram)** - Primary test
• Records brain's electrical activity
• Detects abnormal patterns
• May require multiple sessions

**2. Brain Imaging:**
• MRI - detailed brain structure
• CT Scan - quick assessment
• PET Scan - brain function

**3. Blood Tests:**
• Rule out other causes
• Check medication levels
• Assess overall health

**4. Video EEG Monitoring:**
• Extended recording (days)
• Captures seizure events
• Most comprehensive test

**Diagnosis Process:**
• Detailed medical history
• Description of seizure events
• Physical and neurological exam
• Multiple tests may be needed

Early diagnosis and treatment improve outcomes significantly."""
    
    def respond_lifestyle(self) -> str:
        return """**Living with Epilepsy - Lifestyle Guide:**

**Daily Life:**
✓ Maintain routine medication schedule
✓ Get adequate sleep consistently
✓ Manage stress effectively
✓ Stay physically active (with precautions)
✓ Eat balanced, regular meals

**Work & School:**
• Inform supervisors/teachers about your condition
• Know your rights under disability laws
• Request accommodations if needed
• Have an emergency action plan

**Social Life:**
• Educate friends and family
• Don't let epilepsy define you
• Join support groups
• Stay socially active

**Activities:**
• Swimming - always with supervision
• Driving - follow local laws (seizure-free period required)
• Sports - wear protective gear
• Avoid high-risk activities alone

**Mental Health:**
• Depression and anxiety are common - seek help
• Counseling can be beneficial
• Connect with epilepsy community

Remember: Many people with epilepsy live full, active lives!"""
    
    def respond_safety(self) -> str:
        return """**Safety Precautions for People with Epilepsy:**

**Home Safety:**
🏠 Bathroom:
• Use shower instead of bath
• Install grab bars
• Use plastic containers

🔥 Kitchen:
• Use microwave when possible
• Cook on back burners
• Use timer reminders

🛏️ Bedroom:
• Padded bed rails if needed
• Avoid top bunk beds
• Keep floor clear

**General Safety:**
• Wear medical alert bracelet/necklace
• Carry emergency contact information
• Inform close contacts about your condition
• Have a seizure action plan
• Keep rescue medication accessible (if prescribed)

**Activity Safety:**
• Avoid swimming alone
• Use protective gear for sports
• Be cautious with heights
• Avoid operating heavy machinery during high-risk periods

**Driving:**
• Follow local seizure-free requirements
• Report seizures to doctor
• Don't drive if seizures are uncontrolled

Safety measures help maintain independence while minimizing risks."""
    
    def respond_default(self) -> str:
        return """I'm here to help with seizure and epilepsy-related questions. 

I can provide information about:
• Seizure types and symptoms
• Emergency response and first aid
• Treatment options
• Prevention and trigger management
• Living with epilepsy
• Safety precautions

Please ask me a specific question, or type "help" for more options.

⚠️ Note: I provide information only. For medical advice, always consult a healthcare professional."""
    
    def get_conversation_history(self) -> List[Dict]:
        """Return conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


if __name__ == "__main__":
    # Test chatbot
    bot = SeizureChatbot()
    
    test_messages = [
        "Hello",
        "What is a seizure?",
        "What are the symptoms?",
        "Emergency help needed"
    ]
    
    for msg in test_messages:
        print(f"\nUser: {msg}")
        response = bot.chat(msg)
        print(f"Bot: {response['message'][:200]}...")
