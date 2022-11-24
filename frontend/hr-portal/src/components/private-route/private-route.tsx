import {Navigate} from 'react-router-dom';
import {useAppSelector} from '../../app/hooks';
import {NoAuthRoutes} from '../../const/app-routes';
import {UserStatus} from '../../types/user-status';
import browserHistory from '../../service/browser-history';

type PrivateRouteProps = {
  requiredUserStatus: UserStatus | 'anyLoggedIn'
  children: JSX.Element;
};

function PrivateRoute(props: PrivateRouteProps): JSX.Element {
  const statusUser = useAppSelector((state) => state.general.statusUser);

  const condition =
    (statusUser === props.requiredUserStatus) ||
    (props.requiredUserStatus === 'anyLoggedIn' && statusUser !== UserStatus.noAuth);

  if (condition) {
    return (props.children);
  } else {
    return (<Navigate to={NoAuthRoutes.Login}/>);
  }
}

export default PrivateRoute;