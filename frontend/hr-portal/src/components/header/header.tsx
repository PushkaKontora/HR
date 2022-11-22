import cl from 'classnames';

import logoHeader from '../../assets/img/header/logo_m.svg';
import likeIcon from '../../assets/img/header/likes.svg';
import personalIcon from '../../assets/img/header/personal.svg';
import exitIcon from '../../assets/img/header/button-exit.svg';
import {useAppSelector} from '../../app/hooks';
import './header.scss';
import {UserStatus} from '../../types/user-status';
import HeaderNav from '../header-nav/header-nav';

function Header() {

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
          <div className="header-nav-personal"><img src={likeIcon} alt="like icon"/></div>
          <div className="header-nav-personal"><img src={personalIcon} alt="personal icon"/></div>
          <div className="header-nav-personal"><img src={exitIcon} alt="exit icon"/></div>
        </div>
      </div>
    </div>
  );
}

export default Header;