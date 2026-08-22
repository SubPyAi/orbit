import './LandingFooter.css'

function LandingFooter() {
    return <div className='landing-footer-wrapper'>
        <div className='landing-footer-wrapper-copyright-wrapper'>
            <p style={{fontSize: "12px", letterSpacing: "0.03em", color: "#9A9A9A"}}>Copyright 2026 Orbit. All Rights Reserved.</p>
        </div>
        <div></div>
        <div className='landing-footer-wrapper-email-wrapper'>
            <p style={{fontSize: "12px", letterSpacing: "0.03em", color: "#9A9A9A"}}>info@orbit.com</p>
        </div>
    </div>
}

export default LandingFooter