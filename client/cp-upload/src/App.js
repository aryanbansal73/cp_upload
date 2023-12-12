import './App.css';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter, Route, Routes, Redirect } from 'react-router-dom';
import React, { useState, useMemo} from 'react';
import AuthPresenter from './components/auth/AuthPresenter';
import HomePresenter from './components/home/HomePresenter';
import NavPresenter from './components/nav/NavPresenter';


function App() {
  const [mode, setMode] = useState('dark');
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
        },
      }),
    [mode],
  );

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="App">
        <NavPresenter mode={mode} toggleMode={colorMode.toggleColorMode} />
        <BrowserRouter>
          <Routes>
            <Route path="/" exact element={<HomePresenter />} />
            <Route path="/auth" exact element={<AuthPresenter />} />
          </Routes>
        </BrowserRouter>
      </div>
    </ThemeProvider>
  );
}

export default App;
