import {Navigate} from 'react-router-dom';
import {useAppSelector} from '../../app/hooks';
import {NoAuthRoutes} from '../../const/app-routes';
import {UserStatus} from '../../types/user-status';

type PrivateRouteProps = {
  requiredUserStatus: UserStatus | 'anyLoggedIn'
  children: JSX.Element;
};

function PrivateRoute(props: PrivateRouteProps): JSX.Element {
  const statusUser = useAppSelector((state) => state.general.statusUser);

  return statusUser === props.requiredUserStatus
    ? props.children
    : <Navigate to={NoAuthRoutes.Login}/>;
}

export default PrivateRoute;