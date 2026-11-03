import React from 'react';
import './Button.css';

type ButtonVariant =
    | 'primary'
    | 'secondary'
    | 'outline'
    | 'ghost';

type ButtonSize =
    | 'sm'
    | 'md'
    | 'lg';

interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement> {

    variant?: ButtonVariant;
    size?: ButtonSize;
    fullWidth?: boolean;
}

function Button({
    variant = 'primary',
    size = 'md',
    fullWidth = false,
    className = '',
    children,
    ...props
}: ButtonProps) {

    const classes = [
        'orbit-button',
        `orbit-button--${variant}`,
        `orbit-button--${size}`,
        fullWidth ? 'orbit-button--full' : '',
        className
    ].filter(Boolean).join(' ');

    return (
        <button
            className={classes}
            {...props}
        >
            {children}
        </button>
    );
}

export default Button;