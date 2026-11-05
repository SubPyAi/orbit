import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';
import './AuthRegister.css';
import Button from '../../GlobalComponents/Button/Button.tsx';
import TextField from '../../GlobalComponents/TextField/TextField.tsx';
import { motion } from 'motion/react';
import { toast } from 'sonner';
import React from 'react';
import DateField from '../../GlobalComponents/DateField/DateField.tsx';

function AuthRegister1(  { onNext, onBack }: { onNext: (name: string, DoB: string) => void; onBack: () => void}) {
    const [name, setName] = React.useState('');
    const [DoB, setDoB] = React.useState('');
    const [nameError, setNameError] = React.useState(false);

    const handleNextClick = () => {
        if (name === "") {
            toast.warning("Name cannot be empty!")
            setNameError(true)
        }
        else if (name.length < 4) {
            toast.warning("Your name must be atleast 4 characters!")
        }
        else if (DoB === "") {
            toast.warning("DoB cannot be empty")
        }
        else {
            console.log(DoB)
            onNext(name, DoB)
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
                    <p className="auth-subtitle">Let's get to know you a bit better</p>
                    <TextField label="Name" hasError={nameError} placeholder="Enter your name" className="auth-text-field" onChange={(e) => setName(e.target.value)} />
                    <DateField label="Date of birth" max={new Date().toLocaleDateString('en-CA')} onChange={(e) => { setDoB(e.target.value); }}/>
                    <div className="auth-actions">
                        <Button className="auth-signup-button" variant="secondary" onClick={onBack}>
                            Back
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

export default AuthRegister1;