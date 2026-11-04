function NavElement(
    {
        label, redirect
    } : {
        label: string,
        redirect: string
    }
    
) {
    return (
        <div className="nav-element">
            <button className="nav-element-label" onClick={() => window.location.href = redirect}>
                {label}
            </button>
        </div>
    );
}

export default NavElement;