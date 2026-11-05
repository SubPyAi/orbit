import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';
import './AuthRegister.css';
import Button from '../../GlobalComponents/Button/Button.tsx';
import { motion } from 'motion/react';
import { toast } from 'sonner';

function AuthRegister2(  { onNext, onBack }: { onNext: (pfp_ref: string) => void; onBack: () => void}) {
    const handleNextClick = () => {
        onNext("");
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
                    <p className="auth-subtitle">PS just skip this part </p>
                    <div className="auth-actions">
                        <Button className="auth-signup-button" variant="secondary" onClick={onBack}>
                            Back
                        </Button>
                        <Button className="auth-signup-button" variant="primary" onClick={handleNextClick}>
                            Create!
                        </Button>
                    </div>
                </div>
            </GlassPanel>
        </div>
    </motion.div>
}

export default AuthRegister2;