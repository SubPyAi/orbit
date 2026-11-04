import Button from '../../GlobalComponents/Button/Button.tsx';
import Input from '../../GlobalComponents/TextField/TextField.tsx';
import GlassPanel from '../../GlobalComponents/GlassPanel/GlassPanel.tsx';

function DesignPreview() {
    return (
        <main className="design-preview">

            <GlassPanel intensity="normal">

                <h1>Welcome to Orbit.</h1>

                <p>
                    Your universe of connections.
                </p>

                <Input
                    label="Username"
                    placeholder="Enter your username"
                />

                <Input
                    label="Password"
                    type="password"
                    placeholder="Enter your password"
                />

                <Button fullWidth size="lg">
                    Sign in
                </Button>

                <Button variant="ghost" fullWidth>
                    Create an account
                </Button>

            </GlassPanel>

        </main>
    );
}

export default DesignPreview;