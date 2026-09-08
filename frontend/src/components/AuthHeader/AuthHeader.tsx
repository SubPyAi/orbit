import OrbitIcon from '../OrbitLogo/OrbitLogo';
import './AuthHeader.css'

function AuthHeader() {
    return <div className='auth-header-wrapper'>
        <div className='auth-header-wrapper-brand-name'>
            <OrbitIcon size={30}></OrbitIcon>
            <p style={{marginLeft: "5px"}}>Orbit</p>
        </div>
    </div>
}

export default AuthHeader