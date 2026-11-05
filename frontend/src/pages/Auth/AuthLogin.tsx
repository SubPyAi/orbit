import Nav from './LocalComponents/Nav/Nav.tsx';
import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';
import './AuthLogin.css';
import Button from '../../GlobalComponents/Button/Button.tsx';
import TextField from '../../GlobalComponents/TextField/TextField.tsx';
import { motion } from 'motion/react';
import { useState } from 'react';
import { toast } from 'sonner';

function AuthLogin(  { onLoginClick, onRegisterClick }: { onLoginClick: (username: string, password: string) => void, onRegisterClick: () => void }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [usernameError, setUsernameError] = useState(false);
    const [passwordError, setPasswordError] = useState(false);
    
    const handleLogin = () => {
        if (username === "") {
            toast.warning("Username cannot be empty!")
            setUsernameError(true)
        }
        else if (password === "") {
            toast.warning("Password cannot be empty!")
            setPasswordError(true)
        }
        else {
            onLoginClick(username, password)
        }
    };
    
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
                    <p className="auth-subtitle">Please sign in to continue</p>
                    <TextField label="Username" hasError={usernameError} onChange={(e) => {setUsername(e.target.value)}} placeholder="Enter your username" className="auth-text-field" />
                    <TextField label="Password" hasError={passwordError} onChange={(e) => {setPassword(e.target.value)}} placeholder="Enter your password" type="password" className="auth-text-field" />
                    <div className="auth-forgot-password">
                        <Button className="auth-forgot-password-button" variant="ghost">
                            Forgot Password?
                        </Button>
                    </div>
                    <div className="auth-actions">
                        <Button className="auth-signin-button" onClick={handleLogin} variant="primary">
                            Sign In
                        </Button>
                        <Button className="auth-signup-button" onClick={onRegisterClick} variant="secondary">
                            Register
                        </Button>
                    </div>
                </div>
            </GlassPanel>
        </div>
    </motion.div>
}

export default AuthLogin;