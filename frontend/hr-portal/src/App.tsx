import './App.css';
import '../src/init';
import {useAppDispatch, useAppSelector} from './app/hooks';
import {Navigate, Route, Routes} from 'react-router-dom';
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
import {FavoritePage} from './pages/favorite-page/favorite-page';
import EmployerMyVacancyScreen from './pages/employer-my-vacancy-screen/employer-my-vacancy-screen';
import EmployerResumeScreen from './pages/employer-resume-screen/employer-resume-screen';
import {toast} from 'react-toastify';

function App() {
  const status = useAppSelector((state) => state.general.statusUser);
  const dispatch = useAppDispatch();

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
            <PrivateRoute requiredUserStatus={UserStatus.employer}>
              <EmployerMyVacancyScreen/>
            </PrivateRoute>
          }/>
          <Route index element={
            <PrivateRoute requiredUserStatus={UserStatus.user}>
              <Navigate to={AuthRoutes.Vacancies}/>
            </PrivateRoute>
          }/>
          <Route path={AuthRoutes.Vacancies} element={
            <PrivateRoute requiredUserStatus={'anyLoggedIn'}>
              <JobSearchScreen/>
            </PrivateRoute>
          }/>
          <Route path={':id'} element={
            <PrivateRoute requiredUserStatus={'anyLoggedIn'}>
              <JobSearchDetailsScreen/>
            </PrivateRoute>
          }/>
          <Route path={AuthRoutes.Profile} element={
            <PrivateRoute requiredUserStatus={'anyLoggedIn'}>
              <ProfilePage/>
            </PrivateRoute>
          }/>
          <Route path={AuthRoutes.Favorite} element={
            <PrivateRoute requiredUserStatus={'anyLoggedIn'}>
              <FavoritePage/>
            </PrivateRoute>
          }/>
          <Route path={AuthRoutes.Resume} element={
            <PrivateRoute requiredUserStatus={UserStatus.employer}>
              <EmployerResumeScreen/>
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
