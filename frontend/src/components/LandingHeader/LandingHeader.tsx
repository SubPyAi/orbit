import Button from '../Button/Button'
import OrbitIcon from '../OrbitLogo/OrbitLogo';
import './LandingHeader.css'

function LandingHeader() {
    function handleLoginButtonClick() {
        console.log("eloooooooo");
    }

    return <div className='landing-header-wrapper'>
        <div className='landing-header-wrapper-brand-name'>
            <OrbitIcon size={25}></OrbitIcon>
            <p style={{marginLeft: "5px"}}>Orbit</p>
        </div>
        <div></div>
        <div className='landing-header-wrapper-actions'>
            <div className='landing-header-wrapper-actions-grid'>
                <Button text='Login' onClickFunction={handleLoginButtonClick} bkg='transparent' col='black' hoverCol='#C9C6C3' hoverGlowCol='green' height="40px" width="100px" borderRadius='8px' border='1px solid #C9C6C3' />
                <div></div>
                <Button text='Register' onClickFunction={handleLoginButtonClick} bkg='#1E3A5F' col='white' hoverCol='#173152' hoverGlowCol='green' height="40px" width="100px" borderRadius='8px' />
            </div>
        </div>
    </div>
}

export default LandingHeader