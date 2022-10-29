import './App.css';

import {incremented} from './features/example/example-slice';
import {useAppDispatch, useAppSelector} from './app/hooks';
import {BrowserRouter, Route, Routes} from 'react-router-dom';
import DefaultLayout from './components/layouts/default-layout/default-layout';

import {Root, NoAuthRoutes, AuthRoutes} from './const/app-routes';
import LoginPage from './pages/login-page/login-page';
import SignUpPage from './pages/sign-up-page/sign-up-page';
import PrivateRoute from './components/private-route/private-route';
import {User} from './types/user';

function App() {
  const count = useAppSelector((state) => state.example.valueCount);
  const dispatch = useAppDispatch();

  const handlerClick = () => {
    dispatch(incremented());
  };
  return (
    <div className="App">
      <Routes>
        <Route path={Root} element={<DefaultLayout/>}>
          <Route index element={
            <PrivateRoute requiredUserStatus={User.user}>
              <div>Example private page</div>
            </PrivateRoute>
          }/>
          <Route path={Root + NoAuthRoutes.Login} element={<LoginPage/>}/>
          <Route path={Root + NoAuthRoutes.SignUp} element={<SignUpPage/>}/>
        </Route>
      </Routes>
    </div>
  );
}

export default App;
