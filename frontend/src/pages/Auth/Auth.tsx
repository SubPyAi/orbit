import AuthHeader from '../../components/AuthHeader/AuthHeader';
import Button from '../../components/Button/Button';

import bkg2 from '../../assets/videos/bkg2.mp4'
import "./Auth.css"
import React from 'react';
import { AnimatePresence, motion } from 'motion/react';
import BasicTextField from '../../components/BasicTextField/BasicTextField';

function Auth() {

    const handleRegisterRoute = () => {
        console.log("Register button clicked");
    }

    const [contentText, setContentText] = React.useState("Have you already created an orbit with us?");

    const handleLoginRoute = () => {
        setContentText("Enter your username.")
    }

    const [textAreaElements, setTextAreaElements] = React.useState(
        <BasicTextField 
            label='label'
            onChange={(value) => console.log(value)}
            placeholder='placeholder'
            initialValue='initialValue'
            type='text'
            textColor='white'
            backgroundColor='red'
            border='1px solid white'
            borderRadius='8px'
            height='40px'
            width='100%'
            hoverColor='#C9C6C3'
            hoverGlowColor='green'
            disabled={false}
        />
    )

    const [authWrapperContentContentButtons, setAuthWrapperContentContentButtons] = React.useState(
        [
            <Button
                text="No"
                onClickFunction={handleRegisterRoute}
                bkg="#1E3A5F"
                col="white"
                hoverCol="#173152"
                hoverGlowCol="green"
                height="40px"
                width="100px"
                borderRadius="8px"
                border="1px solid #C9C6C3"
            />,
            <div style={{ width: "10px", height: "2px" }} />,
            <Button
                text="Yes"
                onClickFunction={handleLoginRoute}
                bkg="transparent"
                col="white"
                hoverCol="#535150"
                hoverGlowCol="green"
                height="40px"
                width="100px"
                borderRadius="8px"
                border="1px solid #C9C6C3"
            />
        ]
    )

    return (
        <div className="auth-wrapper">

            <div className="auth-wrapper-video">
                <video autoPlay muted loop playsInline>
                    <source src={bkg2} type="video/mp4" />
                </video>
            </div>

            <motion.div className="auth-wrapper-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.5 }}>
                <AuthHeader />
                    <motion.div
                        layout
                        transition={{
                            layout: {
                                type: "spring",
                                stiffness: 300,
                                damping: 30
                            }
                        }}
                        className="auth-wrapper-content"
                    >
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={contentText}
                                className="auth-wrapper-content-content"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.2 }}
                            >
                                <motion.p>
                                    {contentText}
                                </motion.p>
                    
                                <div className="auth-wrapper-content-content-textarea">
                                    {textAreaElements}
                                </div>
                    
                                <div className="auth-wrapper-content-content-buttons">
                                    {authWrapperContentContentButtons}
                                </div>
                            </motion.div>
                        </AnimatePresence>
                    </motion.div>
            </motion.div>

        </div>
    );
}

export default Auth;