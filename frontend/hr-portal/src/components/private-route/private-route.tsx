import {Navigate} from 'react-router-dom';
import {useAppSelector} from '../../app/hooks';
import {NoAuthRoutes, Root} from '../../const/app-routes';
import {User} from '../../types/user';

type PrivateRouteProps = {
  requiredUserStatus: User
  children: JSX.Element;
};

function PrivateRoute(props: PrivateRouteProps): JSX.Element {
  const statusUser = useAppSelector((state) => state.general.statusUser);

  return statusUser === props.requiredUserStatus
    ? props.children
    : <Navigate to={Root + NoAuthRoutes.Login}/>;
}

export default PrivateRoute;