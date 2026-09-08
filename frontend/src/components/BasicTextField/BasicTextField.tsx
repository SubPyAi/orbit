function BasicTextField(
    {
        placeholder = '',
        initialValue = '',
        onChange = () => {},
        type = 'text',
        disabled = false,
        hoverColor = '#C9C6C3',
        hoverGlowColor = '',
        height,
        width,
        borderRadius,
        backgroundColor,
        textColor,
        border = 'none',
    } : {
        placeholder?: string,
        initialValue?: string,
        onChange?: (value: string) => void,
        type: 'text' | 'password' | 'email' | 'number',
        disabled?: boolean,
        hoverColor?: string,
        hoverGlowColor?: string,
        height?: string,
        width?: string,
        borderRadius: string,
        backgroundColor: string,
        textColor: string,
        border: string,
    }
)

{
    return <div className="basic-text-field-wrapper" style={{"--height": height, "--width": width, "--border-radius": borderRadius, "--background-color": backgroundColor, "--text-color": textColor, "--border": border} as React.CSSProperties}>
        <input 
            className="basic-text-field-wrapper-input"
            type={type}
            placeholder={placeholder}
            value={initialValue}
            disabled={disabled}
        />
    </div>
}

export default BasicTextField;