import { motion } from 'motion/react';
import { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import { useCurrentUser } from '@/context/CurrentUser';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useCurrentUser();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const canSubmit = email.trim().length > 0 && password.length > 0;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await login({ email: email.trim(), password });
      navigate('/feed');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-sm space-y-8"
      >
        <div className="text-center space-y-2">
          <h1 className="text-3xl tracking-tight text-black">SPOTTER</h1>
          <p className="text-base text-black/60">Welcome back.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email address"
            className="w-full px-6 py-4 bg-black/5 rounded-full text-black placeholder:text-black/30 outline-none focus:ring-2 focus:ring-black/20 transition-all text-center text-lg"
            autoFocus
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full px-6 py-4 bg-black/5 rounded-full text-black placeholder:text-black/30 outline-none focus:ring-2 focus:ring-black/20 transition-all text-center text-lg"
          />

          {error && (
            <p className="text-red-500 text-sm text-center">{error}</p>
          )}

          <motion.button
            whileTap={{ scale: 0.97 }}
            type="submit"
            disabled={!canSubmit || submitting}
            className={`w-full px-6 py-4 rounded-full text-base transition-all ${
              canSubmit && !submitting
                ? 'bg-black text-white active:scale-95'
                : 'bg-black/10 text-black/30 cursor-not-allowed'
            }`}
          >
            {submitting ? 'Signing in...' : 'Sign In'}
          </motion.button>
        </form>

        <p className="text-center text-sm text-black/50">
          Don't have an account?{' '}
          <Link to="/get-started" className="text-black underline">
            Get Started
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
