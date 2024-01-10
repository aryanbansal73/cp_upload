import Container from '@mui/material/Container';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import { useState } from 'react';
import { Box, ToggleButtonGroup, ToggleButton, Typography } from '@mui/material';
import SignIn from './SignIn';
import SignUp from './SignUp';

function AuthPresenter() {
    const [form, setForm] = useState('SignIn');

    const handleForm = (event, newForm) => {
        setForm(newForm);
    };

    return (
        <Container component="main" maxWidth="xs">
            <Box
                sx={{
                    marginTop: 8,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                }}
            >
                <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
                    <LockOutlinedIcon />
                </Avatar>
                <ToggleButtonGroup
                    value={form}
                    exclusive
                    onChange={handleForm}
                    aria-label="Select Sign In or Sign Up"
                >
                    <ToggleButton value="SignIn" aria-label="Sign In">
                        <Typography component="h1" variant="h5">
                            Sign In
                        </Typography>
                    </ToggleButton>
                    <ToggleButton value="SignUp" aria-label="Sign Up">
                        <Typography component="h1" variant="h5">
                            Sign Up
                        </Typography>
                    </ToggleButton>
                </ToggleButtonGroup>
                {form === 'SignIn' ? <SignIn/> : <></>}
                {form === 'SignUp' ? <SignUp/> : <></>}
            </Box>
      </Container>
    );
}

export default AuthPresenter;