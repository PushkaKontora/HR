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

function App() {
  const count = useAppSelector((state) => state.example.valueCount);
  const dispatch = useAppDispatch();

  const handlerClick = () => {
    dispatch(incremented());
  };
  return (
    <div className="App">
      <Routes>
        <Route path={'/'} element={<DefaultLayout/>}>
          <Route index element={
            <PrivateRoute requiredUserStatus={UserStatus.user}>
              <div>Example private page</div>
            </PrivateRoute>
          }/>
          <Route path={NoAuthRoutes.Login} element={<LoginPage/>}/>
          <Route path={NoAuthRoutes.SignUp} element={<SignUpPage/>}/>


        </Route>
      </Routes>
    </div>
  );
}

export default App;
