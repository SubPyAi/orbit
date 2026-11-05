import AuthLogin from './AuthLogin.tsx';
import AuthRegister from './AuthRegister.tsx';
import AuthRegister1 from './AuthRegister1.tsx';
import AuthRegister2 from './AuthRegister2.tsx';
import Nav from './LocalComponents/Nav/Nav.tsx';

import { useState } from 'react';
import { AnimatePresence } from 'motion/react';

import "./Auth.css"
import { SendCreateUserReq, SendLoginReq } from "../../orbit-backend-handler/api.tsx";
import { toast } from 'sonner';

function Auth() {
    const [authMode, setAuthMode] = useState<'login' | 'register' | 'forgot' | 'register1' | 'register2'>('login');

    const [userRegData, setUserRegData] = useState({
        email: '',
        password: '',
        username: '',
        DoB: '',
        pfp_ref: '',
        phone: '',
    });

    const regHandler01 = (email: string, password: string) => {
        setUserRegData(prev => ({
            ...prev,
            email: email,
            password: password
        }))
        setAuthMode('register1');
    }

    const onBack = () => {
        setAuthMode('register');
    }

    const regHandler12 = (name:  string, DoB: string) => {
        setUserRegData(prev => ({
            ...prev,
            username: name,
            DoB: DoB
        }))
        setAuthMode('register2');
    };

    const onBack1 = () => {
        setAuthMode('register1');
    }

    const regHandler23 = async (pfp_ref="") => {
        setUserRegData(prev => ({
            ...prev,
            pfp_ref: pfp_ref
        }))
        const accToast = toast.loading("Registering your details...")
        setTimeout(async () => {
            const data = await SendCreateUserReq(userRegData)
            if (data.status != 0) {
                toast.error("There was an error while registering your account, pleasae try again later.", {id: accToast})
            }
            else {
                toast.success("Account registration successful!", {description: "Redirecting to login page", id: accToast})
            }
            setTimeout(() => {setAuthMode("login");}, 2000)
        }, 800)

    }

    const loginHandler = async (username: string, password: string) => {
        const login_res = await SendLoginReq({"username": username, "password": password})
        console.log(login_res)
    }

    return <div className="auth-page">
        <Nav />
        <AnimatePresence mode="wait">
            {authMode === 'login' ? (
                <AuthLogin onLoginClick={loginHandler} onRegisterClick={() => setAuthMode('register')} />
            ) : authMode === 'register' ? (
                <AuthRegister onNext={regHandler01} onLoginClick={() => setAuthMode('login')} />
            ) : authMode === 'forgot' ? (
                <AuthForgotPassword onLoginClick={() => setAuthMode('login')} />
            ) : authMode === 'register1' ? (
                <AuthRegister1 onNext={regHandler12} onBack={onBack} />
            ) : authMode === 'register2' ? (
                <AuthRegister2 onNext={regHandler23} onBack={onBack1} />
            ) : <AuthLogin onLoginClick={loginHandler} onRegisterClick={() => setAuthMode('register')} />}
        </AnimatePresence>
    </div>
}

export default Auth;