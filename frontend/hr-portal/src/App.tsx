import './App.css';

import {incremented} from './features/example/example-slice';
import {useAppDispatch, useAppSelector} from './app/hooks';
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import DefaultLayout from './components/layouts/default-layout/default-layout';

import {NoAuthRoutes, AuthRoutes} from './const/app-routes';
import LoginPage from './pages/login-page/login-page';
import SignUpPage from './pages/sign-up-page/sign-up-page';
import PrivateRoute from './components/private-route/private-route';
import {UserStatus} from './types/user-status';
import React, {useEffect} from 'react';
import {checkToken, getToken} from './service/token-manager';
import {Content} from './components/styled/markup/content';
import {ToastWrapper} from './components/toast-wrapper/toast-wrapper';

function App() {
  const count = useAppSelector((state) => state.example.valueCount);
  const status = useAppSelector((state) => state.general.statusUser);
  const dispatch = useAppDispatch();

  const handlerClick = () => {
    dispatch(incremented());
  };

  useEffect(() => {
    let isMounted = true;

    if (isMounted) {
      checkToken(dispatch);
    }

    return () => {
      isMounted = false;
    };
  }, [status]);

  return (
    <div className="App">
      <Routes>
        <Route path={'/'} element={<DefaultLayout/>}>
          <Route index element={
            <PrivateRoute requiredUserStatus={UserStatus.user}>
              <Content>
                <div>Example private page</div>
              </Content>
            </PrivateRoute>
          }/>
          <Route path={NoAuthRoutes.Login} element={<LoginPage/>}/>
          <Route path={NoAuthRoutes.SignUp} element={<SignUpPage/>}/>


        </Route>
      </Routes>
      <ToastWrapper/>
    </div>
  );
}

export default App;
