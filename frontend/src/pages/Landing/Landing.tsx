import Button from '../../components/Button/Button'
import IconWithText from '../../components/IconWithText/IconWithText'
import LandingFooter from '../../components/LandingFooter/LandingFooter'
import LandingHeader from '../../components/LandingHeader/LandingHeader'
import LandingBg from '../../assets/images/landing-background.png'
import './Landing.css'


import ShieldOutlinedIcon from '@mui/icons-material/ShieldOutlined'
import BoltOutlinedIcon from '@mui/icons-material/BoltOutlined'
import SentimentSatisfiedOutlinedIcon from '@mui/icons-material/SentimentSatisfiedOutlined'
import KeyboardArrowDownIcon from '@mui/icons-material/KeyboardArrowDown'


function Landing() {
    function handleLoginButtonClick(){
        console.log("yeyyyy")
    }

    return <div className='appgrid' style={{backgroundImage: `url(${LandingBg})`, backgroundRepeat: 'no-repeat', backgroundSize: 'cover', backgroundPosition: 'center'}}>
                <LandingHeader />
                <div className='body'>
                    <div style={{backgroundColor: '#1E3A5F26', height: '32px', width: '175px', borderRadius: '16px', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
                        <p style={{fontWeight: 400}}>Introducing Orbit</p>
                    </div>
                    <div style={{height: "fit-content", flexGrow: 0, flexShrink: 0, display: 'flex'}}>
                        <p style={{fontSize: '50px', margin: '20px', lineHeight: 1.1, fontWeight: 200, letterSpacing: "0.03em"}}>
                            Chat that feels lighter.
                        </p>
                    </div>
                    <div>
                        <p style={{color: '#6B6B6B', letterSpacing: "0.02em"}}>
                            Orbit keeps conversations fast, private, and beautifully simple — on every device.
                        </p>
                    </div>
                    <div className='landing-header-wrapper-actions-grid' style={{marginTop: '15px', gridTemplateColumns: '1fr 10px 1fr'}}>
                        <Button text='Get Started' onClickFunction={handleLoginButtonClick} bkg='#1E3A5F' col='white' hoverCol='#173152' hoverGlowCol='green' height="40px" width="120px" borderRadius='8px' />
                        <div></div>
                        <Button text='Login' onClickFunction={handleLoginButtonClick} bkg='transparent' col='black' hoverCol='#C9C6C3' hoverGlowCol='green' height="40px" width="100px" borderRadius='8px' border='1px solid #C9C6C3' />
                    </div>
                    <div style={{marginTop: "10px"}}>
                        <p style={{display: "flex", alignItems: "center", justifyContent: "center", flexDirection: "row", fontWeight: 200, letterSpacing: "0.05em"}}>
                            Explore More <KeyboardArrowDownIcon sx={{ fontSize: '20px', color: '#1E3A5F' }} />
                        </p>
                    </div>
                    <div className='body-explore'>
                        <IconWithText icon={ShieldOutlinedIcon} text="Private by default." />
                        <IconWithText icon={BoltOutlinedIcon} text="High customisability for operators." />
                        <IconWithText icon={SentimentSatisfiedOutlinedIcon} text="Calm by design." />
                    </div>
                </div>
                <LandingFooter />
            </div>
}

export default Landing