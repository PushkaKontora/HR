import cl from 'classnames';

import logoHeader from '../../assets/img/header/logo_m.svg';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent as LikeIcon} from '../../assets/img/header/default-likes.svg';
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
import {ReactComponent as PersonalIcon} from '../../assets/img/header/personal.svg';
import HeaderNav from '../header-nav/header-nav';

import './header.scss';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {logout} from '../../service/async-actions/async-actions-user';
import browserHistory from '../../service/browser-history';
import {UserStatus} from '../../types/user-status';
import {indicateStatus, setUser} from '../../features/general/general-slice';

function Header() {
  const isLoading = useAppSelector((state) => state.general.loading);
  const dispatch = useAppDispatch();

  const handlerClickLogout = () => {
    dispatch(logout())
      .then(() => {
        browserHistory.push('/login');
        dispatch(setUser(null));
        dispatch(indicateStatus(UserStatus.noAuth));
      });
  };

  return (
    <div className="header-wrapper">
      <div className="header-content">
        <div className="side-header side-header__leftSide">
          <div className="logo-header-wrapper">
            <img src={logoHeader} alt="logo"/>
          </div>
          <HeaderNav/>
        </div>
        <div className="side-header">
          <div className="header-nav-personal"><LikeIcon className="likes-icon"/></div>
          <div className="header-nav-personal"><PersonalIcon className="personal-icon"/></div>
          <div
            className="header-nav-personal header-nav-personal__exit"
            onClick={handlerClickLogout}
          >
            <button className={cl('btn-exit', {'btn-exit__load': isLoading})}>
              {isLoading
                ? (<div className="loading"/>)
                : (<>Выйти</>)
              }</button>

          </div>
        </div>
      </div>
    </div>
  );
}

export default Header;