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
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="w-full max-w-sm space-y-8"
      >
        <div className="text-center space-y-2">
          <h1 className="text-3xl tracking-tight text-foreground">SPOTTER</h1>
          <p className="text-base text-muted-foreground">Welcome back.</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-3">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="Email address"
            className="w-full px-6 py-4 bg-card rounded-[15px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30 transition-all text-center text-lg"
            autoFocus
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            className="w-full px-6 py-4 bg-card rounded-[15px] text-foreground placeholder:text-muted-foreground outline-none focus:ring-2 focus:ring-accent/30 transition-all text-center text-lg"
          />

          {error && (
            <p className="text-destructive text-sm text-center">{error}</p>
          )}

          <motion.button
            whileTap={{ scale: 0.97 }}
            type="submit"
            disabled={!canSubmit || submitting}
            className={`w-full px-6 py-4 rounded-[15px] text-base transition-all ${
              canSubmit && !submitting
                ? 'bg-accent text-white active:scale-95'
                : 'bg-inactive text-muted-foreground cursor-not-allowed'
            }`}
          >
            {submitting ? 'Signing in...' : 'Sign In'}
          </motion.button>
        </form>

        <p className="text-center text-sm text-muted-foreground">
          Don't have an account?{' '}
          <Link to="/get-started" className="text-accent underline">
            Get Started
          </Link>
        </p>
      </motion.div>
    </div>
  );
}
