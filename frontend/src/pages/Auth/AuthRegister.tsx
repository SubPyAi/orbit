import Nav from './LocalComponents/Nav/Nav.tsx';
import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';
import './AuthRegister.css';
import Button from '../../GlobalComponents/Button/Button.tsx';
import TextField from '../../GlobalComponents/TextField/TextField.tsx';
import { motion } from 'motion/react';

function AuthRegister(  { onLoginClick }: { onLoginClick: () => void }) {
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
                    <p className="auth-subtitle">Please sign up to continue</p>
                    <TextField label="Email" placeholder="Enter your email" className="auth-text-field" />
                    <TextField label="Password" placeholder="Enter your password" type="password" className="auth-text-field" />
                    <div className="auth-forgot-password">
                        <Button className="auth-forgot-password-button" variant="ghost">
                            Forgot Password?
                        </Button>
                    </div>
                    <div className="auth-actions">
                        <Button className="auth-signin-button" onClick={onLoginClick} variant="primary">
                            Sign In
                        </Button>
                        <Button className="auth-signup-button" variant="secondary">
                            Register
                        </Button>
                    </div>
                </div>
            </GlassPanel>
        </div>
    </motion.div>
}

export default AuthRegister;