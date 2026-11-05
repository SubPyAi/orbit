import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';
import './AuthRegister.css';
import Button from '../../GlobalComponents/Button/Button.tsx';
import TextField from '../../GlobalComponents/TextField/TextField.tsx';
import { motion } from 'motion/react';
import { toast } from 'sonner';
import React from 'react';

function AuthRegister(  { onNext, onLoginClick }: { onNext: (email: string, password: string) => void; onLoginClick: () => void }) {
    const [email, setEmail] = React.useState('');
    const [password, setPassword] = React.useState('');

    const handleNextClick = () => {
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        if (email === "") {
            toast.warning("Email Field cannot be empty!")
        }
        else if (!emailRegex.test(email)) {
            toast.warning("Email not in valid format!")
        }
        else if (password === "") {
            toast.warning("Password Field cannot be empty!")
        }
        else if (password.length < 8) {
            toast.warning("Password must be atleast 8 characters!")
        }
        else {
            onNext(email, password);
        }
    }

    return <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.25 }}
    >
        <div className="auth-content">
            <GlassPanel intensity="subtle" className="auth-glass-panel">
                <div className="auth-glass-panel-content">
                    <h1 className="auth-title">Welcome to Orbit</h1>
                    <p className="auth-subtitle">Your universe of connections</p>
                    <TextField id="reg-email" label="Email" placeholder="Enter your email" className="auth-text-field" onChange={(e) => setEmail(e.target.value)} />
                    <TextField label="Password" placeholder="Enter your password" type="password" className="auth-text-field" onChange={(e) => setPassword(e.target.value)} />
                    <div className="auth-actions">
                        <Button className="auth-signin-button" onClick={onLoginClick} variant="secondary">
                            Sign In
                        </Button>
                        <Button className="auth-signup-button" variant="primary" onClick={handleNextClick}>
                            Next
                        </Button>
                    </div>
                </div>
            </GlassPanel>
        </div>
    </motion.div>
}

export default AuthRegister;