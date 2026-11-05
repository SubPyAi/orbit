
import React from 'react';
import './TextField.css';

interface InputProps
    extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    hint?: string;
    hasError?: boolean;
}

function Input({
    label,
    error,
    hint,
    hasError = false,
    id,
    className = '',
    ...props
}: InputProps) {

    const inputId = id ?? React.useId();
    const messageId = `${inputId}-message`;

    const isError = hasError || Boolean(error);

    return (
        <div className="orbit-input-wrapper">

            {label && (
                <label
                    className="orbit-input-label"
                    htmlFor={inputId}
                >
                    {label}
                </label>
            )}

            <input
                id={inputId}
                className={[
                    'orbit-input',
                    isError ? 'orbit-input--error' : '',
                    className
                ].filter(Boolean).join(' ')}
                aria-invalid={isError ? true : undefined}
                aria-describedby={
                    error || hint ? messageId : undefined
                }
                {...props}
            />

            {(error || hint) && (
                <span
                    id={messageId}
                    className={
                        error
                            ? 'orbit-input-error'
                            : 'orbit-input-hint'
                    }
                >
                    {error ?? hint}
                </span>
            )}

        </div>
    );
}

export default Input;
