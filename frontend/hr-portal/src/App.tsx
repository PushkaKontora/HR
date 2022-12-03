import './App.css';
import '../src/init';
import {useAppDispatch, useAppSelector} from './app/hooks';
import {Route, Routes} from 'react-router-dom';
import DefaultLayout from './components/layouts/default-layout/default-layout';

import {NoAuthRoutes, AuthRoutes} from './const/app-routes';
import LoginPage from './pages/login-page/login-page';
import SignUpPage from './pages/sign-up-page/sign-up-page';
import PrivateRoute from './components/private-route/private-route';
import {UserStatus} from './types/user-status';
import React, {useEffect} from 'react';
import {checkToken} from './service/token-manager';
import JobSearchScreen from './pages/job-search-screen/job-search-screen';
import JobSearchDetailsScreen from './pages/job-search-details-screen/job-search-details-screen';
import ProfilePage from './pages/profile-page/profile-page';
import {ToastWrapper} from './components/toast-wrapper/toast-wrapper';
import browserHistory from './service/browser-history';
import EmployerMyVacancyScreen from './pages/employer-my-vacancy-screen/employer-my-vacancy-screen';

function App() {
  const status = useAppSelector((state) => state.general.statusUser);
  const dispatch = useAppDispatch();

  useEffect(() => {
    let isMounted = true;

    if (isMounted) {
      checkToken(dispatch);
      console.log(browserHistory.location);
      if (status !== UserStatus.noAuth) {
        browserHistory.go(-2);
      }
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
            status === UserStatus.user
              ? <PrivateRoute requiredUserStatus={UserStatus.user}>
                <JobSearchScreen/>
              </PrivateRoute>
              : <PrivateRoute requiredUserStatus={UserStatus.employer}>
                <EmployerMyVacancyScreen/>
              </PrivateRoute>
          }/>
          <Route path={':id'} element={
            <PrivateRoute requiredUserStatus={UserStatus.user && UserStatus.employer}>
              <JobSearchDetailsScreen/>
            </PrivateRoute>
          }/>
          <Route path={AuthRoutes.Profile} element={
            <PrivateRoute requiredUserStatus={'anyLoggedIn'}>
              <ProfilePage/>
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
