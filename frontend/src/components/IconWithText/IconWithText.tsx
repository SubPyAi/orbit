import type { SvgIconProps } from '@mui/material/SvgIcon'

function IconWithText(
    {
        icon: Icon,
        text
    } : {
        icon?: React.ComponentType<SvgIconProps>,
        text: string
    }
) {
    return <div className="icon-with-text-wrapper" style={{margin: "10px", marginTop: "40px", display: 'flex', flexDirection: 'row', alignItems: 'center', justifyContent: 'center'}}>
        <div className='icon-with-text-wrapper-icon' style={{height: '50px', width: '50px', backgroundColor: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center', borderRadius: '25px', border: "1px solid #C9C6C3"}}>
            {Icon && <Icon />}
        </div>
        <div className='icon-with-text-wrapper-text' style={{marginLeft: "10px"}}>
            <p>
                {text}
            </p>
        </div>
    </div>
}

export default IconWithText