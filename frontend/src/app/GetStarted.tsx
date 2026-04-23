import { motion } from 'motion/react';
import { useState } from 'react';
import { useNavigate } from 'react-router';
import { useCurrentUser } from '@/context/CurrentUser';

const goals = [
  { id: 'strength', label: 'Build Strength', desc: 'Focus on progressive overload and compound lifts' },
  { id: 'muscle', label: 'Build Muscle', desc: 'Hypertrophy-focused training with volume tracking' },
  { id: 'endurance', label: 'Improve Endurance', desc: 'Conditioning and high-rep training programs' },
  { id: 'general', label: 'Stay Active', desc: 'Maintain fitness with flexible, balanced routines' },
];

const experienceLevels = [
  { id: 'beginner', label: 'Beginner', desc: 'New to lifting or less than 6 months' },
  { id: 'intermediate', label: 'Intermediate', desc: '6 months to 2 years of consistent training' },
  { id: 'advanced', label: 'Advanced', desc: '2+ years of structured training' },
];

const daysOptions = [2, 3, 4, 5, 6];

export default function GetStarted() {
  const navigate = useNavigate();
  const { register } = useCurrentUser();
  const [step, setStep] = useState(0);
  const [selectedGoal, setSelectedGoal] = useState<string | null>(null);
  const [selectedLevel, setSelectedLevel] = useState<string | null>(null);
  const [selectedDays, setSelectedDays] = useState<number | null>(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalSteps = 4;

  const canProceed = () => {
    if (step === 0) return name.trim().length > 0 && email.trim().length > 0 && password.length >= 6;
    if (step === 1) return selectedGoal !== null;
    if (step === 2) return selectedLevel !== null;
    if (step === 3) return selectedDays !== null;
    return false;
  };

  const handleFinish = async () => {
    setSubmitting(true);
    setError(null);
    try {
      await register({ email: email.trim(), password });
      navigate('/feed');
    } catch (err) {
      const detail = (err as any)?.body?.detail;
      setError(detail ?? (err instanceof Error ? err.message : 'Registration failed. Please try again.'));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="size-full bg-white overflow-y-auto relative min-h-screen">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-black/5">
        <div className="px-4 py-3 flex items-center justify-between">
          <button
            onClick={() => step > 0 ? setStep(step - 1) : navigate('/')}
            className="text-sm text-black/60 active:text-black transition-colors"
          >
            {step > 0 ? '← Back' : '← Home'}
          </button>
          <div className="text-lg tracking-tight text-black">SPOTTER</div>
          <div className="w-12" />
        </div>
      </nav>

      {/* Progress Bar */}
      <div className="fixed top-[53px] left-0 right-0 z-50 h-[2px] bg-black/5">
        <motion.div
          className="h-full bg-black"
          animate={{ width: `${((step + 1) / totalSteps) * 100}%` }}
          transition={{ duration: 0.4, ease: 'easeInOut' }}
        />
      </div>

      {/* Content */}
      <div className="pt-24 pb-32 px-6 flex flex-col items-center">
        {/* Step 0: Name */}
        {step === 0 && (
          <motion.div
            key="name"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -30 }}
            transition={{ duration: 0.4 }}
            className="w-full max-w-sm space-y-8"
          >
            <div className="space-y-3 text-center">
              <h1 className="text-3xl tracking-tight text-black">Let's get you set up</h1>
              <p className="text-base text-black/60">Create your account to get started.</p>
            </div>
            <div className="space-y-3">
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your name"
                className="w-full px-6 py-4 bg-black/5 rounded-full text-black placeholder:text-black/30 outline-none focus:ring-2 focus:ring-black/20 transition-all text-center text-lg"
                autoFocus
              />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email address"
                className="w-full px-6 py-4 bg-black/5 rounded-full text-black placeholder:text-black/30 outline-none focus:ring-2 focus:ring-black/20 transition-all text-center text-lg"
              />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password (6+ characters)"
                className="w-full px-6 py-4 bg-black/5 rounded-full text-black placeholder:text-black/30 outline-none focus:ring-2 focus:ring-black/20 transition-all text-center text-lg"
              />
            </div>
          </motion.div>
        )}

        {/* Step 1: Goal */}
        {step === 1 && (
          <motion.div
            key="goal"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -30 }}
            transition={{ duration: 0.4 }}
            className="w-full max-w-sm space-y-8"
          >
            <div className="space-y-3 text-center">
              <h1 className="text-3xl tracking-tight text-black">
                {name ? `Hey ${name},` : 'Hey,'} what's your goal?
              </h1>
              <p className="text-base text-black/60">We'll tailor your experience.</p>
            </div>
            <div className="space-y-3">
              {goals.map((goal, i) => (
                <motion.button
                  key={goal.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: i * 0.08 }}
                  onClick={() => setSelectedGoal(goal.id)}
                  className={`w-full text-left px-5 py-4 rounded-2xl border transition-all active:scale-[0.98] ${
                    selectedGoal === goal.id
                      ? 'bg-black text-white border-black'
                      : 'bg-white text-black border-black/10 hover:border-black/30'
                  }`}
                >
                  <div className="text-base font-medium">{goal.label}</div>
                  <div className={`text-sm mt-1 ${selectedGoal === goal.id ? 'text-white/60' : 'text-black/50'}`}>
                    {goal.desc}
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Step 2: Experience */}
        {step === 2 && (
          <motion.div
            key="experience"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -30 }}
            transition={{ duration: 0.4 }}
            className="w-full max-w-sm space-y-8"
          >
            <div className="space-y-3 text-center">
              <h1 className="text-3xl tracking-tight text-black">Experience level?</h1>
              <p className="text-base text-black/60">No wrong answers here.</p>
            </div>
            <div className="space-y-3">
              {experienceLevels.map((level, i) => (
                <motion.button
                  key={level.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: i * 0.08 }}
                  onClick={() => setSelectedLevel(level.id)}
                  className={`w-full text-left px-5 py-4 rounded-2xl border transition-all active:scale-[0.98] ${
                    selectedLevel === level.id
                      ? 'bg-black text-white border-black'
                      : 'bg-white text-black border-black/10 hover:border-black/30'
                  }`}
                >
                  <div className="text-base font-medium">{level.label}</div>
                  <div className={`text-sm mt-1 ${selectedLevel === level.id ? 'text-white/60' : 'text-black/50'}`}>
                    {level.desc}
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        )}

        {/* Step 3: Days per week */}
        {step === 3 && (
          <motion.div
            key="days"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -30 }}
            transition={{ duration: 0.4 }}
            className="w-full max-w-sm space-y-8"
          >
            <div className="space-y-3 text-center">
              <h1 className="text-3xl tracking-tight text-black">Days per week?</h1>
              <p className="text-base text-black/60">How often can you train?</p>
            </div>
            <div className="flex justify-center gap-3">
              {daysOptions.map((day, i) => (
                <motion.button
                  key={day}
                  initial={{ opacity: 0, scale: 0.8 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: i * 0.06 }}
                  onClick={() => setSelectedDays(day)}
                  className={`w-14 h-14 rounded-full text-lg transition-all active:scale-90 ${
                    selectedDays === day
                      ? 'bg-black text-white'
                      : 'bg-black/5 text-black hover:bg-black/10'
                  }`}
                >
                  {day}
                </motion.button>
              ))}
            </div>
            {selectedDays && (
              <motion.p
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center text-sm text-black/50"
              >
                {selectedDays} days per week — {selectedDays <= 3 ? 'quality over quantity.' : selectedDays <= 5 ? 'solid commitment.' : 'beast mode.'}
              </motion.p>
            )}
          </motion.div>
        )}
      </div>

      {/* Bottom CTA */}
      <div className="fixed bottom-0 left-0 right-0 z-50 p-4 bg-white/95 backdrop-blur-md border-t border-black/5">
        {error && (
          <p className="text-red-500 text-sm text-center mb-2">{error}</p>
        )}
        <motion.button
          whileTap={{ scale: 0.97 }}
          onClick={() => {
            if (step < totalSteps - 1) {
              setStep(step + 1);
            } else {
              handleFinish();
            }
          }}
          disabled={!canProceed() || submitting}
          className={`w-full px-6 py-4 rounded-full text-base transition-all ${
            canProceed() && !submitting
              ? 'bg-black text-white active:scale-95'
              : 'bg-black/10 text-black/30 cursor-not-allowed'
          }`}
        >
          {submitting ? 'Setting up...' : step < totalSteps - 1 ? 'Continue' : 'Let\'s Go'}
        </motion.button>
      </div>
    </div>
  );
}