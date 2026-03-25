import { ImageWithFallback } from './components/figma/ImageWithFallback';
import { motion, useScroll, useTransform } from 'motion/react';
import { useRef } from 'react';
import { useNavigate } from 'react-router';

export default function App() {
  const navigate = useNavigate();
  const containerRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start start", "end end"]
  });

  const heroY = useTransform(scrollYProgress, [0, 0.3], [0, -100]);
  const heroOpacity = useTransform(scrollYProgress, [0, 0.2], [1, 0]);
  
  return (
    <div ref={containerRef} className="size-full bg-white overflow-y-auto relative">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-white/95 backdrop-blur-md border-b border-black/5">
        <div className="px-4 py-3 flex items-center justify-between">
          <div className="text-lg tracking-tight text-black">SPOTTER</div>
          <button onClick={() => navigate('/get-started')} className="px-5 py-2 bg-black text-white text-sm rounded-full active:scale-95 transition-transform">
            Start
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="min-h-screen flex flex-col items-center justify-center px-4 pt-16 pb-8 relative overflow-hidden">
        <motion.div 
          style={{ y: heroY, opacity: heroOpacity }}
          className="w-full text-center space-y-6"
        >
          <h1 className="text-[2.5rem] leading-[1.1] tracking-tight text-black">
            Strength in<br />Simplicity
          </h1>
          <p className="text-base text-black/60 px-4">
            A minimalist approach to building your strongest self. Track, train, and transform.
          </p>
          <div className="flex flex-col gap-3 pt-4 px-4">
            <button onClick={() => navigate('/get-started')} className="w-full px-6 py-4 bg-black text-white rounded-full active:scale-95 transition-transform">
              Get Started
            </button>
            <button onClick={() => navigate('/learn-more')} className="w-full px-6 py-4 border border-black text-black rounded-full active:scale-95 transition-transform">
              Learn More
            </button>
          </div>
        </motion.div>
        
        {/* Decorative accent */}
        <motion.div 
          style={{ 
            y: useTransform(scrollYProgress, [0, 0.3], [0, 150]),
            opacity: useTransform(scrollYProgress, [0, 0.2], [0.05, 0])
          }}
          className="absolute -bottom-40 left-1/2 -translate-x-1/2 w-96 h-96 bg-black/5 rounded-full blur-3xl"
        />
      </section>

      {/* Image Section 1 */}
      <section className="px-4 py-12">
        <motion.div 
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-100px" }}
          transition={{ duration: 0.6 }}
          className="w-full"
        >
          <motion.div 
            style={{ 
              y: useTransform(scrollYProgress, [0.15, 0.35], [50, -50])
            }}
            className="aspect-[4/3] w-full overflow-hidden rounded-xl"
          >
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1567813600887-8cc1bae6fa87?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxkdW1iYmVsbCUyMG1pbml0YWwlMjBhZXN0aGV0aWN8ZW58MXx8fHwxNzcwODY1MDgxfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
              alt="Minimal dumbbell aesthetic"
              className="w-full h-full object-cover"
            />
          </motion.div>
        </motion.div>
      </section>

      {/* Feature Section */}
      <section className="px-4 py-16 bg-black text-white relative overflow-hidden">
        {/* Accent background */}
        <motion.div 
          style={{ 
            y: useTransform(scrollYProgress, [0.3, 0.5], [100, -100])
          }}
          className="absolute top-0 right-0 w-64 h-64 bg-white/5 rounded-full blur-3xl"
        />
        
        <div className="w-full space-y-10 relative z-10">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.5 }}
            className="text-center space-y-3"
          >
            <h2 className="text-3xl tracking-tight">
              Built for Focus
            </h2>
            <p className="text-base text-white/60 px-4">
              Every detail designed to keep you on track. No distractions, just results.
            </p>
          </motion.div>

          <div className="space-y-8">
            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="space-y-3"
            >
              <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                <div className="w-5 h-5 bg-white rounded-full"></div>
              </div>
              <h3 className="text-lg">Track Simply</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Log your sets, reps, and weight with minimal friction. Get in, train, get out.
              </p>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="space-y-3"
            >
              <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                <div className="w-5 h-5 bg-white rounded-full"></div>
              </div>
              <h3 className="text-lg">Progress Clearly</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                See your strength gains visualized in clean, intuitive charts.
              </p>
            </motion.div>

            <motion.div 
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="space-y-3"
            >
              <div className="w-10 h-10 bg-white/10 rounded-full flex items-center justify-center">
                <div className="w-5 h-5 bg-white rounded-full"></div>
              </div>
              <h3 className="text-lg">Train Focused</h3>
              <p className="text-sm text-white/60 leading-relaxed">
                Minimal interface means maximum concentration on what matters: lifting.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Image Section 2 */}
      <section className="px-4 py-12">
        <div className="w-full space-y-4">
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            style={{ 
              y: useTransform(scrollYProgress, [0.5, 0.7], [30, -30])
            }}
            className="aspect-square overflow-hidden rounded-xl"
          >
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1709315872247-644b7ff5ed10?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxiYXJiZWxsJTIwZ3ltJTIwbWluaW1hbHxlbnwxfHx8fDE3NzA4NjUwODF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
              alt="Barbell minimal"
              className="w-full h-full object-cover"
            />
          </motion.div>
          <motion.div 
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            style={{ 
              y: useTransform(scrollYProgress, [0.5, 0.7], [50, -50])
            }}
            className="aspect-square overflow-hidden rounded-xl"
          >
            <ImageWithFallback
              src="https://images.unsplash.com/photo-1614236224416-9a88c2e195e1?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxmaXRuZXNzJTIwd29ya291dCUyMGJsYWNrJTIwd2hpdGV8ZW58MXx8fHwxNzcwODY1MDgyfDA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral"
              alt="Fitness workout"
              className="w-full h-full object-cover"
            />
          </motion.div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="px-4 py-16 relative overflow-hidden">
        {/* Accent */}
        <motion.div 
          style={{ 
            y: useTransform(scrollYProgress, [0.65, 0.8], [50, -50])
          }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-black/3 rounded-full blur-3xl"
        />
        
        <motion.div 
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="w-full relative z-10"
        >
          <div className="grid grid-cols-2 gap-6">
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="text-center space-y-1"
            >
              <div className="text-3xl text-black">10K+</div>
              <div className="text-xs text-black/60">Athletes</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="text-center space-y-1"
            >
              <div className="text-3xl text-black">50M+</div>
              <div className="text-xs text-black/60">Reps Logged</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="text-center space-y-1"
            >
              <div className="text-3xl text-black">100%</div>
              <div className="text-xs text-black/60">Ad-Free</div>
            </motion.div>
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="text-center space-y-1"
            >
              <div className="text-3xl text-black">4.9</div>
              <div className="text-xs text-black/60">Rating</div>
            </motion.div>
          </div>
        </motion.div>
      </section>

      {/* CTA Section */}
      <section className="px-4 py-20 bg-black text-white relative overflow-hidden">
        {/* Animated background elements */}
        <motion.div 
          style={{ 
            y: useTransform(scrollYProgress, [0.8, 1], [0, -80])
          }}
          className="absolute top-10 right-10 w-32 h-32 bg-white/5 rounded-full blur-2xl"
        />
        <motion.div 
          style={{ 
            y: useTransform(scrollYProgress, [0.8, 1], [0, 80])
          }}
          className="absolute bottom-10 left-10 w-40 h-40 bg-white/5 rounded-full blur-2xl"
        />
        
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="w-full text-center space-y-6 relative z-10"
        >
          <h2 className="text-3xl tracking-tight leading-tight">
            Ready to start<br />your journey?
          </h2>
          <p className="text-base text-white/80 px-4">
            Join thousands of athletes who've simplified their training.
          </p>
          <button onClick={() => navigate('/get-started')} className="w-full max-w-xs mx-auto px-8 py-4 bg-white text-black rounded-full active:scale-95 transition-transform">
            Download Now
          </button>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="px-4 py-10 bg-white border-t border-black/5">
        <div className="w-full">
          <div className="flex flex-col items-center gap-6">
            <div className="text-lg tracking-tight text-black">SPOTTER</div>
            <div className="flex gap-6 text-sm text-black/60">
              <a href="#" className="active:text-black transition-colors">About</a>
              <a href="#" className="active:text-black transition-colors">Features</a>
              <a href="#" className="active:text-black transition-colors">Privacy</a>
              <a href="#" className="active:text-black transition-colors">Contact</a>
            </div>
          </div>
          <div className="mt-6 text-center text-xs text-black/40">
            © 2026 Spotter. All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  );
}