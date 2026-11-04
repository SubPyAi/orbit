import AuthLogin from './AuthLogin.tsx';
import AuthRegister from './AuthRegister.tsx';
import Nav from './LocalComponents/Nav/Nav.tsx';

import { useState } from 'react';
import { AnimatePresence, motion } from 'motion/react';

import "./Auth.css"

function Auth() {
    const [authMode, setAuthMode] = useState<'login' | 'register'>('login');

    return <div className="auth-page">
        <Nav />
        <AnimatePresence mode="wait">
            {authMode === 'login' ? (
            <AuthLogin key="login" onRegisterClick={() => setAuthMode('register')} />
        ) : (
            <AuthRegister key="register" onLoginClick={() => setAuthMode('login')} />
        )}
        </AnimatePresence>
    </div>
}

export default Auth;