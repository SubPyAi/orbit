import React from 'react';
import './GlassPanel.css';

interface GlassPanelProps
    extends React.HTMLAttributes<HTMLDivElement> {

    intensity?: 'subtle' | 'normal' | 'strong';
}

function GlassPanel({
    intensity = 'normal',
    className = '',
    children,
    ...props
}: GlassPanelProps) {

    const classes = [
        'orbit-glass-panel',
        `orbit-glass-panel--${intensity}`,
        className
    ].filter(Boolean).join(' ');

    return (
        <div
            className={classes}
            {...props}
        >
            {children}
        </div>
    );
}

export default GlassPanel;