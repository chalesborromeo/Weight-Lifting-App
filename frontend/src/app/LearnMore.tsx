import { motion, useScroll, useTransform } from 'motion/react';
import { useRef } from 'react';
import { useNavigate } from 'react-router';
import { ThemeToggle } from '@/components/ThemeToggle';

const willDo = [
  { title: 'Log & Track Activities', desc: 'Log and track your athletic activities with location-based features tailored for the Bloomington-Normal area.' },
  { title: 'Create Groups & Clubs', desc: 'Based on your interests, create groups and clubs of varying sizes to find like-minded athletes and build your community.' },
  { title: 'Share Highlights & PRs', desc: 'Post highlights of your workouts and personal records for other users to celebrate and get inspired by.' },
  { title: 'Follow Athletes', desc: 'Follow other athletes and browse activity feeds to stay connected with your fitness circle.' },
  { title: 'Discover Nearby Gyms', desc: 'Access an integrated map of nearby gyms so you always know where to train.' },
  { title: 'Media Postings', desc: 'Share photos and videos of your workouts to showcase your progress and motivate others.' },
];

const wontDo = [
  'Integrate with third-party devices and apps (e.g. Garmin, Fitbit, Apple Watch)',
  'Track nutrition, calories, or dietary information',
  'Function as a general social media platform with non-fitness content',
  'Provide real-time GPS route tracking during workouts',
  'Offer paid subscription tiers or premium features',
];

const glossary = [
  { term: 'Spotter', def: 'A gym partner who provides assistance, motivation, or safety during workouts.' },
  { term: 'User', def: 'Any registered individual who accesses the Spotter application.' },
  { term: 'Workout Log', def: 'A recorded exercise session containing details such as exercises performed, duration, and date.' },
  { term: 'Activity Feed', def: 'A chronological display of posts and updates from users that a person follows.' },
  { term: 'Group / Club', def: 'A user-created community within Spotter organized around shared fitness interests.' },
  { term: 'Personal Record (PR)', def: "A user's best performance in a specific exercise or activity." },
  { term: 'Post', def: 'User-generated content including text, photos, or videos shared to the activity feed.' },
  { term: 'Profile', def: 'A personal page displaying stats, PRs, groups/clubs, and other info the user chooses to share.' },
];

export default function LearnMore() {
  const navigate = useNavigate();
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  return (
    <div ref={containerRef} className="size-full bg-background overflow-y-auto relative">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-background/95 backdrop-blur-md border-b border-border">
        <div className="px-4 py-3 flex items-center justify-between">
          <button
            onClick={() => navigate('/')}
            className="text-sm text-muted-foreground active:text-foreground transition-colors"
          >
            ← Home
          </button>
          <div className="text-lg tracking-tight text-foreground">SPOTTER</div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <button
              onClick={() => navigate('/get-started')}
              className="px-5 py-2 bg-accent text-white text-sm rounded-full active:scale-95 transition-transform"
            >
              Start
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="min-h-[70vh] flex flex-col items-center justify-center px-6 pt-20 pb-12 relative overflow-hidden">
        <motion.div
          style={{
            y: useTransform(scrollYProgress, [0, 0.15], [0, -60]),
            opacity: useTransform(scrollYProgress, [0, 0.12], [1, 0])
          }}
          className="w-full max-w-lg text-center space-y-6"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-block px-4 py-1.5 bg-card rounded-full text-xs text-muted-foreground mb-6">
              Everything you need to know
            </div>
          </motion.div>
          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="text-[2.5rem] leading-[1.1] tracking-tight text-foreground"
          >
            Your Fitness<br />Community,<br />Simplified
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="text-base text-muted-foreground px-2"
          >
            Spotter motivates athletes through social accountability, friendly competition, and the backing of a real fitness community.
          </motion.p>
        </motion.div>

        <motion.div
          style={{
            y: useTransform(scrollYProgress, [0, 0.2], [0, 100]),
            opacity: useTransform(scrollYProgress, [0, 0.15], [0.05, 0])
          }}
          className="absolute -bottom-32 left-1/2 -translate-x-1/2 w-96 h-96 bg-accent/5 rounded-full blur-3xl"
        />
      </section>

      {/* What Spotter Does */}
      <section className="px-4 py-16 bg-card relative overflow-hidden">
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.1, 0.35], [80, -80]) }}
          className="absolute top-0 right-0 w-64 h-64 bg-accent/5 rounded-full blur-3xl"
        />
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.15, 0.4], [100, -60]) }}
          className="absolute bottom-0 left-0 w-48 h-48 bg-accent/5 rounded-full blur-3xl"
        />

        <div className="w-full max-w-lg mx-auto space-y-10 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-3"
          >
            <h2 className="text-3xl tracking-tight text-foreground">What Spotter Does</h2>
            <p className="text-base text-muted-foreground px-4">
              Built for athletes who want more than just a workout tracker.
            </p>
          </motion.div>

          <div className="space-y-6">
            {willDo.map((item, i) => (
              <motion.div
                key={item.title}
                initial={{ opacity: 0, x: -30 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
                className="flex gap-4 items-start"
              >
                <div className="mt-1 w-8 h-8 shrink-0 bg-accent/10 rounded-full flex items-center justify-center">
                  <div className="w-3 h-3 bg-accent rounded-full" />
                </div>
                <div className="space-y-1">
                  <h3 className="text-base font-medium text-foreground">{item.title}</h3>
                  <p className="text-sm text-muted-foreground leading-relaxed">{item.desc}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* What Spotter Won't Do */}
      <section className="px-4 py-16 relative overflow-hidden">
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.35, 0.55], [50, -50]) }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-accent/3 rounded-full blur-3xl"
        />

        <div className="w-full max-w-lg mx-auto space-y-10 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-3"
          >
            <h2 className="text-3xl tracking-tight text-foreground">Focused by Design</h2>
            <p className="text-base text-muted-foreground px-4">
              We intentionally leave out things that dilute the experience.
            </p>
          </motion.div>

          <div className="space-y-4">
            {wontDo.map((item, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: i * 0.08 }}
                className="flex gap-3 items-start px-5 py-4 bg-card rounded-[20px]"
              >
                <span className="text-muted-foreground text-lg mt-[-2px]">—</span>
                <p className="text-sm text-muted-foreground leading-relaxed">{item}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Product Perspective */}
      <section className="px-4 py-16 bg-card relative overflow-hidden">
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.5, 0.7], [60, -60]) }}
          className="absolute top-10 right-10 w-40 h-40 bg-accent/5 rounded-full blur-2xl"
        />

        <div className="w-full max-w-lg mx-auto space-y-12 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-3"
          >
            <h2 className="text-3xl tracking-tight text-foreground">The Vision</h2>
            <p className="text-base text-muted-foreground px-2 leading-relaxed">
              Spotter is a standalone, independent mobile app. It differentiates itself by letting users share workouts, post photo and video media, and access map integrations to discover local gyms.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="space-y-4"
          >
            <h3 className="text-lg text-center text-foreground">Built for Everyone</h3>
            <p className="text-sm text-muted-foreground text-center leading-relaxed px-2">
              Any education level. Any fitness level. If you can open an app, you can use Spotter. It's designed for anyone who wants to start, track, or share their fitness journey.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="space-y-4"
          >
            <h3 className="text-lg text-center text-foreground">Cross-Platform</h3>
            <div className="grid grid-cols-2 gap-3">
              {[
                { label: 'iOS & Android', sub: 'React Native + TypeScript' },
                { label: 'Backend', sub: 'Python' },
                { label: 'Database', sub: 'PostgreSQL' },
                { label: 'Maps', sub: 'Google Maps & Apple Maps' },
              ].map((item, i) => (
                <motion.div
                  key={item.label}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.3, delay: 0.3 + i * 0.08 }}
                  className="bg-background rounded-[20px] p-4 text-center space-y-1"
                >
                  <div className="text-sm font-medium text-foreground">{item.label}</div>
                  <div className="text-xs text-muted-foreground">{item.sub}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>
        </div>
      </section>

      {/* Glossary */}
      <section className="px-4 py-16 relative overflow-hidden">
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.7, 0.85], [40, -40]) }}
          className="absolute top-1/2 right-0 w-60 h-60 bg-accent/3 rounded-full blur-3xl"
        />

        <div className="w-full max-w-lg mx-auto space-y-10 relative z-10">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-3"
          >
            <h2 className="text-3xl tracking-tight text-foreground">Key Terms</h2>
            <p className="text-base text-muted-foreground">
              The language of Spotter.
            </p>
          </motion.div>

          <div className="space-y-3">
            {glossary.map((item, i) => (
              <motion.div
                key={item.term}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.3, delay: i * 0.05 }}
                className="px-5 py-4 bg-card rounded-[20px] space-y-1"
              >
                <div className="text-sm font-medium text-foreground">{item.term}</div>
                <div className="text-sm text-muted-foreground leading-relaxed">{item.def}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="px-4 py-20 bg-card relative overflow-hidden">
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.85, 1], [0, -60]) }}
          className="absolute top-10 right-10 w-32 h-32 bg-accent/5 rounded-full blur-2xl"
        />
        <motion.div
          style={{ y: useTransform(scrollYProgress, [0.85, 1], [0, 60]) }}
          className="absolute bottom-10 left-10 w-40 h-40 bg-accent/5 rounded-full blur-2xl"
        />

        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="w-full max-w-lg mx-auto text-center space-y-6 relative z-10"
        >
          <h2 className="text-3xl tracking-tight leading-tight text-foreground">
            Ready to find<br />your community?
          </h2>
          <p className="text-base text-muted-foreground px-4">
            Join athletes in Bloomington-Normal who are building something together.
          </p>
          <button
            onClick={() => navigate('/get-started')}
            className="w-full max-w-xs mx-auto px-8 py-4 bg-accent text-white rounded-full active:scale-95 transition-transform"
          >
            Get Started
          </button>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="px-4 py-10 bg-background border-t border-border">
        <div className="w-full max-w-lg mx-auto">
          <div className="flex flex-col items-center gap-6">
            <div className="text-lg tracking-tight text-foreground">SPOTTER</div>
            <div className="flex gap-6 text-sm text-muted-foreground">
              <button onClick={() => navigate('/')} className="active:text-foreground transition-colors">Home</button>
              <button onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} className="active:text-foreground transition-colors">Back to Top</button>
              <button onClick={() => navigate('/get-started')} className="active:text-foreground transition-colors">Get Started</button>
            </div>
          </div>
          <div className="mt-6 text-center text-xs text-muted-foreground">
            &copy; 2026 Spotter. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}
