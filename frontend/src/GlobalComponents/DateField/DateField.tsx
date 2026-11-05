import React from 'react';
import './DateField.css';

interface DateFieldProps
    extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    hint?: string;
}

function DateField({
    label,
    error,
    hint,
    id,
    className = '',
    ...props
}: DateFieldProps) {

    const inputId = id ?? React.useId();
    const messageId = `${inputId}-message`;

    return (
        <div className="orbit-date-wrapper">

            {label && (
                <label
                    className="orbit-date-label"
                    htmlFor={inputId}
                >
                    {label}
                </label>
            )}

            <input
                {...props}
                id={inputId}
                type="date"
                className={[
                    'orbit-date',
                    error ? 'orbit-date--error' : '',
                    className
                ].filter(Boolean).join(' ')}
                aria-invalid={error ? true : undefined}
                aria-describedby={
                    error || hint ? messageId : undefined
                }
            />

            {(error || hint) && (
                <span id={messageId}>
                    {error ?? hint}
                </span>
            )}

        </div>
    );
}

export default DateField;