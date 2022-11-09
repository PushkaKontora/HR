import './App.css';
import '../src/init';
import {useAppDispatch, useAppSelector} from './app/hooks';
import {Route, Routes} from 'react-router-dom';
import DefaultLayout from './components/layouts/default-layout/default-layout';

import {NoAuthRoutes} from './const/app-routes';
import LoginPage from './pages/login-page/login-page';
import SignUpPage from './pages/sign-up-page/sign-up-page';
import PrivateRoute from './components/private-route/private-route';
import {UserStatus} from './types/user-status';
import React, {useEffect} from 'react';
import {checkToken} from './service/token-manager';
import JobSearchScreen from './pages/job-search-screen/job-search-screen';
import JobSearchDetailsScreen from './pages/job-search-details-screen/job-search-details-screen';
import EmployerCreatingNewVacancy from './components/employer-creating-new-vacancy/employer-creating-new-vacancy';
import {Content} from './components/styled/markup/content';
import {ToastWrapper} from './components/toast-wrapper/toast-wrapper';

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
            <PrivateRoute requiredUserStatus={UserStatus.user}>
              <JobSearchScreen/>
            </PrivateRoute>
          }/>
          <Route path={':id'} element={
            <PrivateRoute requiredUserStatus={UserStatus.user}>
              <JobSearchDetailsScreen/>
            </PrivateRoute>
          }/>
          <Route path={NoAuthRoutes.Login} element={<LoginPage/>}/>
          <Route path={NoAuthRoutes.SignUp} element={<SignUpPage/>}/>
          <Route path={NoAuthRoutes.Vacancy} element={<JobSearchScreen/>}/>
          <Route path={'/empl'} element={<EmployerCreatingNewVacancy/>}/>
          <Route path={`${NoAuthRoutes.Vacancy}/:id`} element={<JobSearchDetailsScreen/>}/>
        </Route>
      </Routes>
      <ToastWrapper/>
    </div>
  );
}

export default App;
