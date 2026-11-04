import OrbitLogo from "../../../../GlobalComponents/OrbitLogo/OrbitLogo"

import './Nav.css';

function Nav() {
    return <div className="nav-container">
        <div className="nav-visible">
            <OrbitLogo size={30} />
            <p className="nav-logo-text">Orbit</p>
        </div>
    </div>;
}

export default Nav;