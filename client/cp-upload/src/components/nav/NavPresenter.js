import { AppBar, Toolbar, Typography, Box, Container, IconButton } from "@mui/material";
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

function NavPresenter(props) {
    const {mode, toggleMode} = props;

    return (
        <AppBar position="static">
            <Container>
                <Toolbar disableGutters>
                    <Typography
                        variant="h6"
                        noWrap
                        component="a"
                        href="/"
                        sx={{
                            mr: 2,
                            display: { xs: 'none', md: 'flex' },
                            fontFamily: 'monospace',
                            fontWeight: 700,
                            letterSpacing: '.3rem',
                            color: 'inherit',
                            textDecoration: 'none',
                            
                        }}
                    >
                        CP UPLOAD
                    </Typography>
                    

                    <Box sx={{ flexGrow: 1 }}/>
                    <IconButton sx={{ ml: 1 }} onClick={toggleMode} color="inherit">
                        {mode === 'dark' ? <Brightness7Icon /> : <Brightness4Icon />}
                    </IconButton>
                    <Typography
                        variant="h6"
                        component="a"
                        href="./auth"
                        sx={{
                            color: 'inherit',
                            textDecoration: 'none',
                            padding: '1px 4px',
                            "&:hover": {
                                boxShadow: 8,
                                padding: '4px 4px 1px 4px'
                            }
                        }}
                    >
                        SignIn/SignUp
                    </Typography>
                </Toolbar>
            </Container>
        </AppBar>
    );
}

export default NavPresenter;